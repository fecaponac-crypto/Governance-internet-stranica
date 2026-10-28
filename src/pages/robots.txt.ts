import type { APIRoute } from 'astro';
import { SITE } from '../data/site';

// Preview: keep sample content out of search engines, but let link-preview bots read pages
// so shared links show a title and card. After launch: everything open, with the sitemap.
const PREVIEW = `User-agent: LinkedInBot
User-agent: Twitterbot
User-agent: facebookexternalhit
User-agent: Slackbot
User-agent: Slackbot-LinkExpanding
User-agent: TelegramBot
User-agent: WhatsApp
User-agent: SkypeUriPreview
User-agent: Discordbot
Allow: /

User-agent: *
Disallow: /
`;

const LIVE = `User-agent: *
Allow: /

Sitemap: ${SITE.url}/sitemap-index.xml
`;

export const GET: APIRoute = () =>
  new Response(SITE.preview ? PREVIEW : LIVE, { headers: { 'Content-Type': 'text/plain; charset=utf-8' } });
