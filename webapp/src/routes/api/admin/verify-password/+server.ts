import { json, error } from '@sveltejs/kit'
import { env } from '$env/dynamic/private'
import type { RequestHandler } from './$types'

export const POST: RequestHandler = async ({ request }) => {
	const { password } = await request.json()

	console.log('Password verification:', {
		received: password?.substring(0, 10) + '...',
		expected: env.ADMIN_PASSWORD?.substring(0, 10) + '...',
		match: password === env.ADMIN_PASSWORD
	})

	if (!env.ADMIN_PASSWORD) {
		console.error('ADMIN_PASSWORD not configured!')
		throw error(500, 'Admin password not configured')
	}

	if (password === env.ADMIN_PASSWORD) {
		return json({ success: true })
	} else {
		throw error(401, 'Invalid password')
	}
}
