import { requireAdmin } from '$lib/server/auth'
import Database from 'better-sqlite3'
import { fail } from '@sveltejs/kit'
import type { PageServerLoad, Actions } from './$types'
import { statSync } from 'fs'

const DB_PATH = process.env.DATABASE_PATH || './data/posts.db'
const sqlite = new Database(DB_PATH)

interface TableInfo {
	name: string
	rowCount: number
	size: number
}

function formatBytes(bytes: number): string {
	if (bytes === 0) return '0 Bytes'
	const k = 1024
	const sizes = ['Bytes', 'KB', 'MB', 'GB']
	const i = Math.floor(Math.log(bytes) / Math.log(k))
	return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i]
}

export const load: PageServerLoad = async (event) => {
	await requireAdmin(event)

	// DB 파일 크기
	let dbSize = 0
	try {
		const stats = statSync(DB_PATH)
		dbSize = stats.size
	} catch (err) {
		console.error('Error reading DB file:', err)
	}

	// 모든 테이블 목록
	const tables = sqlite
		.prepare("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
		.all() as { name: string }[]

	// 각 테이블의 정보
	const tableStats: TableInfo[] = []
	for (const table of tables) {
		try {
			const countResult = sqlite
				.prepare(`SELECT COUNT(*) as count FROM ${table.name}`)
				.get() as { count: number }

			// 테이블 크기 추정 (페이지 수 * 페이지 크기)
			const sizeResult = sqlite
				.prepare(
					`SELECT SUM(pgsize) as size FROM dbstat WHERE name = ?`
				)
				.get(table.name) as { size: number | null }

			tableStats.push({
				name: table.name,
				rowCount: countResult.count,
				size: sizeResult?.size || 0
			})
		} catch (err) {
			console.error(`Error getting stats for ${table.name}:`, err)
		}
	}

	// 인덱스 정보
	const indexes = sqlite
		.prepare(
			"SELECT name, tbl_name FROM sqlite_master WHERE type='index' AND sql IS NOT NULL ORDER BY tbl_name, name"
		)
		.all() as { name: string; tbl_name: string }[]

	// PRAGMA 정보
	const pragmaInfo = {
		pageSize: (sqlite.prepare('PRAGMA page_size').get() as { page_size: number }).page_size,
		pageCount: (sqlite.prepare('PRAGMA page_count').get() as { page_count: number }).page_count,
		journalMode: (sqlite.prepare('PRAGMA journal_mode').get() as { journal_mode: string })
			.journal_mode,
		synchronous: (sqlite.prepare('PRAGMA synchronous').get() as { synchronous: number })
			.synchronous
	}

	return {
		dbSize,
		dbSizeFormatted: formatBytes(dbSize),
		tableStats: tableStats.map((t) => ({
			...t,
			sizeFormatted: formatBytes(t.size)
		})),
		indexes,
		pragmaInfo,
		totalRows: tableStats.reduce((sum, t) => sum + t.rowCount, 0)
	}
}

export const actions: Actions = {
	// VACUUM 실행
	vacuum: async (event) => {
		await requireAdmin(event)

		try {
			const startTime = Date.now()
			sqlite.exec('VACUUM')
			const executionTime = Date.now() - startTime

			return {
				success: true,
				message: `VACUUM 완료 (${executionTime}ms)`
			}
		} catch (err) {
			console.error('VACUUM error:', err)
			return fail(500, {
				error: err instanceof Error ? err.message : 'VACUUM 실행에 실패했습니다'
			})
		}
	},

	// ANALYZE 실행
	analyze: async (event) => {
		await requireAdmin(event)

		try {
			const startTime = Date.now()
			sqlite.exec('ANALYZE')
			const executionTime = Date.now() - startTime

			return {
				success: true,
				message: `ANALYZE 완료 (${executionTime}ms)`
			}
		} catch (err) {
			console.error('ANALYZE error:', err)
			return fail(500, {
				error: err instanceof Error ? err.message : 'ANALYZE 실행에 실패했습니다'
			})
		}
	},

	// PRAGMA optimize 실행
	optimize: async (event) => {
		await requireAdmin(event)

		try {
			const startTime = Date.now()
			sqlite.exec('PRAGMA optimize')
			const executionTime = Date.now() - startTime

			return {
				success: true,
				message: `최적화 완료 (${executionTime}ms)`
			}
		} catch (err) {
			console.error('Optimize error:', err)
			return fail(500, {
				error: err instanceof Error ? err.message : '최적화 실행에 실패했습니다'
			})
		}
	}
}
