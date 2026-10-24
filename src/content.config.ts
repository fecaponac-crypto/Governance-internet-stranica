import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';
import { CATEGORY_IDS, CONTENT_TYPES } from './data/site';

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

export const collections = { articles };
