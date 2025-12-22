import { db } from '$lib/server/db'
import { posts, images } from '$lib/server/schema'
import { sql } from 'drizzle-orm'
import type { PageServerLoad } from './$types'

export const load: PageServerLoad = async ({ url }) => {
    const query = url.searchParams.get('q')?.trim()

    if (!query) {
        return {
            query: '',
            results: []
        }
    }

    try {
        // FTS5 검색 쿼리
        const searchResults = await db.all<any>(sql`
			SELECT 
				posts.id,
				posts.site_name,
				posts.title,
				posts.content,
				posts.source_url,
				posts.created_at,
				posts.crawled_at,
				(SELECT COUNT(*) FROM images WHERE images.post_id = posts.id) as image_count
			FROM posts
			WHERE posts.related_post_id IS NULL
			AND (
				posts.title LIKE ${'%' + query + '%'}
				OR posts.content LIKE ${'%' + query + '%'}
			)
			ORDER BY posts.id DESC
			LIMIT 50
		`)

        // 각 게시글의 첫 번째 이미지 가져오기
        const resultsWithImages = await Promise.all(
            searchResults.map(async (post: any) => {
                const firstImage = await db
                    .select()
                    .from(images)
                    .where(sql`${images.post_id} = ${post.id}`)
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
