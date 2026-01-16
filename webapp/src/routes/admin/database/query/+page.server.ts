import { requireAdmin } from '$lib/server/auth'
import Database from 'better-sqlite3'
import { fail } from '@sveltejs/kit'
import type { PageServerLoad, Actions } from './$types'

const DB_PATH = process.env.DATABASE_PATH || './data/posts.db'
const sqlite = new Database(DB_PATH)

// 위험한 쿼리 패턴
const DANGEROUS_PATTERNS = [
	/DROP\s+TABLE/i,
	/DROP\s+DATABASE/i,
	/TRUNCATE/i,
	/DELETE\s+FROM\s+\w+\s*;?\s*$/i, // WHERE 절 없는 DELETE
	/UPDATE\s+\w+\s+SET\s+.*\s*;?\s*$/i // WHERE 절 없는 UPDATE
]

export const load: PageServerLoad = async (event) => {
	await requireAdmin(event)

	return {
		// 쿼리 히스토리는 클라이언트 localStorage에서 관리
	}
}

export const actions: Actions = {
	// 쿼리 실행
	execute: async (event) => {
		const { user } = await requireAdmin(event)

		const formData = await event.request.formData()
		const query = formData.get('query') as string
		const mode = formData.get('mode') as string // 'read' or 'write'

		if (!query || !query.trim()) {
			return fail(400, { error: '쿼리를 입력해주세요' })
		}

		const trimmedQuery = query.trim()

		// 읽기 전용 모드에서는 SELECT만 허용
		if (mode === 'read' && !trimmedQuery.toUpperCase().startsWith('SELECT')) {
			return fail(403, { error: '읽기 전용 모드에서는 SELECT 쿼리만 실행할 수 있습니다' })
		}

		// 위험한 쿼리 감지
		const isDangerous = DANGEROUS_PATTERNS.some((pattern) => pattern.test(trimmedQuery))
		if (isDangerous && mode !== 'write-confirmed') {
			return fail(400, {
				error: '위험한 쿼리가 감지되었습니다',
				warning: true,
				query: trimmedQuery
			})
		}

		try {
			const startTime = Date.now()

			// SELECT 쿼리인 경우
			if (trimmedQuery.toUpperCase().startsWith('SELECT')) {
				const results = sqlite.prepare(trimmedQuery).all()
				const executionTime = Date.now() - startTime

				// Security: Audit log for SELECT queries
				console.log(`[AUDIT] Admin query executed:`, {
					timestamp: new Date().toISOString(),
					admin: user.email || 'unknown',
					queryType: 'SELECT',
					executionTime: `${executionTime}ms`,
					rowCount: results.length
				})

				return {
					success: true,
					results: results as Record<string, unknown>[],
					rowCount: results.length,
					executionTime,
					query: trimmedQuery
				}
			}
			// INSERT, UPDATE, DELETE 등
			else {
				const result = sqlite.prepare(trimmedQuery).run()
				const executionTime = Date.now() - startTime

				// Security: Audit log for write queries (CRITICAL)
				console.warn(`[AUDIT] Admin WRITE query executed:`, {
					timestamp: new Date().toISOString(),
					admin: user.email || 'unknown',
					queryType: trimmedQuery.split(' ')[0].toUpperCase(),
					executionTime: `${executionTime}ms`,
					affectedRows: result.changes,
					query: trimmedQuery.substring(0, 200) // Log first 200 chars
				})

				return {
					success: true,
					changes: result.changes,
					lastInsertRowid: result.lastInsertRowid,
					executionTime,
					query: trimmedQuery,
					message: `${result.changes}개의 행이 영향을 받았습니다`
				}
			}
		} catch (err) {
			console.error('Query execution error:', err)

			// Security: Log failed queries
			console.error(`[AUDIT] Query execution FAILED:`, {
				timestamp: new Date().toISOString(),
				admin: user.email || 'unknown',
				query: trimmedQuery.substring(0, 200),
				error: err instanceof Error ? err.message : 'Unknown error'
			})

			return fail(500, {
				error: err instanceof Error ? err.message : '쿼리 실행에 실패했습니다',
				query: trimmedQuery
			})
		}
	}
}
