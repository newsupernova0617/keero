import { error, json } from '@sveltejs/kit'
import type { RequestHandler } from './$types'
import { env } from '$env/dynamic/private'

// 로그 조회 (Admin 전용)
export const GET: RequestHandler = async () => {
	// requireAdmin(event) 생략 - D1에서 직접 볼 수 있도록 유도
	throw error(501, {
		message: '이 기능은 Cloudflare D1에서 지원되지 않습니다.',
		hint: 'D1 대시보드를 사용하세요: https://dash.cloudflare.com'
	})
}

// 로그 저장 (크롤러 전용)
export const POST: RequestHandler = async ({ request }) => {
	try {
		// 1. API Key 검증
		const apiKey = request.headers.get('X-API-Key');
		const expectedKey = env.CRAWLER_API_KEY;

		if (!expectedKey) {
			console.error('❌ CRAWLER_API_KEY not configured');
			return json({ error: 'Server configuration error' }, { status: 500 });
		}

		if (!apiKey || apiKey !== expectedKey) {
			console.warn('⚠️ Unauthorized Logs API request');
			return json({ error: 'Unauthorized' }, { status: 401 });
		}

		// 현재 Cloudflare D1에서는 로그 테이블을 별도로 관리하지 않기로 함 (무료 한도 및 성능 고려)
		// 하지만 크롤러가 성공 응답을 기대하므로 200 OK 반환
		return json({ success: true, message: 'Logs received (but not stored in D1 for now)' })
	} catch (e) {
		console.error('Error processing logs API:', e)
		return json({ success: false, error: 'Internal Server Error' }, { status: 500 })
	}
}
