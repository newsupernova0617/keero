import { posts, likes, comments, images } from '$lib/server/schema'
import { desc, sql, count, isNull } from 'drizzle-orm'
import type { PageServerLoad } from './$types'

export const load: PageServerLoad = async ({ locals }) => {
    const db = locals.db
    // 주간 베스트 (최근 7일, 좋아요 순)
    const weeklyBest = await db
        .select({
            id: posts.id,
            title: posts.title,
            site_name: posts.site_name,
            created_at: posts.created_at,
            like_count: sql<number>`(SELECT COUNT(*) FROM likes WHERE likes.post_id = posts.id)`.as('like_count'),
            comment_count: sql<number>`(SELECT COUNT(*) FROM comments WHERE comments.post_id = posts.id AND comments.is_deleted = 0)`.as('comment_count'),
        })
        .from(posts)
        .where(sql`posts.crawled_at > datetime('now', '-7 days') AND posts.related_post_id IS NULL`)
        .orderBy(desc(sql`like_count`))
        .limit(10)

    // 월간 베스트 (최근 30일, 좋아요 순)
    const monthlyBest = await db
        .select({
            id: posts.id,
            title: posts.title,
            site_name: posts.site_name,
            created_at: posts.created_at,
            like_count: sql<number>`(SELECT COUNT(*) FROM likes WHERE likes.post_id = posts.id)`.as('like_count'),
            comment_count: sql<number>`(SELECT COUNT(*) FROM comments WHERE comments.post_id = posts.id AND comments.is_deleted = 0)`.as('comment_count'),
        })
        .from(posts)
        .where(sql`posts.crawled_at > datetime('now', '-30 days') AND posts.related_post_id IS NULL`)
        .orderBy(desc(sql`like_count`))
        .limit(10)

    // 댓글 활발도 순위 (최근 7일)
    const mostDiscussed = await db
        .select({
            id: posts.id,
            title: posts.title,
            site_name: posts.site_name,
            created_at: posts.created_at,
            like_count: sql<number>`(SELECT COUNT(*) FROM likes WHERE likes.post_id = posts.id)`.as('like_count'),
            comment_count: sql<number>`(SELECT COUNT(*) FROM comments WHERE comments.post_id = posts.id AND comments.is_deleted = 0)`.as('comment_count'),
        })
        .from(posts)
        .where(sql`posts.crawled_at > datetime('now', '-7 days') AND posts.related_post_id IS NULL`)
        .orderBy(desc(sql`comment_count`))
        .limit(10)

    // 사이트별 통계
    const siteStats = await db
        .select({
            site_name: posts.site_name,
            total_posts: count(),
        })
        .from(posts)
        .where(isNull(posts.related_post_id))
        .groupBy(posts.site_name)
        .orderBy(desc(count()))

    // 전체 통계
    const totalStats = await db
        .select({
            total_posts: count(),
        })
        .from(posts)
        .where(isNull(posts.related_post_id))

    const totalLikes = await db.select({ count: count() }).from(likes)
    const totalComments = await db.select({ count: count() }).from(comments)
    const totalImages = await db.select({ count: count() }).from(images)

    // 최근 7일 신규 게시글 수
    const recentPosts = await db
        .select({ count: count() })
        .from(posts)
        .where(sql`posts.crawled_at > datetime('now', '-7 days') AND posts.related_post_id IS NULL`)

    return {
        weeklyBest,
        monthlyBest,
        mostDiscussed,
        siteStats,
        overview: {
            totalPosts: totalStats[0]?.total_posts || 0,
            totalLikes: totalLikes[0]?.count || 0,
            totalComments: totalComments[0]?.count || 0,
            totalImages: totalImages[0]?.count || 0,
            recentPosts: recentPosts[0]?.count || 0,
        }
    }
}
