// Cloudflare Worker for datagovernancesignal.com.
// - Web requests are served from the static assets in dist/ (see wrangler.jsonc);
//   this script only runs when no asset matches.
// - /feeds/<id> relays a small allowlist of RSS feeds whose hosts block the GitHub
//   runners that run the ingestion pipeline (Substack).
// - Email sent to sources@datagovernancesignal.com (Email Routing → "Send to a Worker")
//   is parsed and stored in the private SOURCES KV namespace for the pipeline.
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

export default {
  async fetch(request) {
    const { pathname } = new URL(request.url);
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
