/**
 * SvelteKit RequestEvent Mock 유틸리티
 * 
 * 서버 액션 테스트를 위한 Mock Event 생성
 */

import type { RequestEvent } from '@sveltejs/kit'

interface MockEventOptions {
	params?: Record<string, string>
	formData?: Record<string, string | File>
	user?: { id: number; role: number; email?: string }
	url?: string
}

/**
 * SvelteKit RequestEvent Mock 생성
 */
export function createMockEvent(options: MockEventOptions = {}): Partial<RequestEvent> {
	const formDataObj = new FormData()
	
	if (options.formData) {
		Object.entries(options.formData).forEach(([key, value]) => {
			if (value instanceof File) {
				formDataObj.append(key, value)
			} else {
				formDataObj.set(key, value)
			}
		})
	}

	return {
		params: options.params || {},
		url: new URL(options.url || 'http://localhost:5173'),
		request: {
			formData: async () => formDataObj,
			headers: new Headers(),
			method: 'POST'
		} as Request,
		locals: {
			user: options.user || null,
			session: options.user ? { user: options.user } : null,
			// safeGetSession Mock 추가
			safeGetSession: async () => ({
				session: options.user ? { user: options.user } : null,
				user: options.user || null
			})
		} as any,
		fetch: global.fetch,
		platform: undefined,
		route: { id: '/test' },
		setHeaders: () => {},
		cookies: {
			get: () => undefined,
			set: () => {},
			delete: () => {},
			serialize: () => ''
		} as any
	} as Partial<RequestEvent>
}

/**
 * Admin 사용자 Mock Event
 */
export function createAdminEvent(options: Omit<MockEventOptions, 'user'> = {}) {
	return createMockEvent({
		...options,
		user: { id: 1, role: 99, email: 'admin@test.com' }
	})
}

/**
 * 일반 사용자 Mock Event
 */
export function createUserEvent(options: Omit<MockEventOptions, 'user'> = {}) {
	return createMockEvent({
		...options,
		user: { id: 2, role: 1, email: 'user@test.com' }
	})
}
