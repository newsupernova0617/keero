import { redirect, fail } from '@sveltejs/kit'
import type { PageServerLoad, Actions } from './$types'
import { db } from '$lib/server/db'
import { users } from '$lib/server/schema'
import { eq } from 'drizzle-orm'

export const load: PageServerLoad = async ({ locals: { safeGetSession } }) => {
	const { session, user } = await safeGetSession()

	if (!session) {
		throw redirect(303, '/auth/login')
	}

	// DB에서 사용자 정보 조회
	const dbUser = await db
		.select()
		.from(users)
		.where(eq(users.supabase_id, user!.id))
		.limit(1)

	return {
		user,
		dbUser: dbUser[0] || null
	}
}

export const actions: Actions = {
	updateProfile: async ({ request, locals: { safeGetSession } }) => {
		const { session, user } = await safeGetSession()

		if (!session || !user) {
			return fail(401, { error: '로그인이 필요합니다.' })
		}

		const formData = await request.formData()
		const displayName = formData.get('display_name')?.toString()

		if (!displayName || displayName.trim().length === 0) {
			return fail(400, { error: '표시 이름을 입력해주세요.' })
		}

		if (displayName.length > 50) {
			return fail(400, { error: '표시 이름은 50자를 초과할 수 없습니다.' })
		}

		// DB에서 사용자 조회
		const dbUser = await db
			.select()
			.from(users)
			.where(eq(users.supabase_id, user.id))
			.limit(1)

		if (!dbUser || dbUser.length === 0) {
			// 사용자 생성
			await db.insert(users).values({
				supabase_id: user.id,
				email: user.email || '',
				display_name: displayName.trim()
			})
		} else {
			// 사용자 업데이트
			await db
				.update(users)
				.set({ display_name: displayName.trim() })
				.where(eq(users.supabase_id, user.id))
		}

		return { success: true, message: '프로필이 업데이트되었습니다.' }
	}
}
