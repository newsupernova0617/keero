import { json, error } from '@sveltejs/kit'
import { ADMIN_PASSWORD } from '$env/static/private'
import type { RequestHandler } from './$types'

export const POST: RequestHandler = async ({ request }) => {
	const { password } = await request.json()

	console.log('Password verification:', {
		received: password?.substring(0, 10) + '...',
		expected: ADMIN_PASSWORD?.substring(0, 10) + '...',
		match: password === ADMIN_PASSWORD
	})

	if (!ADMIN_PASSWORD) {
		console.error('ADMIN_PASSWORD not configured!')
		throw error(500, 'Admin password not configured')
	}

	if (password === ADMIN_PASSWORD) {
		return json({ success: true })
	} else {
		throw error(401, 'Invalid password')
	}
}
