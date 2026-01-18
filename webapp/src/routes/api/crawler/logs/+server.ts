import { requireAdmin } from '$lib/server/auth'
import { error } from '@sveltejs/kit'
import type { PageServerLoad } from './$types'

export const load: PageServerLoad = async (event) => {
await requireAdmin(event)

throw error(501, {
message: '이 기능은 Cloudflare D1에서 지원되지 않습니다.',
hint: 'D1 대시보드를 사용하세요: https://dash.cloudflare.com'
})
}
