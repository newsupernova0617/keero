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

    if (!dbUser || dbUser.length === 0 || dbUser[0].role !== 99) {
        throw redirect(303, '/')
    }

    return {
        user: dbUser[0]
    }
}
