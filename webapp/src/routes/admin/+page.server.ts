import { db } from '$lib/server/db'
import { posts, users, comments } from '$lib/server/schema'
import { sql } from 'drizzle-orm'
import type { PageServerLoad } from './$types'

export const load: PageServerLoad = async () => {
    // 통계 조회
    const stats = {
        totalPosts: 0,
        totalUsers: 0,
        totalComments: 0,
        recentPosts: [] as any[]
    }

    try {
        // 게시글 수
        const postCount = await db.all<{ count: number }>(sql`SELECT COUNT(*) as count FROM posts WHERE related_post_id IS NULL`)
        stats.totalPosts = postCount[0]?.count || 0

        // 사용자 수  
        const userCount = await db.all<{ count: number }>(sql`SELECT COUNT(*) as count FROM users`)
        stats.totalUsers = userCount[0]?.count || 0

        // 댓글 수
        const commentCount = await db.all<{ count: number }>(sql`SELECT COUNT(*) as count FROM comments`)
        stats.totalComments = commentCount[0]?.count || 0

        // 최근 게시글
        stats.recentPosts = await db
            .select()
            .from(posts)
            .orderBy(sql`${posts.id} DESC`)
            .limit(10)
    } catch (error) {
        console.error('Admin stats error:', error)
    }

    return stats
}
