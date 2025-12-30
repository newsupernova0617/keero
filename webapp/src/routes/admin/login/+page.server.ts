import { redirect, fail } from '@sveltejs/kit'
import type { Actions, PageServerLoad } from './$types'

const ADMIN_PASSWORD_HASH = 'e4e94bfe953deb4d8fbc803e99caafdeb13104439429359428df80705f425764'

export const load: PageServerLoad = async ({ cookies }) => {
    // 이미 인증되어 있으면 관리자 페이지로
    const adminAuth = cookies.get('admin_auth')
    if (adminAuth === ADMIN_PASSWORD_HASH) {
        throw redirect(303, '/admin')
    }
    
    return {}
}

export const actions: Actions = {
    default: async ({ request, cookies }) => {
        const data = await request.formData()
        const password = data.get('password')?.toString() || ''
        
        // SHA-256 해시 생성 (간단 비교를 위해 직접 비교)
        // 실제로는 crypto를 사용해야 하지만, 여기서는 해시를 직접 받음
        const crypto = await import('crypto')
        const hash = crypto.createHash('sha256').update(password).digest('hex')
        
        if (hash === ADMIN_PASSWORD_HASH) {
            // 쿠키 설정 (7일 유효)
            cookies.set('admin_auth', ADMIN_PASSWORD_HASH, {
                path: '/',
                httpOnly: true,
                secure: true,
                sameSite: 'lax',
                maxAge: 60 * 60 * 24 * 7 // 7일
            })
            
            throw redirect(303, '/admin')
        }
        
        return fail(400, { error: '비밀번호가 올바르지 않습니다.' })
    }
}
