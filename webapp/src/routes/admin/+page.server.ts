import { requireAdmin } from '$lib/server/auth'
import { db } from '$lib/server/db'
import { posts, comments, users } from '$lib/server/schema'
import { sql } from 'drizzle-orm'
import type { PageServerLoad } from './$types'

export const load: PageServerLoad = async (event) => {
    await requireAdmin(event)

    // 통계 데이터 조회
    const totalPosts = await db
        .select({ count: sql<number>`count(*)` })
        .from(posts)
        .then(result => result[0]?.count || 0)

    const totalComments = await db
        .select({ count: sql<number>`count(*)` })
        .from(comments)
        .then(result => result[0]?.count || 0)

    const totalUsers = await db
        .select({ count: sql<number>`count(*)` })
        .from(users)
        .then(result => result[0]?.count || 0)

    // 최근 게시글 (5개)
    const recentPosts = await db
        .select({
            id: posts.id,
            title: posts.title,
            site_name: posts.site_name,
            created_at: posts.created_at
        })
        .from(posts)
        .orderBy(sql`${posts.id} DESC`)
        .limit(5)

    // 최근 댓글 (5개)
    const recentComments = await db
        .select({
            id: comments.id,
            content: comments.content,
            created_at: comments.created_at,
            user_display_name: users.display_name,
            post_id: comments.post_id
        })
        .from(comments)
        .leftJoin(users, sql`${comments.user_id} = ${users.id}`)
        .orderBy(sql`${comments.id} DESC`)
        .limit(5)

    return {
        stats: {
            totalPosts,
            totalComments,
            totalUsers
        },
        recentPosts,
        recentComments
    }
}
