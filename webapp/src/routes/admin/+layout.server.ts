import { redirect } from '@sveltejs/kit'
import type { LayoutServerLoad } from './$types'

const ADMIN_PASSWORD_HASH = 'e4e94bfe953deb4d8fbc803e99caafdeb13104439429359428df80705f425764'

export const load: LayoutServerLoad = async ({ cookies }) => {
    // 쿠키에서 관리자 인증 확인
    const adminAuth = cookies.get('admin_auth')
    
    if (adminAuth !== ADMIN_PASSWORD_HASH) {
        throw redirect(303, '/admin/login')
    }

    return {
        authenticated: true
    }
}
