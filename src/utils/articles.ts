import { getCollection, type CollectionEntry } from 'astro:content';
import { SITE } from '../data/site';

export type Article = CollectionEntry<'articles'>;

export async function getArticles(): Promise<Article[]> {
  // Sample articles exist only for the preview.
  const all = await getCollection('articles', ({ data }) => !data.draft && (SITE.preview || !data.sample));
  return all.sort((a, b) => b.data.date.getTime() - a.data.date.getTime());
}

export const articleUrl = (a: Article) => `/news/${a.id}/`;

const DAY = 864e5;

/**
 * Homepage lead: importance minus half a point per day of age, so a Critical story leads for
 * about two days and an Important one for about a day, unless something as weighty arrives.
 * An editor's pin (featuredUntil) wins while it lasts. `articles` must be newest first.
 */
export function pickLead(articles: Article[], now = new Date()): Article | undefined {
  const today = now.getTime();
  const pinned = articles.find((a) => a.data.featuredUntil && a.data.featuredUntil.getTime() + DAY > today);
  if (pinned) return pinned;
  const score = (a: Article) => a.data.importance - 0.5 * Math.max(0, (today - a.data.date.getTime()) / DAY);
  const recent = articles.filter((a) => today - a.data.date.getTime() <= 14 * DAY);
  // Sort is stable, so ties go to the newer story.
  return [...recent].sort((a, b) => score(b) - score(a))[0] ?? articles[0];
}

/**
 * Stories that rotate in the homepage lead slot: the lead, then up to two other Important or
 * Critical stories from the last 7 days, best score first.
 */
export function pickLeadStories(articles: Article[], now = new Date(), max = 3): Article[] {
  const lead = pickLead(articles, now);
  if (!lead) return [];
  const today = now.getTime();
  const score = (a: Article) => a.data.importance - 0.5 * Math.max(0, (today - a.data.date.getTime()) / DAY);
  const others = articles
    .filter((a) => a !== lead && a.data.importance >= 4 && today - a.data.date.getTime() <= 7 * DAY)
    .sort((a, b) => score(b) - score(a));
  return [lead, ...others].slice(0, max);
}

export function formatDate(d: Date): string {
  return d.toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric', timeZone: 'UTC' });
}

export const isoDate = (d: Date) => d.toISOString().slice(0, 10);

export type Column = CollectionEntry<'columns'>;
export type Prediction = CollectionEntry<'predictions'>;

export async function getColumns(): Promise<Column[]> {
  const all = await getCollection('columns', ({ data }) => !data.draft);
  return all.sort((a, b) => b.data.date.getTime() - a.data.date.getTime());
}

export const columnUrl = (c: Column) => `/monday-signal/${c.id}/`;

export async function getPredictions(): Promise<Prediction[]> {
  const all = await getCollection('predictions');
  return all.sort((a, b) => a.data.due.getTime() - b.data.due.getTime());
}

// Correct = 1, partly = 0.5, wrong = 0; open and void predictions are not scored.
const OUTCOME: Record<string, number> = { correct: 1, partly: 0.5, wrong: 0 };

export function scorecard(predictions: Prediction[]) {
  const judged = predictions.filter((p) => p.data.status in OUTCOME);
  const hits = judged.reduce((sum, p) => sum + OUTCOME[p.data.status], 0);
  // Brier score for predictions with a stated confidence: 0 is perfect, 0.25 is a coin flip.
  const rated = judged.filter((p) => p.data.confidence !== undefined);
  const brier = rated.length
    ? rated.reduce((sum, p) => sum + (p.data.confidence! / 100 - OUTCOME[p.data.status]) ** 2, 0) / rated.length
    : undefined;
  return {
    total: predictions.length,
    open: predictions.filter((p) => p.data.status === 'open').length,
    judged: judged.length,
    hitRate: judged.length ? hits / judged.length : undefined,
    brier,
  };
}

export type Opinion = CollectionEntry<'opinion'>;

export async function getOpinions(): Promise<Opinion[]> {
  // An essay dated in the future is scheduled: it appears with the first build on or after its
  // date (the site rebuilds every morning at about 07:20 Zagreb time).
  const now = Date.now();
  const all = await getCollection('opinion', ({ data }) => !data.draft && data.date.getTime() <= now);
  return all.sort((a, b) => b.data.date.getTime() - a.data.date.getTime());
}

export const opinionUrl = (o: Opinion) => `/opinion/${o.id}/`;

/** Amounts as readers expect them: "EUR 7m", "USD 25bn", "NOK 92m", "EUR 450,000". */
export function formatAmount(amount?: number, currency?: string): string {
  if (!amount || !currency) return '—';
  const n = (v: number) => (Number.isInteger(v) ? String(v) : v.toFixed(v < 10 ? 2 : 1).replace(/\.0+$|0+$/, ''));
  if (amount >= 1e9) return `${currency} ${n(amount / 1e9)}bn`;
  if (amount >= 1e6) return `${currency} ${n(amount / 1e6)}m`;
  return `${currency} ${amount.toLocaleString('en-GB')}`;
}
