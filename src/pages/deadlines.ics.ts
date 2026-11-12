// Calendar feed of the key dates (/deadlines/): subscribe once, new dates appear by themselves.
import { createHash } from 'node:crypto';
import { SITE } from '../data/site';
import { articleUrl, getArticles, getKeyDates, isoDate } from '../utils/articles';

const esc = (s: string) => s.replace(/\\/g, '\\\\').replace(/\r?\n/g, '\\n').replace(/([,;])/g, '\\$1');
const day = (d: Date) => isoDate(d).replace(/-/g, '');
// RFC 5545: lines of at most 75 octets, continued with a leading space.
function fold(line: string): string {
  const out: string[] = [];
  let current = '';
  for (const ch of line) {
    if (Buffer.byteLength(current + ch) > (out.length ? 74 : 75)) {
      out.push(current);
      current = '';
    }
    current += ch;
  }
  return [...out, current].join('\r\n ');
}

export async function GET() {
  const dates = await getKeyDates(await getArticles());
  const cutoff = Date.now() - 30 * 864e5;
  const lines = [
    'BEGIN:VCALENDAR',
    'VERSION:2.0',
    `PRODID:-//${SITE.name}//Key dates//EN`,
    'CALSCALE:GREGORIAN',
    'METHOD:PUBLISH',
    `X-WR-CALNAME:${esc(`${SITE.name}: key dates`)}`,
    `X-WR-CALDESC:${esc('Application dates, comment deadlines, hearings and votes in data protection, AI and data regulation.')}`,
    'REFRESH-INTERVAL;VALUE=DURATION:PT12H',
    'X-PUBLISHED-TTL:PT12H',
  ];
  for (const d of dates.filter((x) => x.date.getTime() >= cutoff)) {
    const url = new URL(articleUrl(d.article), SITE.url).href;
    const next = new Date(d.date.getTime() + 864e5);
    lines.push(
      'BEGIN:VEVENT',
      `UID:${createHash('sha1').update(`${isoDate(d.date)}|${d.what}`).digest('hex').slice(0, 24)}@datagovernancesignal.com`,
      `DTSTAMP:${day(d.article.data.date)}T000000Z`,
      `DTSTART;VALUE=DATE:${day(d.date)}`,
      `DTEND;VALUE=DATE:${day(next)}`,
      `SUMMARY:${esc(d.what)}`,
      `DESCRIPTION:${esc(`${d.kind}. From: ${d.article.data.title}\n${url}`)}`,
      `URL:${url}`,
      `CATEGORIES:${esc(d.kind)}`,
      'TRANSP:TRANSPARENT',
      'END:VEVENT',
    );
  }
  lines.push('END:VCALENDAR');
  return new Response(lines.map(fold).join('\r\n') + '\r\n', {
    headers: { 'Content-Type': 'text/calendar; charset=utf-8', 'Content-Disposition': 'inline; filename="data-governance-signal-key-dates.ics"' },
  });
}
