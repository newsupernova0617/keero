import { posts } from '$lib/server/schema'
import { desc, isNull } from 'drizzle-orm'
import { env } from '$env/dynamic/public'

export async function GET({ url, locals }) {
    const db = locals.db
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

        // PUBLIC_BASE_URL 우선 사용 (Railway 배포 대비)
        // https:// 프로토콜이 없으면 자동 추가
        let baseUrl = env.PUBLIC_BASE_URL || url.origin
        if (baseUrl && !baseUrl.startsWith('http://') && !baseUrl.startsWith('https://')) {
            baseUrl = `https://${baseUrl}`
        }

        const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>${baseUrl}/</loc>
    <changefreq>hourly</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>${baseUrl}/about</loc>
    <changefreq>monthly</changefreq>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>${baseUrl}/contact</loc>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>${baseUrl}/faq</loc>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>${baseUrl}/privacy</loc>
    <changefreq>yearly</changefreq>
    <priority>0.6</priority>
  </url>
  <url>
    <loc>${baseUrl}/terms</loc>
    <changefreq>yearly</changefreq>
    <priority>0.6</priority>
  </url>
  <url>
    <loc>${baseUrl}/dmca</loc>
    <changefreq>yearly</changefreq>
    <priority>0.5</priority>
  </url>
  <url>
    <loc>${baseUrl}/stats</loc>
    <changefreq>daily</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>${baseUrl}/highlights/weekly</loc>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>${baseUrl}/best-comments</loc>
    <changefreq>daily</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>${baseUrl}/search</loc>
    <changefreq>daily</changefreq>
    <priority>0.7</priority>
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
