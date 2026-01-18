import { requireAdmin } from '$lib/server/auth'
import { reports, users, posts, comments } from '$lib/server/schema'
import { eq, desc, sql } from 'drizzle-orm'
import { fail } from '@sveltejs/kit'
import type { PageServerLoad, Actions } from './$types'

export const load: PageServerLoad = async (event) => {
    const db = event.locals.db
	await requireAdmin(event)

	// 모든 신고 조회
	const allReports = await db
		.select({
			id: reports.id,
			reason: reports.reason,
			description: reports.description,
			status: reports.status,
			created_at: reports.created_at,
			resolved_at: reports.resolved_at,
			// Reporter info
			reporter_id: sql<number>`${users.id}`,
			reporter_email: sql<string>`${users.email}`,
			reporter_display_name: sql<string>`${users.display_name}`,
			// Reported content
			post_id: reports.post_id,
			comment_id: reports.comment_id,
			post_title: sql<string>`${posts.title}`,
			comment_content: sql<string>`${comments.content}`
		})
		.from(reports)
		.leftJoin(users, eq(reports.user_id, users.id))
		.leftJoin(posts, eq(reports.post_id, posts.id))
		.leftJoin(comments, eq(reports.comment_id, comments.id))
		.orderBy(desc(reports.id))
		.limit(100)

	return {
		reports: allReports
	}
}

export const actions: Actions = {
	resolve: async (event) => {
        const db = event.locals.db
        await requireAdmin(event)
		const { user } = await event.locals.safeGetSession()

		const formData = await event.request.formData()
		const reportId = formData.get('report_id')?.toString()

		if (!reportId) {
			return fail(400, { error: '잘못된 요청입니다.' })
		}

		// 관리자 DB ID 조회
		const adminUser = await db
			.select()
			.from(users)
			.where(eq(users.supabase_id, user!.id))
			.limit(1)

		await db
			.update(reports)
			.set({
				status: 'resolved',
				resolved_at: new Date().toISOString(),
				resolved_by: adminUser[0]?.id || null
			})
			.where(eq(reports.id, parseInt(reportId)))

		return { success: true }
	},

	reject: async (event) => {
        const db = event.locals.db
        await requireAdmin(event)
		const { user } = await event.locals.safeGetSession()

		const formData = await event.request.formData()
		const reportId = formData.get('report_id')?.toString()

		if (!reportId) {
			return fail(400, { error: '잘못된 요청입니다.' })
		}

		// 관리자 DB ID 조회
		const adminUser = await db
			.select()
			.from(users)
			.where(eq(users.supabase_id, user!.id))
			.limit(1)

		await db
			.update(reports)
			.set({
				status: 'rejected',
				resolved_at: new Date().toISOString(),
				resolved_by: adminUser[0]?.id || null
			})
			.where(eq(reports.id, parseInt(reportId)))

		return { success: true }
	},

	deleteContent: async (event) => {
        const db = event.locals.db
        await requireAdmin(event)
		const { user } = await event.locals.safeGetSession()

		const formData = await event.request.formData()
		const reportId = formData.get('report_id')?.toString()

		if (!reportId) {
			return fail(400, { error: '잘못된 요청입니다.' })
		}

		// 신고 정보 조회
		const report = await db
			.select()
			.from(reports)
			.where(eq(reports.id, parseInt(reportId)))
			.limit(1)

		if (!report || report.length === 0) {
			return fail(404, { error: '신고를 찾을 수 없습니다.' })
		}

		// 신고된 콘텐츠 삭제
		if (report[0].post_id) {
			// 게시글 삭제는 구현하지 않음 (크롤링된 데이터이므로)
			return fail(400, { error: '게시글은 삭제할 수 없습니다.' })
		} else if (report[0].comment_id) {
			// 댓글 soft delete
			await db
				.update(comments)
				.set({
					is_deleted: true,
					content: '관리자에 의해 삭제된 댓글입니다.'
				})
				.where(eq(comments.id, report[0].comment_id))
		}

		// 신고 상태 업데이트
		const adminUser = await db
			.select()
			.from(users)
			.where(eq(users.supabase_id, user!.id))
			.limit(1)

		await db
			.update(reports)
			.set({
				status: 'resolved',
				resolved_at: new Date().toISOString(),
				resolved_by: adminUser[0]?.id || null
			})
			.where(eq(reports.id, parseInt(reportId)))

		return { success: true }
	}
}
