import type { APIRoute, GetStaticPaths } from 'astro';
import { getArticles, type Article } from '../../../utils/articles';
import { renderCard, THUMB_WIDTH } from '../../../utils/card';

export const getStaticPaths = (async () => {
  const articles = await getArticles();
  return articles.map((article) => ({ params: { slug: article.id }, props: { article } }));
}) satisfies GetStaticPaths;

export const GET: APIRoute<{ article: Article }> = async ({ props }) => {
  const png = await renderCard(props.article, THUMB_WIDTH);
  return new Response(new Uint8Array(png), { headers: { 'Content-Type': 'image/png' } });
};
