import { requireAdmin } from '$lib/server/auth'
import { error } from '@sveltejs/kit'
import type { PageServerLoad } from './$types'

export const load: PageServerLoad = async (event) => {
	await requireAdmin(event)
	
	// D1에서는 직접 SQLite 파일 접근이 불가능
	throw error(501, {
		message: 'Database Monitor 기능은 Cloudflare D1에서 지원되지 않습니다.',
		hint: 'D1 대시보드(https://dash.cloudflare.com)를 사용하세요.'
	})
}
