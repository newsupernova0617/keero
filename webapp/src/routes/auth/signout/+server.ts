import { redirect } from '@sveltejs/kit'
import type { RequestHandler } from './$types'

export const POST: RequestHandler = async ({ locals: { supabase } }) => {
	await supabase.auth.signOut()
	throw redirect(303, '/')
}

// GET 요청도 지원 (링크 클릭으로 로그아웃 가능)
export const GET: RequestHandler = async ({ locals: { supabase } }) => {
	await supabase.auth.signOut()
	throw redirect(303, '/')
}
