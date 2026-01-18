import { posts, images } from '$lib/server/schema'
import { desc, isNull, eq, and } from 'drizzle-orm'
import { env } from '$env/dynamic/public'

/**
 * Google Search Console 최적화 사이트맵 생성기
 */
export async function GET({ url, locals }) {
    const db = locals.db
    if (!db) {
        return new Response('Database not available', { status: 500 })
    }

    try {
        // 최신 게시글 5000개 조회 (D1 성능 고려)
        const allPosts = await db
            .select({
                id: posts.id,
                title: posts.title,
                crawled_at: posts.crawled_at,
                imageUrl: images.r2_url
            })
            .from(posts)
            .leftJoin(images, and(eq(posts.id, images.post_id), eq(images.order_index, 0)))
            .where(isNull(posts.related_post_id))
            .orderBy(desc(posts.id))
            .limit(5000)

        // 도메인 결정 및 보정
        let baseUrl = env.PUBLIC_BASE_URL || url.origin
        if (!baseUrl || baseUrl.includes('railway.app') || baseUrl.includes('pages.dev') || baseUrl.includes('localhost')) {
            baseUrl = 'https://keero.site'
        }
        if (baseUrl && !baseUrl.startsWith('http')) {
            baseUrl = `https://${baseUrl}`
        }
        baseUrl = baseUrl.replace(/\/$/, '')

        // 날짜 포맷팅 (ISO 8601: YYYY-MM-DD)
        const formatDate = (dateStr: string | null) => {
            if (!dateStr) return new Date().toISOString().split('T')[0]
            try {
                // DB에 저장된 형식이 다를 수 있으므로 안전하게 처리
                const d = new Date(dateStr)
                return isNaN(d.getTime()) ? new Date().toISOString().split('T')[0] : d.toISOString().split('T')[0]
            } catch {
                return new Date().toISOString().split('T')[0]
            }
        }

        const now = formatDate(null)

        const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"
        xmlns:mobile="http://www.google.com/schemas/sitemap-mobile/1.0">
  <!-- 메인 페이지 -->
  <url>
    <loc>${baseUrl}/</loc>
    <lastmod>${now}</lastmod>
    <changefreq>always</changefreq>
    <priority>1.0</priority>
  </url>

  <!-- 주요 서비스 페이지 -->
  <url>
    <loc>${baseUrl}/highlights/weekly</loc>
    <changefreq>daily</changefreq>
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
  <url>
    <loc>${baseUrl}/stats</loc>
    <changefreq>daily</changefreq>
    <priority>0.7</priority>
  </url>

  <!-- 법적 및 안내 페이지 (E-E-A-T 점수 향상) -->
  <url><loc>${baseUrl}/about</loc><changefreq>monthly</changefreq><priority>0.5</priority></url>
  <url><loc>${baseUrl}/contact</loc><changefreq>monthly</changefreq><priority>0.5</priority></url>
  <url><loc>${baseUrl}/privacy</loc><changefreq>yearly</changefreq><priority>0.3</priority></url>
  <url><loc>${baseUrl}/terms</loc><changefreq>yearly</changefreq><priority>0.3</priority></url>
  <url><loc>${baseUrl}/dmca</loc><changefreq>yearly</changefreq><priority>0.3</priority></url>
  <url><loc>${baseUrl}/faq</loc><changefreq>monthly</changefreq><priority>0.5</priority></url>

  <!-- 최신 게시글 5000개 -->
${allPosts
                .map(
                    (post) => `  <url>
    <loc>${baseUrl}/post/${post.id}</loc>
    <lastmod>${formatDate(post.crawled_at)}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.6</priority>${post.imageUrl ? `
    <image:image>
      <image:loc>${post.imageUrl.startsWith('http') ? post.imageUrl : baseUrl + post.imageUrl}</image:loc>
      <image:title><![CDATA[${post.title}]]></image:title>
    </image:image>` : ''}
  </url>`
                )
                .join('\n')}
</urlset>`

        return new Response(xml, {
            headers: {
                'Content-Type': 'application/xml; charset=utf-8',
                'Cache-Control': 'public, max-age=3600, s-maxage=3600',
                'X-Content-Type-Options': 'nosniff'
            }
        })
    } catch (error) {
        console.error('Sitemap generation error:', error)
        return new Response('Error generating sitemap', { status: 500 })
    }
}

