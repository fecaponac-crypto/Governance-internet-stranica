// Generates the 1200×630 news card used on the site and as the social preview image.
import { readFileSync } from 'node:fs';
import { createRequire } from 'node:module';
import satori from 'satori';
import { Resvg } from '@resvg/resvg-js';
import { categoryById, SITE } from '../data/site';
import type { Article } from './articles';

export const CARD_WIDTH = 1200;
export const CARD_HEIGHT = 630;

const require = createRequire(import.meta.url);
const font = (pkg: string, file: string) => readFileSync(require.resolve(`${pkg}/files/${file}`));

const fonts = [
  { name: 'Serif', data: font('@fontsource/source-serif-4', 'source-serif-4-latin-700-normal.woff'), weight: 700 as const },
  { name: 'Sans', data: font('@fontsource/inter', 'inter-latin-500-normal.woff'), weight: 500 as const },
  { name: 'Sans', data: font('@fontsource/inter', 'inter-latin-700-normal.woff'), weight: 700 as const },
];

const C = {
  bg: '#14213d',
  ink: '#fbfaf7',
  muted: '#aab3c5',
  dim: '#2b3a5c',
  signal: '#f08a5d',
};

type Node = { type: string; props: Record<string, unknown> };
const h = (type: string, style: Record<string, unknown>, children?: unknown, extra: Record<string, unknown> = {}): Node => ({
  type,
  props: { style, children, ...extra },
});

// Shrink the headline figure so long values still fit on one or two lines.
function figureSize(text: string): number {
  const n = text.length;
  if (n <= 8) return 168;
  if (n <= 12) return 132;
  if (n <= 18) return 104;
  return 84;
}

