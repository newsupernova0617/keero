import { requireAuth } from '$lib/server/auth'
import { comments, likes, bookmarks, posts, users } from '$lib/server/schema'
import { eq, sql } from 'drizzle-orm'
import type { PageServerLoad } from './$types'

export const load: PageServerLoad = async (event) => {
    const db = event.locals.db
    const { user } = await requireAuth(event)

    // DB에서 사용자 정보 조회
    const dbUser = await db
        .select()
        .from(users)
        .where(eq(users.supabase_id, user.id))
        .limit(1)

    if (!dbUser || dbUser.length === 0) {
        return {
            stats: {
                totalComments: 0,
                totalLikes: 0,
                totalBookmarks: 0
            },
            recentComments: [],
            likedPosts: [],
            bookmarkedPosts: []
        }
    }

    const userId = dbUser[0].id

    // 통계 조회
    const totalComments = await db
        .select({ count: sql<number>`count(*)` })
        .from(comments)
        .where(eq(comments.user_id, userId))
        .then(result => result[0]?.count || 0)

    const totalLikes = await db
        .select({ count: sql<number>`count(*)` })
        .from(likes)
        .where(sql`${likes.user_id} = ${userId} AND ${likes.post_id} IS NOT NULL`)
        .then(result => result[0]?.count || 0)

    const totalBookmarks = await db
        .select({ count: sql<number>`count(*)` })
        .from(bookmarks)
        .where(eq(bookmarks.user_id, userId))
        .then(result => result[0]?.count || 0)

    // 최근 댓글 (5개)
    const recentComments = await db
        .select({
            id: comments.id,
            content: comments.content,
            created_at: comments.created_at,
            post_id: comments.post_id,
            post_title: posts.title
        })
        .from(comments)
        .leftJoin(posts, eq(comments.post_id, posts.id))
        .where(eq(comments.user_id, userId))
        .orderBy(sql`${comments.id} DESC`)
        .limit(5)

    // 좋아요한 게시글 (5개)
    const likedPosts = await db
        .select({
            id: posts.id,
            title: posts.title,
            site_name: posts.site_name,
            created_at: posts.created_at,
            liked_at: likes.created_at
        })
        .from(likes)
        .leftJoin(posts, eq(likes.post_id, posts.id))
        .where(sql`${likes.user_id} = ${userId} AND ${likes.post_id} IS NOT NULL`)
        .orderBy(sql`${likes.id} DESC`)
        .limit(5)

    // 북마크한 게시글 (5개)
    const bookmarkedPosts = await db
        .select({
            id: posts.id,
            title: posts.title,
            site_name: posts.site_name,
            created_at: posts.created_at,
            bookmarked_at: bookmarks.created_at
        })
        .from(bookmarks)
        .leftJoin(posts, eq(bookmarks.post_id, posts.id))
        .where(eq(bookmarks.user_id, userId))
        .orderBy(sql`${bookmarks.id} DESC`)
        .limit(5)

    return {
        stats: {
            totalComments,
            totalLikes,
            totalBookmarks
        },
        recentComments,
        likedPosts,
        bookmarkedPosts
    }
}
