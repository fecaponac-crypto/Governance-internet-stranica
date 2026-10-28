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
  const all = await getCollection('opinion', ({ data }) => !data.draft);
  return all.sort((a, b) => b.data.date.getTime() - a.data.date.getTime());
}

export const opinionUrl = (o: Opinion) => `/opinion/${o.id}/`;
