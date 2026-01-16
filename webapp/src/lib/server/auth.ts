import { redirect, error } from '@sveltejs/kit'
import { db } from '$lib/server/db'
import { users } from '$lib/server/schema'
import { eq } from 'drizzle-orm'
import type { RequestEvent } from '@sveltejs/kit'
import { env } from '$env/dynamic/private'

// Security: Admin emails from environment variable (comma-separated)
const ADMIN_EMAILS = (env.ADMIN_EMAILS || '').split(',').map(email => email.trim()).filter(Boolean)

/**
 * 관리자 권한 체크 함수
 */
export async function requireAdmin(event: RequestEvent) {
    const { user } = await event.locals.safeGetSession()

    if (!user) {
        // 원래 접근하려던 URL을 redirect 파라미터로 전달
        const redirectUrl = event.url.pathname
        throw redirect(303, `/auth/login?redirect=${encodeURIComponent(redirectUrl)}`)
    }

    // DB에서 사용자 정보 조회
    const dbUser = await db
        .select()
        .from(users)
        .where(eq(users.supabase_id, user.id))
        .limit(1)

    if (!dbUser || dbUser.length === 0) {
        throw error(403, '권한이 없습니다.')
    }

    // 관리자 권한 체크 (role이 99(admin)이거나 환경변수에 등록된 이메일)
    const isAdmin = 
        dbUser[0].role === 99 || // 99: admin
        ADMIN_EMAILS.includes(user.email || '')

    if (!isAdmin) {
        throw error(403, '관리자 권한이 필요합니다.')
    }

    return {
        user,
        dbUser: dbUser[0]
    }
}

/**
 * 로그인 필수 체크 함수
 */
export async function requireAuth(event: RequestEvent) {
    const { user } = await event.locals.safeGetSession()

    if (!user) {
        const redirectUrl = event.url.pathname
        throw redirect(303, `/auth/login?redirect=${encodeURIComponent(redirectUrl)}`)
    }

    return { user }
}
