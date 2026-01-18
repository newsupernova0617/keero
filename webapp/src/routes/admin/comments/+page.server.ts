import { requireAdmin } from '$lib/server/auth'
import { comments, users, posts } from '$lib/server/schema'
import { eq, desc } from 'drizzle-orm'
import { fail } from '@sveltejs/kit'
import type { PageServerLoad, Actions } from './$types'

export const load: PageServerLoad = async (event) => {
    const db = event.locals.db
	await requireAdmin(event)

	// 모든 댓글 조회 (사용자 및 게시글 정보 포함)
	const allComments = await db
		.select({
			id: comments.id,
			content: comments.content,
			created_at: comments.created_at,
			is_deleted: comments.is_deleted,
			post_id: comments.post_id,
			post_title: posts.title,
			user_id: comments.user_id,
			user_email: users.email,
			user_display_name: users.display_name
		})
		.from(comments)
		.leftJoin(users, eq(comments.user_id, users.id))
		.leftJoin(posts, eq(comments.post_id, posts.id))
		.orderBy(desc(comments.id))
		.limit(100)

	return {
		comments: allComments
	}
}

export const actions: Actions = {
	delete: async (event) => {
		const db = event.locals.db
		await requireAdmin(event)

		const formData = await event.request.formData()
		const commentId = formData.get('comment_id')?.toString()

		if (!commentId) {
			return fail(400, { error: '잘못된 요청입니다.' })
		}

		// Soft delete
		await db
			.update(comments)
			.set({
				is_deleted: true,
				content: '관리자에 의해 삭제된 댓글입니다.'
			})
			.where(eq(comments.id, parseInt(commentId)))

		return { success: true }
	}
}
