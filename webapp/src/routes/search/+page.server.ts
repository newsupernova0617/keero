import { sql } from 'drizzle-orm'
import type { PageServerLoad } from './$types'

type SearchResult = {
    id: number
    site_name: string
    title: string
    content: string
    source_url: string
    created_at: string
    crawled_at: string
    image_count: number
    thumbnail: string | null
}

export const load: PageServerLoad = async ({ url, locals }) => {
    const db = locals.db
    const query = url.searchParams.get('q')?.trim()

    if (!query) {
        return {
            query: '',
            results: []
        }
    }

    try {
        // FTS5 전문 검색어 정제 (특수문자 제거 및 부분 일치 지원)
        // 여러 단어인 경우 각각 prefix search(*)를 적용하고 AND로 결합
        const sanitizedQuery = query
            .replace(/[()"'*]/g, ' ')
            .trim()
            .split(/\s+/)
            .filter(Boolean)
            .map(word => `${word}*`)
            .join(' AND ')

        if (!sanitizedQuery) {
            return { query, results: [] }
        }

        // FTS5 전문 검색 (Join 및 서브쿼리로 한 번에 썸네일까지 조회 - N+1 해결)
        const results = await db.all<SearchResult>(sql`
			SELECT 
				posts.id,
				posts.site_name,
				posts.title,
				posts.content,
				posts.source_url,
				posts.created_at,
				posts.crawled_at,
				(SELECT COUNT(*) FROM images WHERE images.post_id = posts.id) as image_count,
				(SELECT r2_url FROM images WHERE images.post_id = posts.id ORDER BY order_index ASC LIMIT 1) as thumbnail
			FROM posts_fts
			JOIN posts ON posts_fts.rowid = posts.id
			WHERE posts.related_post_id IS NULL
			AND posts_fts MATCH ${sanitizedQuery}
			ORDER BY posts.id DESC
			LIMIT 50
		`)

        return {
            query,
            results
        }
    } catch (error) {
        console.error('Search error:', error)
        return {
            query,
            results: []
        }
    }
}

