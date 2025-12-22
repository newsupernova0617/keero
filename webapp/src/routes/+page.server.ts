import { db } from '$lib/server/db'
import { posts, images } from '$lib/server/schema'
import { desc, isNull, sql } from 'drizzle-orm'
import type { PageServerLoad } from './$types'

export const load: PageServerLoad = async ({ url }) => {
    // 페이지네이션 파라미터
    const page = parseInt(url.searchParams.get('page') || '1')
    const limit = 20
    const offset = (page - 1) * limit

    // 전체 게시글 수 조회
    const totalCountResult = await db
        .select({ count: sql<number>`count(*)` })
        .from(posts)
        .where(isNull(posts.related_post_id))
    
    const totalCount = totalCountResult[0]?.count || 0
    const totalPages = Math.ceil(totalCount / limit)

    // 원본 게시글만 조회 (중복 제외)
    const allPosts = await db
        .select({
            id: posts.id,
            site_name: posts.site_name,
            title: posts.title,
            content: posts.content,
            source_url: posts.source_url,
            created_at: posts.created_at,
            crawled_at: posts.crawled_at,
            // 이미지 개수 서브쿼리
            image_count: sql<number>`(SELECT COUNT(*) FROM images WHERE images.post_id = posts.id)`
        })
        .from(posts)
        .where(isNull(posts.related_post_id))
        .orderBy(desc(posts.id))
        .limit(limit)
        .offset(offset)

    // 각 게시글의 첫 번째 이미지 가져오기
    const postsWithImages = await Promise.all(
        allPosts.map(async (post) => {
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
        posts: postsWithImages,
        pagination: {
            page,
            totalPages,
            totalCount,
            hasNext: page < totalPages,
            hasPrev: page > 1
        }
    }
}
