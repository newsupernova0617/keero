import type { LayoutServerLoad } from './$types'

// 비밀번호: keero2026
const ADMIN_PASSWORD_HASH = '6461160bdd49a2a4d718ccd186984c2169ec09bdf42f6569c0fc9f305dc595f1'

export const load: LayoutServerLoad = async ({ cookies }) => {
    // 쿠키에서 관리자 인증 확인
    const adminAuth = cookies.get('admin_auth')
    
    return {
        authenticated: adminAuth === ADMIN_PASSWORD_HASH
    }
}
