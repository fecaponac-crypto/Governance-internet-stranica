import rss from '@astrojs/rss';
import type { APIContext } from 'astro';
import { SITE } from '../data/site';
import { getArticles, articleUrl } from '../utils/articles';

export async function GET(context: APIContext) {
  const articles = await getArticles();
  return rss({
    title: SITE.name,
    description: SITE.description,
    site: context.site ?? SITE.url,
    items: articles.map((a) => ({
      title: a.data.title,
      pubDate: a.data.date,
      description: `${a.data.dek} Why it matters: ${a.data.whyItMatters}`,
      link: articleUrl(a),
      categories: a.data.categories,
    })),
  });
}
