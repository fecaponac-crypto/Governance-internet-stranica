// Cloudflare Worker for datagovernancesignal.com.
// - Web requests are served from the static assets in dist/ (see wrangler.jsonc);
//   this script only runs when no asset matches.
// - /feeds/<id> relays a small allowlist of RSS feeds whose hosts block the GitHub
//   runners that run the ingestion pipeline (Substack).
// - A Cron Trigger starts the ingestion workflow on GitHub (GitHub's own schedule
//   proved unreliable); needs the GITHUB_TOKEN secret on the Worker.
// - Email sent to sources@datagovernancesignal.com (Email Routing → "Send to a Worker")
//   is parsed and stored in the private SOURCES KV namespace for the pipeline.
// - POST /api/feedback records anonymous "Was this useful?" votes per page and month in KV
//   (counters only: no IP address, cookie or other identifier is stored).
//   GET /api/feedback?month=YYYY-MM returns them, with the FEEDBACK_READ_TOKEN secret as a Bearer token.
// - On Monday mornings the Worker emails the weekly traffic report (data/reports/weekly.md, written by
//   the pipeline) to the REPORT_EMAIL secret, which must be a verified Email Routing destination.
import PostalMime from 'postal-mime';

const MAX_SIZE = 5 * 1024 * 1024;
const KEEP_SECONDS = 120 * 24 * 60 * 60;
const MAX_TEXT = 200_000;

