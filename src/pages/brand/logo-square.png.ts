import type { APIRoute } from 'astro';
import { renderLogoSquare } from '../../utils/card';

export const GET: APIRoute = () =>
  new Response(new Uint8Array(renderLogoSquare()), { headers: { 'Content-Type': 'image/png' } });
