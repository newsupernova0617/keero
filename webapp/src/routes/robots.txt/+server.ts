export async function GET({ url }) {
    const baseUrl = url.origin

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