/** Collect unique http(s) links from the HTML and plain-text parts. */
export function extractLinks(html, text) {
  const links = [];
  const seen = new Set();
  const add = (raw, label) => {
    const url = raw.replace(/&amp;/g, '&').trim();
    if (!/^https?:\/\//i.test(url) || seen.has(url)) return;
    seen.add(url);
    links.push(label ? { url, text: label } : { url });
  };
  for (const m of html.matchAll(/<a\b[^>]*href\s*=\s*["']([^"']+)["'][^>]*>([\s\S]*?)<\/a>/gi)) {
    const label = m[2].replace(/<[^>]+>/g, ' ').replace(/&nbsp;/g, ' ').replace(/\s+/g, ' ').trim();
    add(m[1], label.slice(0, 300));
  }
  for (const m of text.matchAll(/https?:\/\/[^\s<>()"']+/g)) add(m[0].replace(/[.,;:!?\]]+$/, ''));
  return links;
}

/** Plain text from HTML, for messages that have no text/plain part. */
export function htmlToText(html) {
  return html
    .replace(/<(script|style|head)\b[\s\S]*?<\/\1>/gi, ' ')
    .replace(/<br\s*\/?>|<\/(p|div|h[1-6]|li|tr|table)>/gi, '\n')
    .replace(/<[^>]+>/g, ' ')
    .replace(/&nbsp;/g, ' ')
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&#39;|&rsquo;|&lsquo;/g, "'")
    .replace(/[ \t\u00a0]+/g, ' ')
    .replace(/ *\n[\s]*/g, '\n')
    .trim();
}

// Only these feeds can be relayed; anything else is a 404.
export const RELAYED_FEEDS = {
  'eu-ai-act-newsletter': 'https://artificialintelligenceact.substack.com/feed',
  'modern-data-101': 'https://moderndata101.substack.com/feed',
};
const FEED_CACHE_SECONDS = 1800;

async function relayFeed(id) {
  const upstream = RELAYED_FEEDS[id];
  if (!upstream) return new Response('Not found', { status: 404 });
  const res = await fetch(upstream, {
    headers: { 'User-Agent': 'Mozilla/5.0 (compatible; DataGovernanceSignal/0.1; +https://datagovernancesignal.com/about/)' },
    cf: { cacheTtl: FEED_CACHE_SECONDS, cacheEverything: true },
  });
  if (!res.ok) return new Response(`Upstream returned ${res.status}`, { status: 502 });
  return new Response(res.body, {
    headers: {
      'Content-Type': res.headers.get('Content-Type') ?? 'application/rss+xml; charset=utf-8',
      'Cache-Control': `public, max-age=${FEED_CACHE_SECONDS}`,
      'X-Robots-Tag': 'noindex',
    },
  });
}

const WORKFLOWS_URL = 'https://api.github.com/repos/fecaponac-crypto/Governance-internet-stranica/actions/workflows';
// Cron expression (as in wrangler.jsonc) -> workflow it starts and the KV key for its outcome.
export const CRON_JOBS = {
  '17 */3 * * *': { workflow: 'ingest.yml', key: 'cron:last' },
  '47 5 * * MON': { workflow: 'monday.yml', key: 'cron:last-monday', weeklyReport: true },
  // Public launch, 30 October 12:00 Zagreb; repeats yearly but does nothing after launch.
  '55 10 30 10 *': { workflow: 'launch.yml', key: 'cron:last-launch' },
  // One-off test of the weekly email (30 October 07:58 UTC); remove after the test.
  '58 7 30 10 *': { workflow: null, key: 'cron:last-report-test', weeklyReport: true },
};
const WORKFLOW_REF = 'claude/data-intelligence-portal-plan-v46ux0';

/** Keep the outcome of the latest cron run in KV (key "cron:last") so it can be checked in the dashboard. */
async function recordCron(env, event, key, outcome) {
  console.log(`cron ${event.cron}: ${outcome}`);
  await env.SOURCES?.put(key, JSON.stringify({ at: new Date().toISOString(), cron: event.cron, outcome }));
}

export async function dispatchWorkflow(env, workflow = 'ingest.yml') {
  if (!env.GITHUB_TOKEN) throw new Error('GITHUB_TOKEN secret not set on the Worker');
  const res = await fetch(`${WORKFLOWS_URL}/${workflow}/dispatches`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${env.GITHUB_TOKEN}`,
      Accept: 'application/vnd.github+json',
      'X-GitHub-Api-Version': '2022-11-28',
      'User-Agent': 'datagovernancesignal-worker',
    },
    body: JSON.stringify({ ref: WORKFLOW_REF }),
  });
  if (res.status !== 204) throw new Error(`workflow dispatch failed: ${res.status} ${await res.text()}`);
}

export const FEEDBACK_REASONS = ['not-relevant', 'too-technical', 'too-basic', 'possible-error'];
const FEEDBACK_PAGE = /^\/(news|opinion|monday-signal)\/[a-z0-9-]+\/$/;

const json = (body, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' } });

/** Count one vote ({page, vote: yes|no}) or one reason ({page, reason}) for the current month. */
export async function recordFeedback(request, env) {
  if (Number(request.headers.get('Content-Length') ?? 0) > 1000) return json({ error: 'too large' }, 413);
  let body;
  try {
    body = await request.json();
  } catch {
    return json({ error: 'bad json' }, 400);
  }
  const { page, vote, reason } = body ?? {};
  if (typeof page !== 'string' || !FEEDBACK_PAGE.test(page)) return json({ error: 'bad page' }, 400);
  if (vote !== undefined && vote !== 'yes' && vote !== 'no') return json({ error: 'bad vote' }, 400);
  if (reason !== undefined && !FEEDBACK_REASONS.includes(reason)) return json({ error: 'bad reason' }, 400);
  if ((vote === undefined) === (reason === undefined)) return json({ error: 'send a vote or a reason' }, 400);

  const key = `feedback:${new Date().toISOString().slice(0, 7)}:${page}`;
  const counts = (await env.SOURCES.get(key, 'json')) ?? { yes: 0, no: 0, reasons: {} };
  if (vote) counts[vote] += 1;
  if (reason) counts.reasons[reason] = (counts.reasons[reason] ?? 0) + 1;
  // Read-modify-write: two simultaneous votes on one page may count once; fine at this scale.
  await env.SOURCES.put(key, JSON.stringify(counts));
  return json({ ok: true });
}

/** All counters for one month, for the monthly figures (needs FEEDBACK_READ_TOKEN). */
export async function readFeedback(request, env) {
  const token = env.FEEDBACK_READ_TOKEN;
  if (!token || request.headers.get('Authorization') !== `Bearer ${token}`) return json({ error: 'not found' }, 404);
  const month = new URL(request.url).searchParams.get('month') ?? '';
  if (!/^\d{4}-\d{2}$/.test(month)) return json({ error: 'bad month' }, 400);
  const prefix = `feedback:${month}:`;
  const pages = {};
  let cursor;
  do {
    const list = await env.SOURCES.list({ prefix, cursor });
    for (const { name } of list.keys) pages[name.slice(prefix.length)] = await env.SOURCES.get(name, 'json');
    cursor = list.list_complete ? undefined : list.cursor;
  } while (cursor);
  return json({ month, pages });
}

const WEEKLY_REPORT_URL =
  'https://raw.githubusercontent.com/fecaponac-crypto/Governance-internet-stranica/claude/data-intelligence-portal-plan-v46ux0/data/reports/weekly.md';
const REPORT_FROM = 'reports@datagovernancesignal.com';

/** A plain-text email as raw MIME (what the send_email binding expects). */
export function reportMime(to, text, now = new Date()) {
  const subject = text.split('\n')[0].trim() || 'Weekly report';
  // RFC 2047 encoded subject, so the dash and other non-ASCII characters survive.
  const encoded = `=?UTF-8?B?${btoa(String.fromCharCode(...new TextEncoder().encode(subject)))}?=`;
  return [
    `From: "Data Governance Signal" <${REPORT_FROM}>`,
    `To: ${to}`,
    `Subject: ${encoded}`,
    `Date: ${now.toUTCString()}`,
    `Message-ID: <${crypto.randomUUID()}@datagovernancesignal.com>`,
    'MIME-Version: 1.0',
    'Content-Type: text/plain; charset=utf-8',
    'Content-Transfer-Encoding: 8bit',
    '',
    text.replace(/\n/g, '\r\n'),
  ].join('\r\n');
}

/** Email data/reports/weekly.md to REPORT_EMAIL. `makeMessage` is injectable for tests. */
export async function sendWeeklyReport(env, makeMessage) {
  if (!env.REPORT_EMAIL || !env.REPORT_MAILER) throw new Error('REPORT_EMAIL secret or REPORT_MAILER binding missing');
  const res = await fetch(WEEKLY_REPORT_URL, { headers: { 'User-Agent': 'datagovernancesignal-worker' } });
  if (!res.ok) throw new Error(`weekly report not found: ${res.status}`);
  const text = await res.text();
  if (!makeMessage) {
    const { EmailMessage } = await import('cloudflare:email');
    makeMessage = (from, to, raw) => new EmailMessage(from, to, raw);
  }
  await env.REPORT_MAILER.send(makeMessage(REPORT_FROM, env.REPORT_EMAIL, reportMime(env.REPORT_EMAIL, text)));
}

export default {
  async scheduled(event, env, ctx) {
    const key = Object.keys(CRON_JOBS).find((c) => c.toLowerCase() === String(event.cron).toLowerCase());
    const job = CRON_JOBS[key] ?? CRON_JOBS['17 */3 * * *'];
    if (job.workflow) ctx.waitUntil(
      dispatchWorkflow(env, job.workflow).then(
        () => recordCron(env, event, job.key, 'dispatched'),
        (err) => recordCron(env, event, job.key, `error: ${err.message}`.slice(0, 500)),
      ),
    );
    if (job.weeklyReport) {
      ctx.waitUntil(
        sendWeeklyReport(env).then(
          () => recordCron(env, event, 'cron:last-report', 'sent'),
          (err) => recordCron(env, event, 'cron:last-report', `error: ${err.message}`.slice(0, 500)),
        ),
      );
    }
  },

  async fetch(request, env) {
    const { pathname } = new URL(request.url);
    if (pathname === '/api/feedback') {
      if (request.method === 'POST') return recordFeedback(request, env);
      if (request.method === 'GET') return readFeedback(request, env);
      return json({ error: 'method not allowed' }, 405);
    }
    const match = pathname.match(/^\/feeds\/([a-z0-9-]+)\/?$/);
    if (match && request.method === 'GET') return relayFeed(match[1]);
    return new Response('Not found', { status: 404 });
  },

  async email(message, env) {
    if (message.rawSize > MAX_SIZE) {
      message.setReject('Message too large');
      return;
    }
    const email = await PostalMime.parse(message.raw);
    const received = new Date().toISOString();
    const record = {
      received,
      to: message.to,
      envelopeFrom: message.from,
      from: email.from ?? null,
      subject: email.subject ?? '',
      date: email.date ?? null,
      text: (email.text?.trim() ? email.text : htmlToText(email.html ?? '')).slice(0, MAX_TEXT),
      links: extractLinks(email.html ?? '', email.text ?? ''),
    };
    // Keys sort chronologically; the dashboard shows subject and sender as metadata.
    const key = `email:${received}:${crypto.randomUUID().slice(0, 8)}`;
    await env.SOURCES.put(key, JSON.stringify(record, null, 1), {
      expirationTtl: KEEP_SECONDS,
      metadata: { from: record.from?.address ?? message.from, subject: record.subject.slice(0, 200) },
    });
  },
};