function arcs(): Node {
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="420" height="420" viewBox="0 0 420 420" fill="none">
    <circle cx="70" cy="350" r="22" fill="${C.signal}"/>
    <path d="M70 230a120 120 0 0 1 120 120" stroke="${C.dim}" stroke-width="26" stroke-linecap="round"/>
    <path d="M70 130a220 220 0 0 1 220 220" stroke="${C.dim}" stroke-width="26" stroke-linecap="round"/>
    <path d="M70 30a320 320 0 0 1 320 320" stroke="${C.dim}" stroke-width="26" stroke-linecap="round"/>
  </svg>`;
  return h('img', { position: 'absolute', right: 0, bottom: 0, width: 420, height: 420 }, undefined, {
    src: `data:image/svg+xml;base64,${Buffer.from(svg).toString('base64')}`,
    width: 420,
    height: 420,
  });
}

function bars(level: number): Node {
  return h(
    'div',
    { display: 'flex', alignItems: 'flex-end', gap: 6 },
    [1, 2, 3, 4, 5].map((i) =>
      h('div', { width: 10, height: 26, borderRadius: 2, background: i <= level ? C.signal : C.dim }),
    ),
  );
}

export async function renderCard(article: Article, width = CARD_WIDTH): Promise<Buffer> {
  const { data } = article;
  return renderFrame({
    eyebrow: [data.type, data.region].filter(Boolean).join('  ·  ').toUpperCase(),
    figure: data.card?.figure ?? data.type,
    caption: data.card?.caption ?? data.dek,
    topic: categoryById(data.categories[0]).label,
    importance: data.importance,
    width,
  });
}

// Default share image for pages without their own card.
export const renderSiteCard = () =>
  renderFrame({
    eyebrow: 'DATA GOVERNANCE · PRIVACY · AI GOVERNANCE',
    figure: 'Signal, not noise.',
    caption: 'What matters in data governance, and why — editor-reviewed, every source linked.',
    topic: 'datagovernancesignal.com',
  });

interface Frame {
  eyebrow: string;
  figure: string;
  caption: string;
  topic: string;
  importance?: number;
  width?: number;
}

async function renderFrame({ eyebrow, figure, caption, topic, importance, width = CARD_WIDTH }: Frame): Promise<Buffer> {
  const tree = h(
    'div',
    {
      width: CARD_WIDTH,
      height: CARD_HEIGHT,
      boxSizing: 'border-box',
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'space-between',
      padding: '64px 72px',
      background: C.bg,
      color: C.ink,
      fontFamily: 'Sans',
      position: 'relative',
    },
    [
      arcs(),
      h('div', { display: 'flex', alignItems: 'center', justifyContent: 'space-between' }, [
        h('div', { display: 'flex', fontSize: 26, fontWeight: 700, letterSpacing: 3, color: C.signal }, eyebrow),
        importance ? bars(importance) : h('div', { display: 'flex' }, ''),
      ]),
      h('div', { display: 'flex', flexDirection: 'column', maxWidth: 900 }, [
        h(
          'div',
          { display: 'flex', fontFamily: 'Serif', fontWeight: 700, fontSize: figureSize(figure), lineHeight: 1.02, letterSpacing: -2 },
          figure,
        ),
        h('div', { display: 'flex', marginTop: 22, fontSize: 36, lineHeight: 1.3, color: C.muted, maxWidth: 820 }, caption),
      ]),
      h('div', { display: 'flex', alignItems: 'center', gap: 10, fontSize: 26, color: C.muted }, [
        h('div', { display: 'flex', fontFamily: 'Serif', fontWeight: 700, color: C.ink }, 'Data Governance'),
        h('div', { display: 'flex', fontFamily: 'Serif', fontWeight: 700, color: C.signal }, 'Signal'),
        h('div', { display: 'flex', marginLeft: 12 }, `·  ${topic}`),
      ]),
    ],
  );

  const svg = await satori(tree as Parameters<typeof satori>[0], { width: CARD_WIDTH, height: CARD_HEIGHT, fonts });
  return new Resvg(svg, { fitTo: { mode: 'width', value: width } }).render().asPng();
}

export const cardUrl = (article: Article) => `/cards/${article.id}.png`;
// Smaller copy for list thumbnails.
export const THUMB_WIDTH = 480;
export const thumbUrl = (article: Article) => `/cards/thumbs/${article.id}.png`;
export const cardAbsoluteUrl = (article: Article) => new URL(cardUrl(article), SITE.url).href;
export const SITE_CARD_URL = new URL('/cards/site.png', SITE.url).href;

// Brand images for directories such as Google News: a square icon and a wide wordmark.
const ICON_SVG = (fg: string) => `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
  <rect width="32" height="32" rx="7" fill="${C.bg}"/>
  <circle cx="10" cy="22" r="3" fill="#e4572e"/>
  <path d="M10 13a9 9 0 0 1 9 9" fill="none" stroke="${fg}" stroke-width="2.6" stroke-linecap="round"/>
  <path d="M10 6.5A15.5 15.5 0 0 1 25.5 22" fill="none" stroke="${fg}" stroke-width="2.6" stroke-linecap="round"/>
</svg>`;

export function renderLogoSquare(size = 1024): Buffer {
  return new Resvg(ICON_SVG(C.ink), { fitTo: { mode: 'width', value: size } }).render().asPng();
}

/** Wordmark on a transparent background: icon + "Data Governance Signal", dark text for light backgrounds. */
export async function renderLogoWide(width = 1600, height = 280): Promise<Buffer> {
  const icon = `data:image/svg+xml;base64,${Buffer.from(ICON_SVG(C.ink)).toString('base64')}`;
  const word = (text: string, color: string) =>
    h('div', { display: 'flex', fontFamily: 'Serif', fontWeight: 700, fontSize: 104, color, whiteSpace: 'nowrap' }, text);
  const tree = h('div', { width, height, display: 'flex', alignItems: 'center', padding: '0 48px', boxSizing: 'border-box' }, [
    h('img', { width: 184, height: 184, marginRight: 52 }, undefined, { src: icon, width: 184, height: 184 }),
    word('Data Governance', '#1b1f24'),
    h('div', { display: 'flex', width: 28 }, ''),
    word('Signal', '#c2410c'),
  ]);
  const svg = await satori(tree as Parameters<typeof satori>[0], { width, height, fonts });
  return new Resvg(svg, { fitTo: { mode: 'width', value: width } }).render().asPng();
}
