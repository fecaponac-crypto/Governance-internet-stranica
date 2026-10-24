// Run: node --test worker/
import { test } from 'node:test';
import assert from 'node:assert/strict';
import PostalMime from 'postal-mime';
import worker, { extractLinks } from './index.js';

const raw = [
  'From: Newsletter <news@example.com>',
  'To: sources@datagovernancesignal.com',
  'Subject: =?UTF-8?Q?Tjedni_pregled_=E2=80=94_AI?=',
  'Date: Sun, 25 Oct 2026 07:00:00 +0100',
  'MIME-Version: 1.0',
  'Content-Type: multipart/alternative; boundary="b"',
  '',
  '--b',
  'Content-Type: text/plain; charset=utf-8',
  '',
  'EDPB guidelines https://www.edpb.europa.eu/news/x_en. More: https://example.org/a?x=1&y=2',
  '--b',
  'Content-Type: text/html; charset=utf-8',
  '',
  '<p><a href="https://www.edpb.europa.eu/news/x_en">EDPB <b>guidelines</b></a> <a href="mailto:a@b.c">mail</a> <a href="https://example.org/a?x=1&amp;y=2">more</a></p>',
  '--b--',
  '',
].join('\r\n');

test('extractLinks keeps unique http links with labels', async () => {
  const email = await PostalMime.parse(raw);
  const links = extractLinks(email.html, email.text);
  assert.deepEqual(links, [
    { url: 'https://www.edpb.europa.eu/news/x_en', text: 'EDPB guidelines' },
    { url: 'https://example.org/a?x=1&y=2', text: 'more' },
  ]);
});

test('email handler stores parsed message in KV', async () => {
  const stored = [];
  const env = { SOURCES: { put: async (key, value, opts) => stored.push({ key, value: JSON.parse(value), opts }) } };
  const message = {
    from: 'bounce@example.com',
    to: 'sources@datagovernancesignal.com',
    rawSize: raw.length,
    raw: new Response(raw).body,
    setReject: () => assert.fail('should not reject'),
  };
  await worker.email(message, env);
  assert.equal(stored.length, 1);
  assert.match(stored[0].key, /^email:\d{4}-\d{2}-\d{2}T/);
  assert.equal(stored[0].value.subject, 'Tjedni pregled — AI');
  assert.equal(stored[0].value.from.address, 'news@example.com');
  assert.equal(stored[0].value.links.length, 2);
  assert.equal(stored[0].opts.metadata.subject, 'Tjedni pregled — AI');
});
