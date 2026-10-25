import { defineCollection } from 'astro:content';
import { file, glob } from 'astro/loaders';
import { z } from 'astro/zod';
import { CATEGORY_IDS, COLUMN, CONTENT_TYPES, PREDICTION_STATUSES } from './data/site';

const articles = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/articles' }),
  schema: z.object({
    title: z.string(),
    // Original publication date of the news (not our publication date).
    date: z.coerce.date(),
    // One-sentence standfirst shown on cards and under the headline.
    dek: z.string(),
    whyItMatters: z.string(),
    categories: z.array(z.enum(CATEGORY_IDS)).min(1),
    whoShouldCare: z.array(z.string()).min(1),
    importance: z.number().int().min(1).max(5),
    type: z.enum(CONTENT_TYPES),
    region: z.string().optional(),
    sources: z
      .array(
        z.object({
          name: z.string(),
          title: z.string(),
          url: z.url(),
          primary: z.boolean().default(false),
        }),
      )
      .min(1),
    // Where the editor found the story (e.g. a newsletter); credited, not used as the source.
    via: z.object({ name: z.string(), url: z.url() }).optional(),
    related: z.array(z.string()).default([]),
    // News card: the key fact in large type plus a short caption.
    card: z
      .object({
        figure: z.string().max(22),
        caption: z.string().max(90),
      })
      .optional(),
    // Sample content created for the preview; hidden once preview mode ends.
    sample: z.boolean().default(false),
    draft: z.boolean().default(false),
  }),
});

// The Monday Signal: the editor's weekly column (one file per Monday, named YYYY-MM-DD.md).
const columns = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/columns' }),
  schema: z.object({
    title: z.string(),
    date: z.coerce.date(),
    dek: z.string(),
    author: z.string().default(COLUMN.author),
    draft: z.boolean().default(false),
  }),
});

const link = z.object({ title: z.string(), url: z.url() });

const predictions = defineCollection({
  loader: file('data/predictions.yaml'),
  schema: z
    .object({
      claim: z.string(),
      by: z.string(),
      role: z.string().optional(),
      ours: z.boolean().default(false),
      quote: z.string().optional(),
      source: link,
      made: z.coerce.date(),
      due: z.coerce.date(),
      confidence: z.number().int().min(1).max(99).optional(),
      status: z.enum(PREDICTION_STATUSES).default('open'),
      resolved: z.coerce.date().optional(),
      evidence: link.optional(),
      note: z.string().optional(),
      categories: z.array(z.enum(CATEGORY_IDS)).default([]),
    })
    .refine((p) => !p.ours || p.confidence !== undefined, { message: 'our predictions need a confidence' })
    .refine((p) => p.ours || !!p.quote, { message: "others' predictions need the quoted words" })
    .refine((p) => p.status === 'open' || (p.resolved && p.evidence), {
      message: 'a judged prediction needs resolved and evidence',
    }),
});

export const collections = { articles, columns, predictions };
