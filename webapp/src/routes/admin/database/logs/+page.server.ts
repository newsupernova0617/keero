import { requireAdmin } from '$lib/server/auth'
import Database from 'better-sqlite3'
import type { PageServerLoad } from './$types'

const DB_PATH = process.env.DATABASE_PATH || './data/posts.db'
const sqlite = new Database(DB_PATH)

export const load: PageServerLoad = async (event) => {
	await requireAdmin(event)

	const { url } = event
	const page = parseInt(url.searchParams.get('page') || '1')
	const pageSize = 50
	const offset = (page - 1) * pageSize

	const action = url.searchParams.get('action') || ''
	const tableName = url.searchParams.get('table') || ''

	// 필터 조건 구성
	let whereClause = ''
	const params: unknown[] = []

	if (action) {
		whereClause += ' AND action = ?'
		params.push(action)
	}

	if (tableName) {
		whereClause += ' AND table_name = ?'
		params.push(tableName)
	}

	// 총 개수
	const countQuery = `SELECT COUNT(*) as count FROM audit_logs WHERE 1=1${whereClause}`
	const countResult = sqlite.prepare(countQuery).get(...params) as { count: number }
	const totalCount = countResult.count

	// 로그 조회
	const logsQuery = `
		SELECT 
			al.*,
			u.display_name as user_name,
			u.email as user_email
		FROM audit_logs al
		LEFT JOIN users u ON al.user_id = u.id
		WHERE 1=1${whereClause}
		ORDER BY al.created_at DESC
		LIMIT ? OFFSET ?
	`
	const logs = sqlite.prepare(logsQuery).all(...params, pageSize, offset) as Array<{
		id: number
		userId: number | null
		action: string
		tableName: string
		recordId: number | null
		oldValue: string | null
		newValue: string | null
		query: string | null
		createdAt: string
		user_name: string | null
		user_email: string | null
	}>

	// 액션 타입 목록
	const actions = sqlite
		.prepare('SELECT DISTINCT action FROM audit_logs ORDER BY action')
		.all() as { action: string }[]

	// 테이블 목록
	const tables = sqlite
		.prepare('SELECT DISTINCT table_name FROM audit_logs ORDER BY table_name')
		.all() as { table_name: string }[]

	return {
		logs,
		actions: actions.map((a) => a.action),
		tables: tables.map((t) => t.table_name),
		pagination: {
			page,
			pageSize,
			totalCount,
			totalPages: Math.ceil(totalCount / pageSize)
		},
		filters: {
			action,
			tableName
		}
	}
}
