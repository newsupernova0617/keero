import { fail } from '@sveltejs/kit'
import type { Actions } from './$types'
import { createHash } from 'crypto'

// 비밀번호: keero2026
const ADMIN_PASSWORD_HASH = '6461160bdd49a2a4d718ccd186984c2169ec09bdf42f6569c0fc9f305dc595f1'

export const actions: Actions = {
    default: async ({ request, cookies }) => {
        const data = await request.formData()
        const password = data.get('password')?.toString() || ''
        
        // SHA-256 해시 생성
        const hash = createHash('sha256').update(password).digest('hex')
        
        console.log('🔐 Admin Login Debug:')
        console.log('  - Input password:', password)
        console.log('  - Generated hash:', hash)
        console.log('  - Expected hash:', ADMIN_PASSWORD_HASH)
        console.log('  - Match:', hash === ADMIN_PASSWORD_HASH)
        
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
