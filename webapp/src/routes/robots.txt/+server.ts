import { env } from '$env/dynamic/public'

export async function GET({ url }) {
    // PUBLIC_BASE_URL 우선 사용 (없으면 origin 사용)
    let baseUrl = env.PUBLIC_BASE_URL || url.origin

    // 잘못된 Railway 주소나 기본 pages.dev 주소인 경우 공식 도메인으로 강제 고정
    if (!baseUrl || baseUrl.includes('railway.app') || baseUrl.includes('pages.dev')) {
        baseUrl = 'https://keero.site'
    }

    if (baseUrl && !baseUrl.startsWith('http://') && !baseUrl.startsWith('https://')) {
        baseUrl = `https://${baseUrl}`
    }
    // trailing slash 제거
    baseUrl = baseUrl.replace(/\/$/, '')

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
