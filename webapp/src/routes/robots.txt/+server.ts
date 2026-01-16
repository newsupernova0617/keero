import { env } from '$env/dynamic/public'

export async function GET({ url }) {
    // PUBLIC_BASE_URL 우선 사용 (Railway 배포 대비)
    // https:// 프로토콜이 없으면 자동 추가
    let baseUrl = env.PUBLIC_BASE_URL || url.origin
    if (baseUrl && !baseUrl.startsWith('http://') && !baseUrl.startsWith('https://')) {
        baseUrl = `https://${baseUrl}`
    }

    const robotsTxt = `User-agent: *
Allow: /
Disallow: /admin/
Disallow: /auth/

# Sitemap
Sitemap: ${baseUrl}/sitemap.xml

# Crawl-delay for polite crawling
Crawl-delay: 1
`

    return new Response(robotsTxt, {
        headers: {
            'Content-Type': 'text/plain',
            'Cache-Control': 'max-age=86400' // 24시간 캐시
        }
    })
}
