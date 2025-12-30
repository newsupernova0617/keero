import { redirect } from '@sveltejs/kit'
import type { LayoutServerLoad } from './$types'
import { db } from '$lib/server/db'
import { users } from '$lib/server/schema'
import { eq } from 'drizzle-orm'

export const load: LayoutServerLoad = async ({ locals }) => {
    const { session, user } = await locals.safeGetSession()

    if (!session || !user) {
        throw redirect(303, '/auth/login')
    }

    // 사용자 DB에서 조회
    const dbUser = await db.select().from(users).where(eq(users.supabase_id, user.id)).limit(1)

    // 관리자 권한 체크 (role이 99이거나 특정 이메일)
    const isAdmin = 
        (dbUser && dbUser.length > 0 && dbUser[0].role === 99) ||
        user.email === 'yj43773@gmail.com'

    if (!dbUser || dbUser.length === 0 || !isAdmin) {
        throw redirect(303, '/')
    }

    return {
        user: dbUser[0]
    }
}
