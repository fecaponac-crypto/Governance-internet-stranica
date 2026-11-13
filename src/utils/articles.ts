import { getCollection, type CollectionEntry } from 'astro:content';
import { SITE } from '../data/site';

export type Article = CollectionEntry<'articles'>;

export async function getArticles(): Promise<Article[]> {
  // Sample articles exist only for the preview.
  const all = await getCollection('articles', ({ data }) => !data.draft && (SITE.preview || !data.sample));
  return all.sort((a, b) => b.data.date.getTime() - a.data.date.getTime());
}

/** News reports a development; analysis, opinion and how-to pieces are someone's view or advice. */
export const isNews = (a: Article) => a.data.format === 'News';
export const getNews = async () => (await getArticles()).filter(isNews);
export const getAnalysis = async () => (await getArticles()).filter((a) => !isNews(a));

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

export type Enforcement = NonNullable<Article['data']['enforcement']>;
export interface CaseStep {
  article: Article;
  e: Enforcement;
}
export interface EnforcementCase {
  id: string;
  steps: CaseStep[]; // oldest first
  latest: CaseStep;
  // The most recent step with an amount (a settlement or fine stays visible after a later ruling).
  amount?: { amount: number; currency: string };
  status: 'Open' | 'Closed';
}

/**
 * Enforcement records grouped into cases (stories without a case id are a case of their own).
 * A case is closed when its latest step is a settlement or is marked final (appeal waived,
 * final judgment); otherwise it is open. Newest activity first.
 */
export function enforcementCases(articles: Article[]): EnforcementCase[] {
  const byCase = new Map<string, CaseStep[]>();
  for (const article of articles) {
    const e = article.data.enforcement;
    if (!e) continue;
    const id = e.case ?? article.id;
    byCase.set(id, [...(byCase.get(id) ?? []), { article, e }]);
  }
  return [...byCase]
    .map(([id, steps]) => {
      steps.sort((a, b) => a.e.date.getTime() - b.e.date.getTime());
      const latest = steps[steps.length - 1];
      const withAmount = [...steps].reverse().find((s) => s.e.amount && s.e.currency);
      return {
        id,
        steps,
        latest,
        amount: withAmount ? { amount: withAmount.e.amount!, currency: withAmount.e.currency! } : undefined,
        status: (latest.e.final || latest.e.action === 'Settlement' ? 'Closed' : 'Open') as 'Open' | 'Closed',
      };
    })
    .sort((a, b) => b.latest.e.date.getTime() - a.latest.e.date.getTime());
}

// Rough euro values, used only to order amounts in different currencies; amounts are always shown as stated.
const ROUGH_EUR: Record<string, number> = { EUR: 1, USD: 0.92, GBP: 1.17, CHF: 1.05, NOK: 0.085, SEK: 0.09, DKK: 0.134, CAD: 0.67, AUD: 0.6 };
const roughEur = (a: { amount: number; currency: string }) => a.amount * (ROUGH_EUR[a.currency] ?? 1);

/** Where a case belongs in the country totals: US states and courts count as United States, EU bodies as EU. */
export const enforcementCountry = (jurisdiction: string): string =>
  /\bUS\b|United States/.test(jurisdiction) ? 'United States' : /^EU\b/.test(jurisdiction) ? 'EU' : /\bUK\b|United Kingdom/.test(jurisdiction) ? 'United Kingdom' : jurisdiction;

export interface EnforcementGroup {
  label: string;
  cases: number;
  open: number;
  // Stated amounts added up per currency, largest first; never converted.
  amounts: { amount: number; currency: string }[];
}

function groupCases(cases: EnforcementCase[], key: (c: EnforcementCase) => string): EnforcementGroup[] {
  const groups = new Map<string, EnforcementCase[]>();
  for (const c of cases) groups.set(key(c), [...(groups.get(key(c)) ?? []), c]);
  return [...groups]
    .map(([label, list]) => {
      const sums = new Map<string, number>();
      for (const c of list) if (c.amount) sums.set(c.amount.currency, (sums.get(c.amount.currency) ?? 0) + c.amount.amount);
      return {
        label,
        cases: list.length,
        open: list.filter((c) => c.status === 'Open').length,
        amounts: [...sums].map(([currency, amount]) => ({ amount, currency })).sort((a, b) => roughEur(b) - roughEur(a)),
      };
    })
    .sort((a, b) => b.cases - a.cases || a.label.localeCompare(b.label));
}

/** The tracker in numbers: cases by law, by country and by period, and the largest stated amounts. */
export function enforcementTotals(cases: EnforcementCase[]) {
  const years = new Set(cases.map((c) => c.latest.e.date.getUTCFullYear()));
  const byMonth = years.size < 2;
  const period = (c: EnforcementCase) =>
    byMonth ? c.latest.e.date.toLocaleDateString('en-GB', { month: 'long', year: 'numeric', timeZone: 'UTC' }) : String(c.latest.e.date.getUTCFullYear());
  const newest = new Map<string, number>();
  for (const c of cases) newest.set(period(c), Math.max(newest.get(period(c)) ?? 0, c.latest.e.date.getTime()));
  return {
    byLaw: groupCases(cases, (c) => c.latest.e.framework),
    byCountry: groupCases(cases, (c) => enforcementCountry(c.latest.e.jurisdiction)),
    byPeriod: groupCases(cases, period).sort((a, b) => newest.get(b.label)! - newest.get(a.label)!),
    periodLabel: byMonth ? 'Month' : 'Year',
    largest: cases
      .filter((c) => c.amount)
      .sort((a, b) => roughEur(b.amount!) - roughEur(a.amount!))
      .slice(0, 5),
  };
}

