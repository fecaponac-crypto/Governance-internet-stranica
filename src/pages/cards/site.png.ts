import type { APIRoute } from 'astro';
import { renderSiteCard } from '../../utils/card';

export const GET: APIRoute = async () =>
  new Response(new Uint8Array(await renderSiteCard()), { headers: { 'Content-Type': 'image/png' } });
