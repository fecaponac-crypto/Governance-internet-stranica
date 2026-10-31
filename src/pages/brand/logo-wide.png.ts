import type { APIRoute } from 'astro';
import { renderLogoWide } from '../../utils/card';

export const GET: APIRoute = async () =>
  new Response(new Uint8Array(await renderLogoWide()), { headers: { 'Content-Type': 'image/png' } });