export type LegislationFile = CollectionEntry<'legislation'>;
export interface LegislationView {
  file: LegislationFile;
  stories: Article[]; // newest first
  keyDates: { date: Date; what: string; article?: Article }[];
}

/** Every tracked law with its stories and the key dates those stories give, latest activity first. */
export async function getLegislation(articles: Article[]): Promise<LegislationView[]> {
  const files = await getCollection('legislation');
  return files
    .map((file) => {
      const stories = articles.filter((a) => a.data.legislation.includes(file.id));
      const keyDates = [
        ...file.data.dates.map((d) => ({ ...d, article: undefined as Article | undefined })),
        ...stories.flatMap((a) => a.data.deadlines.map((d) => ({ ...d, article: a as Article | undefined }))),
      ]
        .sort((x, y) => x.date.getTime() - y.date.getTime())
        .filter((d, i, all) => all.findIndex((o) => o.date.getTime() === d.date.getTime() && o.what === d.what) === i);
      return { file, stories, keyDates };
    })
    .sort((a, b) => (b.stories[0]?.data.date.getTime() ?? 0) - (a.stories[0]?.data.date.getTime() ?? 0));
}

export type KeyDateKind = 'Applies' | 'Comment deadline' | 'Hearing or vote' | 'Other';
export interface KeyDate {
  id: string;
  date: Date;
  what: string;
  kind: KeyDateKind;
  area: 'EU' | 'UK' | 'US' | 'Other';
  /** The story the date comes from, or none when the date is set by the tracked law itself. */
  article?: Article;
  laws: LegislationFile[];
  /** Where the reader goes for more: the story, or the law's page in the tracker. */
  href: string;
  from: string;
}

const kindOf = (what: string): KeyDateKind =>
  /comment|consultation|feedback|submission|respond/i.test(what)
    ? 'Comment deadline'
    : /hearing|vote|ruling|judgment|plenary|trial|meeting|decision due/i.test(what)
      ? 'Hearing or vote'
      : /effect|force|appl|start|begin|commenc|in operation|compliance|deadline to comply|must/i.test(what)
        ? 'Applies'
        : 'Other';

const areaOf = (region = ''): KeyDate['area'] =>
  /\bEU\b|Europe|France|German|Spain|Ital|Nether|Dutch|Ireland|Sweden|Norway|Denmark|Belg|Austria|Poland|Croatia/i.test(region)
    ? 'EU'
    : /\bUK\b|United Kingdom|Britain/i.test(region)
      ? 'UK'
      : /\bUS\b|United States|California|Colorado|New York|Texas|Pennsylvania/i.test(region)
        ? 'US'
        : 'Other';

/** Every dated obligation, deadline, hearing and vote from our stories and tracked laws, earliest first, without repeats. */
export async function getKeyDates(articles: Article[]): Promise<KeyDate[]> {
  const files = await getCollection('legislation');
  const seen = new Set<string>();
  const fromLaws: KeyDate[] = files.flatMap((f) =>
    f.data.dates.map((d) => ({
      id: `${isoDate(d.date)}-${f.id}`.slice(0, 80),
      date: d.date,
      what: d.what,
      kind: kindOf(d.what),
      area: areaOf(f.data.jurisdiction),
      laws: [f],
      href: `/legislation/${f.id}/`,
      from: `${f.data.short}: official text`,
    })),
  );
  const fromStories: KeyDate[] = articles.flatMap((article) =>
    article.data.deadlines.map((d) => ({
      id: `${isoDate(d.date)}-${article.id}`.slice(0, 80),
      date: d.date,
      what: d.what,
      kind: kindOf(d.what),
      area: areaOf(article.data.region),
      article,
      laws: files.filter((f) => article.data.legislation.includes(f.id)),
      href: articleUrl(article),
      from: article.data.title,
    })),
  );
  // Dates from the law's own text come first, so a story repeating one does not double it.
  return [...fromLaws, ...fromStories]
    .sort((x, y) => x.date.getTime() - y.date.getTime())
    .filter((d) => {
      const key = `${isoDate(d.date)}|${d.what.toLowerCase()}`;
      const sameLawSameDay = d.laws.some((l) => seen.has(`${isoDate(d.date)}|law:${l.id}`));
      if (seen.has(key) || (d.article && sameLawSameDay)) return false;
      seen.add(key);
      if (!d.article) d.laws.forEach((l) => seen.add(`${isoDate(d.date)}|law:${l.id}`));
      return true;
    });
}
