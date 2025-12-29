import { db } from '$lib/server/db'
import { images } from '$lib/server/schema'
import { sql, eq } from 'drizzle-orm'
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
}

export const load: PageServerLoad = async ({ url }) => {
    const query = url.searchParams.get('q')?.trim()

    if (!query) {
        return {
            query: '',
            results: []
        }
    }

    try {
        // FTS5 전문 검색 (훨씬 빠르고 정확함)
        const searchResults = await db.all<SearchResult>(sql`
			SELECT 
				posts.id,
				posts.site_name,
				posts.title,
				posts.content,
				posts.source_url,
				posts.created_at,
				posts.crawled_at,
				(SELECT COUNT(*) FROM images WHERE images.post_id = posts.id) as image_count
			FROM posts_fts
			JOIN posts ON posts_fts.rowid = posts.id
			WHERE posts.related_post_id IS NULL
			AND posts_fts MATCH ${query}
			ORDER BY posts.id DESC
			LIMIT 50
		`)

        // 각 게시글의 첫 번째 이미지 가져오기 (Drizzle ORM 사용)
        const resultsWithImages = await Promise.all(
            searchResults.map(async (post) => {
                const firstImage = await db
                    .select()
                    .from(images)
                    .where(eq(images.post_id, post.id))
                    .orderBy(images.order_index)
                    .limit(1)

                return {
                    ...post,
                    thumbnail: firstImage[0]?.r2_url || null
                }
            })
        )

        return {
            query,
            results: resultsWithImages
        }
    } catch (error) {
        console.error('Search error:', error)
        return {
            query,
            results: []
        }
    }
}
