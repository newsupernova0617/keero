import { db } from '$lib/server/db'
import { posts } from '$lib/server/schema'
import { desc, isNull } from 'drizzle-orm'
import { PUBLIC_BASE_URL } from '$env/static/public'

export async function GET() {
    try {
        // 최근 1000개 게시글 조회
        const allPosts = await db
            .select({
                id: posts.id,
                crawled_at: posts.crawled_at
            })
            .from(posts)
            .where(isNull(posts.related_post_id))
            .orderBy(desc(posts.id))
            .limit(1000)

        const baseUrl = PUBLIC_BASE_URL || 'http://localhost:5173'

        const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>${baseUrl}/</loc>
    <changefreq>hourly</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>${baseUrl}/search</loc>
    <changefreq>daily</changefreq>
    <priority>0.8</priority>
  </url>
${allPosts
                .map(
                    (post) => `  <url>
    <loc>${baseUrl}/post/${post.id}</loc>
    <lastmod>${post.crawled_at}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>`
                )
                .join('\n')}
</urlset>`

        return new Response(xml, {
            headers: {
                'Content-Type': 'application/xml',
                'Cache-Control': 'max-age=3600' // 1시간 캐시
            }
        })
    } catch (error) {
        console.error('Sitemap generation error:', error)
        return new Response('Error generating sitemap', { status: 500 })
    }
}
