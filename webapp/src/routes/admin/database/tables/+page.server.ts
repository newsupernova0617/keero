import { requireAdmin } from '$lib/server/auth'
import Database from 'better-sqlite3'
import { getAllTables } from '$lib/server/tableMetadata'
import type { PageServerLoad } from './$types'

// SQLite 인스턴스 가져오기
const DB_PATH = process.env.DATABASE_PATH || './data/posts.db'
const sqlite = new Database(DB_PATH)

export const load: PageServerLoad = async (event) => {
	await requireAdmin(event)

	const tables = getAllTables()

	// 각 테이블의 레코드 수 조회
	const tableStats = await Promise.all(
		tables.map(async (table) => {
			try {
				const result = sqlite.prepare(`SELECT COUNT(*) as count FROM ${table.name}`).get() as { count: number }
				return {
					...table,
					count: result?.count || 0
				}
			} catch (error) {
				console.error(`Error counting ${table.name}:`, error)
				return {
					...table,
					count: 0
				}
			}
		})
	)

	return {
		tables: tableStats
	}
}
