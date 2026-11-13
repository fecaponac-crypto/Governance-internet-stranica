import { categoryById } from '../data/site';
import { areaOf, enforcementCases, getArticles, getKeyDates, getLegislation, isoDate, type Article, type CaseStep, type KeyDate, type LegislationFile } from './articles';

export interface MonthReview {
  key: string; // YYYY-MM
  label: string; // October 2026
  complete: boolean; // false while the month is still running
  stories: Article[]; // newest first
  top: Article[];
  byTopic: { label: string; count: number }[];
  byRegion: { label: string; count: number }[];
  steps: CaseStep[]; // enforcement steps dated in the month, newest first
  amounts: { amount: number; currency: string }[];
  laws: { file: LegislationFile; stories: Article[] }[];
  lawDates: KeyDate[]; // dates set by a tracked law that fell in the month
  ahead: KeyDate[]; // key dates in the month that follows
}

const monthKey = (d: Date) => d.toISOString().slice(0, 7);
const monthLabel = (key: string) =>
  new Date(`${key}-01T00:00:00Z`).toLocaleDateString('en-GB', { month: 'long', year: 'numeric', timeZone: 'UTC' });
const nextMonth = (key: string) => {
  const d = new Date(`${key}-01T00:00:00Z`);
  d.setUTCMonth(d.getUTCMonth() + 1);
  return monthKey(d);
};
const tally = (labels: string[]) =>
  [...labels.reduce((m, l) => m.set(l, (m.get(l) ?? 0) + 1), new Map<string, number>())]
    .map(([label, count]) => ({ label, count }))
    .sort((a, b) => b.count - a.count || a.label.localeCompare(b.label));

const regionOf = (region = '') => (/global|worldwide|international/i.test(region) ? 'Global' : areaOf(region) === 'Other' ? 'Other countries' : areaOf(region));

/** One review per month in which we published, built only from the stories and the two trackers. Newest first. */
export async function getMonthReviews(now = new Date()): Promise<MonthReview[]> {
  const articles = await getArticles();
  const keyDates = await getKeyDates(articles);
  const laws = await getLegislation(articles);
  const steps = enforcementCases(articles).flatMap((c) => c.steps);
  const months = [...new Set(articles.map((a) => monthKey(a.data.date)))].filter((k) => k <= monthKey(now)).sort().reverse();

  return months.map((key) => {
    const stories = articles.filter((a) => monthKey(a.data.date) === key);
    const monthSteps = steps.filter((s) => monthKey(s.e.date) === key).sort((a, b) => b.e.date.getTime() - a.e.date.getTime());
    const sums = new Map<string, number>();
    for (const s of monthSteps) if (s.e.amount && s.e.currency) sums.set(s.e.currency, (sums.get(s.e.currency) ?? 0) + s.e.amount);
    return {
      key,
      label: monthLabel(key),
      complete: key < monthKey(now),
      stories,
      top: [...stories].sort((a, b) => b.data.importance - a.data.importance || b.data.date.getTime() - a.data.date.getTime()).slice(0, 5),
      byTopic: tally(stories.flatMap((a) => a.data.categories.map((c) => categoryById(c).short))),
      byRegion: tally(stories.map((a) => regionOf(a.data.region))),
      steps: monthSteps,
      amounts: [...sums].map(([currency, amount]) => ({ amount, currency })).sort((a, b) => b.amount - a.amount),
      laws: laws
        .map((l) => ({ file: l.file, stories: l.stories.filter((a) => monthKey(a.data.date) === key) }))
        .filter((l) => l.stories.length)
        .sort((a, b) => b.stories.length - a.stories.length),
      lawDates: keyDates.filter((d) => !d.article && monthKey(d.date) === key),
      ahead: keyDates.filter((d) => monthKey(d.date) === nextMonth(key) && (key < monthKey(now) || isoDate(d.date) >= isoDate(now))),
    };
  });
}

export interface WeekReview {
  stories: number;
  steps: CaseStep[];
  amounts: { amount: number; currency: string }[];
  laws: LegislationFile[];
  dates: KeyDate[]; // key dates in the 30 days from the column date
}

/** The seven days before a Monday column, counted from the stories and the two trackers, and the dates that follow. */
export async function getWeekReview(monday: Date): Promise<WeekReview> {
  const articles = await getArticles();
  const start = monday.getTime() - 7 * 864e5;
  const inWeek = (d: Date) => d.getTime() >= start && d.getTime() < monday.getTime();
  const stories = articles.filter((a) => inWeek(a.data.date));
  const steps = enforcementCases(articles)
    .flatMap((c) => c.steps)
    .filter((s) => inWeek(s.e.date))
    .sort((a, b) => b.e.date.getTime() - a.e.date.getTime());
  const sums = new Map<string, number>();
  for (const s of steps) if (s.e.amount && s.e.currency) sums.set(s.e.currency, (sums.get(s.e.currency) ?? 0) + s.e.amount);
  const ids = new Set(stories.flatMap((a) => a.data.legislation));
  return {
    stories: stories.length,
    steps,
    amounts: [...sums].map(([currency, amount]) => ({ amount, currency })).sort((a, b) => b.amount - a.amount),
    laws: (await getLegislation(articles)).map((l) => l.file).filter((f) => ids.has(f.id)),
    dates: (await getKeyDates(articles)).filter((d) => d.date.getTime() >= monday.getTime() && d.date.getTime() < monday.getTime() + 30 * 864e5),
  };
}
