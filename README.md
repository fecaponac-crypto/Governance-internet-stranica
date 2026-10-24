# Data Governance Signal

*What matters in data governance, and why.* — https://datagovernancesignal.com

Independent, editor-reviewed briefing on data governance, privacy, AI governance and data regulation.

## Documentation (Croatian)

- [Project specification](docs/specifikacija.md)
- [Source catalog overview](docs/katalog-izvora.md) · data: [`data/sources.yaml`](data/sources.yaml)

## Site

Static site built with [Astro](https://astro.build) and searchable with [Pagefind](https://pagefind.app).

```sh
npm install
npm run dev       # http://localhost:4321 (search works only after a build)
npm run build     # astro build (includes Pagefind index) -> dist/
npm run preview   # serve dist/
npm run check     # type check
```

Requires Node.js >= 22.23.4 (see `.node-version`).

### Content

Articles live in `src/content/articles/*.md`. Front matter is validated by `src/content.config.ts`:
`title`, `date` (original news date), `dek`, `whyItMatters`, `categories`, `whoShouldCare`,
`importance` (1–5), `type`, `region`, `sources` (mark primary sources), `related`, `card`, `sample`, `draft`.

Each article gets a 1200×630 news card at `/cards/<slug>.png` (`src/utils/card.ts`), used on the site
and as the social preview image. `card.figure` is the key fact in large type (e.g. `NOK 92M`),
`card.caption` one short line; without them the card falls back to the content type and standfirst.

Categories are defined in `src/data/site.ts` and must match `data/sources.yaml`.

### Preview mode

`SITE.preview` in `src/data/site.ts` shows the preview banner and adds `noindex`.
`public/robots.txt` blocks crawlers. At launch: set `preview: false`, remove `sample` articles,
and allow crawling in `robots.txt` (add `Sitemap: https://datagovernancesignal.com/sitemap-index.xml`).

### Deployment (Cloudflare Pages)

- Build command: `npm run build` (or `npx astro build` — the search index is built by an Astro integration)
- Output directory: `dist`
- Node version: taken from `.node-version`
