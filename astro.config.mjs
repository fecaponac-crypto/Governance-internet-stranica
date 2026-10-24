// @ts-check
import { defineConfig } from 'astro/config';
import { fileURLToPath } from 'node:url';
import sitemap from '@astrojs/sitemap';
import * as pagefind from 'pagefind';

/**
 * Builds the Pagefind search index as part of `astro build`, so search works
 * whatever build command the host runs.
 * @returns {import('astro').AstroIntegration}
 */
function pagefindIndex() {
  return {
    name: 'pagefind-index',
    hooks: {
      'astro:build:done': async ({ dir, logger }) => {
        const site = fileURLToPath(dir);
        const { index, errors } = await pagefind.createIndex({});
        if (!index) throw new Error(`Pagefind: ${errors.join(', ')}`);
        const added = await index.addDirectory({ path: site });
        if (added.errors.length) throw new Error(`Pagefind: ${added.errors.join(', ')}`);
        await index.writeFiles({ outputPath: `${site}pagefind` });
        await pagefind.close();
        logger.info(`Indexed ${added.page_count} pages`);
      },
    },
  };
}

export default defineConfig({
  site: 'https://datagovernancesignal.com',
  trailingSlash: 'always',
  integrations: [sitemap(), pagefindIndex()],
});
