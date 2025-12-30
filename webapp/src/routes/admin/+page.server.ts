import { fail } from '@sveltejs/kit'
import type { Actions } from './$types'

const ADMIN_PASSWORD_HASH = 'e4e94bfe953deb4d8fbc803e99caafdeb13104439429359428df80705f425764'

export const actions: Actions = {
    default: async ({ request, cookies }) => {
        const data = await request.formData()
        const password = data.get('password')?.toString() || ''
        
        // SHA-256 해시 생성
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
            
            return { success: true }
        }
        
        return fail(400, { error: '비밀번호가 올바르지 않습니다.' })
    }
}
