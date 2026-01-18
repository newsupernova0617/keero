import { comments, users, posts, likes } from '$lib/server/schema'
import { desc, sql, eq } from 'drizzle-orm'
import type { PageServerLoad } from './$types'

export const load: PageServerLoad = async ({ locals }) => {
    const db = locals.db
	// 좋아요 많은 댓글 TOP 100 조회
	const bestComments = await db
		.select({
			id: comments.id,
			content: comments.content,
			createdAt: comments.created_at,
			postId: posts.id,
			postTitle: posts.title,
			postSiteName: posts.site_name,
			userName: users.display_name,
			userEmail: users.email,
			likeCount: sql<number>`(SELECT COUNT(*) FROM ${likes} WHERE ${likes.comment_id} = ${comments.id})`.as(
				'like_count'
			)
		})
		.from(comments)
		.leftJoin(users, eq(comments.user_id, users.id))
		.leftJoin(posts, eq(comments.post_id, posts.id))
		.where(eq(comments.is_deleted, false))
		.orderBy(desc(sql`like_count`))
		.limit(100)

	// 댓글 통계
	const totalComments = bestComments.length
	const totalLikes = bestComments.reduce((sum, c) => sum + (c.likeCount || 0), 0)
	const avgLikes = totalComments > 0 ? Math.round(totalLikes / totalComments) : 0

	return {
		comments: bestComments.map((c) => ({
			...c,
			displayName: c.userName || c.userEmail?.split('@')[0] || '익명'
		})),
		stats: {
			totalComments,
			totalLikes,
			avgLikes
		}
	}
}
