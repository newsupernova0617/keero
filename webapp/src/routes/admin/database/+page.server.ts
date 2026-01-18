import { requireAdmin } from '$lib/server/auth'
import { posts, comments, users } from '$lib/server/schema'
import { sql, desc } from 'drizzle-orm'
import { error } from '@sveltejs/kit'
import type { PageServerLoad, Actions } from './$types'

export const load: PageServerLoad = async (event) => {
    const db = event.locals.db
	await requireAdmin(event)

	// 테이블별 통계
	const [postStats] = await db
		.select({
			total: sql<number>`count(*)`,
			sites: sql<number>`count(distinct ${posts.site_name})`
		})
		.from(posts)

	const [commentStats] = await db
		.select({
			total: sql<number>`count(*)`
		})
		.from(comments)

	const [userStats] = await db
		.select({
			total: sql<number>`count(*)`
		})
		.from(users)

	// 최근 게시글 (상세)
	const recentPosts = await db
		.select({
			id: posts.id,
			title: posts.title,
			site_name: posts.site_name,
			created_at: posts.created_at,
			crawled_at: posts.crawled_at
		})
		.from(posts)
		.orderBy(desc(posts.crawled_at))
		.limit(20)

	// 사이트별 게시글 수
	const postsBySite = await db
		.select({
			site_name: posts.site_name,
			count: sql<number>`count(*)`
		})
		.from(posts)
		.groupBy(posts.site_name)
		.orderBy(desc(sql<number>`count(*)`))

	return {
		stats: {
			posts: postStats,
			comments: commentStats,
			users: userStats
		},
		recentPosts,
		postsBySite
	}
}

export const actions: Actions = {
	// 게시글 삭제
	deletePost: async (event) => {
        const db = event.locals.db
        await requireAdmin(event)
		const { request } = event

		const formData = await request.formData()
		const postId = formData.get('postId')

		if (!postId) {
			throw error(400, '게시글 ID가 필요합니다')
		}

		// FOREIGN KEY constraint 해결: 연관 데이터 먼저 삭제
		// 1. 댓글 삭제
		await db.delete(comments).where(sql`${comments.post_id} = ${postId}`)
		
		// 2. 이미지 삭제 (있다면)
		try {
			const { images } = await import('$lib/server/schema')
			await db.delete(images).where(sql`${images.post_id} = ${postId}`)
		} catch {
			// images 테이블이 없으면 무시
		}
		
		// 3. 좋아요 삭제 (있다면)
		try {
			const { likes } = await import('$lib/server/schema')
			await db.delete(likes).where(sql`${likes.post_id} = ${postId}`)
		} catch {
			// likes 테이블이 없으면 무시
		}
		
		// 4. 북마크 삭제 (있다면)
		try {
			const { bookmarks } = await import('$lib/server/schema')
			await db.delete(bookmarks).where(sql`${bookmarks.post_id} = ${postId}`)
		} catch {
			// bookmarks 테이블이 없으면 무시
		}
		
		// 5. 신고 삭제 (있다면)
		try {
			const { reports } = await import('$lib/server/schema')
			await db.delete(reports).where(sql`${reports.post_id} = ${postId}`)
		} catch {
			// reports 테이블이 없으면 무시
		}
		
		// 6. 마지막으로 게시글 삭제
		await db.delete(posts).where(sql`${posts.id} = ${postId}`)

		return { success: true, message: '게시글이 삭제되었습니다' }
	},

	// 댓글 삭제
	deleteComment: async (event) => {
        const db = event.locals.db
        await requireAdmin(event)
		const { request } = event

		const formData = await request.formData()
		const commentId = formData.get('commentId')

		if (!commentId) {
			throw error(400, '댓글 ID가 필요합니다')
		}

		await db.delete(comments).where(sql`${comments.id} = ${commentId}`)

		return { success: true, message: '댓글이 삭제되었습니다' }
	},

	// 오래된 게시글 정리 (30일 이상)
	cleanOldPosts: async (event) => {
        const db = event.locals.db
        await requireAdmin(event)

		const thirtyDaysAgo = new Date()
		thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30)

		await db
			.delete(posts)
			.where(sql`${posts.created_at} < ${thirtyDaysAgo.toISOString()}`)

		return { success: true, message: '오래된 게시글이 정리되었습니다' }
	}
}
