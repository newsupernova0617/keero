import { requireAdmin } from '$lib/server/auth'
import Database from 'better-sqlite3'
import { getTableMetadata, isValidTableName } from '$lib/server/tableMetadata'
import { error, fail } from '@sveltejs/kit'
import type { PageServerLoad, Actions } from './$types'

// SQLite 인스턴스 가져오기
const DB_PATH = process.env.DATABASE_PATH || './data/posts.db'
const sqlite = new Database(DB_PATH)

export const load: PageServerLoad = async (event) => {
	await requireAdmin(event)

	const { tableName } = event.params
	
	// Security: Validate table name against whitelist
	if (!isValidTableName(tableName)) {
		throw error(400, '유효하지 않은 테이블명입니다')
	}
	
	const tableMetadata = getTableMetadata(tableName)

	if (!tableMetadata) {
		throw error(404, '테이블을 찾을 수 없습니다')
	}

	// 테이블 데이터 조회
	try {
		const data = sqlite.prepare(`SELECT * FROM ${tableName} ORDER BY id DESC LIMIT 1000`).all()

		return {
			tableMetadata,
			data: (data as Record<string, unknown>[]) || []
		}
	} catch (err) {
		console.error(`Error loading table ${tableName}:`, err)
		return {
			tableMetadata,
			data: []
		}
	}
}

export const actions: Actions = {
	// 레코드 생성
	create: async (event) => {
		await requireAdmin(event)
		const { tableName } = event.params
		
		// Security: Validate table name
		if (!isValidTableName(tableName)) {
			return fail(400, { error: '유효하지 않은 테이블명입니다' })
		}
		
		const tableMetadata = getTableMetadata(tableName)

		if (!tableMetadata || !tableMetadata.canCreate) {
			return fail(403, { error: '생성 권한이 없습니다' })
		}

		const formData = await event.request.formData()
		const data: Record<string, unknown> = {}

		// FormData를 객체로 변환
		for (const [key, value] of formData.entries()) {
			if (key === 'id') continue // ID는 자동 생성

			const column = tableMetadata.columns.find((col) => col.key === key)
			if (!column) continue

			// 타입에 맞게 변환
			if (column.type === 'number') {
				data[key] = value ? parseInt(value as string) : null
			} else if (column.type === 'boolean') {
				data[key] = value === 'true' || value === '1' ? 1 : 0
			} else {
				data[key] = value || null
			}
		}

		try {
			// 동적 INSERT 쿼리 생성
			const columns = Object.keys(data).join(', ')
			const placeholders = Object.keys(data)
				.map(() => '?')
				.join(', ')
			const values = Object.values(data)

			sqlite.prepare(`INSERT INTO ${tableName} (${columns}) VALUES (${placeholders})`).run(...values)

			return { success: true, message: '레코드가 생성되었습니다' }
		} catch (err) {
			console.error('Create error:', err)
			return fail(500, { error: '레코드 생성에 실패했습니다' })
		}
	},

	// 레코드 수정
	update: async (event) => {
		await requireAdmin(event)
		const { tableName } = event.params
		
		// Security: Validate table name
		if (!isValidTableName(tableName)) {
			return fail(400, { error: '유효하지 않은 테이블명입니다' })
		}
		
		const tableMetadata = getTableMetadata(tableName)

		if (!tableMetadata || !tableMetadata.canEdit) {
			return fail(403, { error: '수정 권한이 없습니다' })
		}

		const formData = await event.request.formData()
		const id = formData.get('id')

		if (!id) {
			return fail(400, { error: 'ID가 필요합니다' })
		}

		const data: Record<string, unknown> = {}

		// FormData를 객체로 변환
		for (const [key, value] of formData.entries()) {
			if (key === 'id') continue

			const column = tableMetadata.columns.find((col) => col.key === key)
			if (!column || !column.editable) continue

			// 타입에 맞게 변환
			if (column.type === 'number') {
				data[key] = value ? parseInt(value as string) : null
			} else if (column.type === 'boolean') {
				data[key] = value === 'true' || value === '1' ? 1 : 0
			} else {
				data[key] = value || null
			}
		}

		try {
			// 동적 UPDATE 쿼리 생성
			const setClause = Object.keys(data)
				.map((key) => `${key} = ?`)
				.join(', ')
			const values = [...Object.values(data), id]

			sqlite.prepare(`UPDATE ${tableName} SET ${setClause} WHERE id = ?`).run(...values)

			return { success: true, message: '레코드가 수정되었습니다' }
		} catch (err) {
			console.error('Update error:', err)
			return fail(500, { error: '레코드 수정에 실패했습니다' })
		}
	},

	// 레코드 삭제
	delete: async (event) => {
		await requireAdmin(event)
		const { tableName } = event.params
		
		// Security: Validate table name
		if (!isValidTableName(tableName)) {
			return fail(400, { error: '유효하지 않은 테이블명입니다' })
		}
		
		const tableMetadata = getTableMetadata(tableName)

		if (!tableMetadata || !tableMetadata.canDelete) {
			return fail(403, { error: '삭제 권한이 없습니다' })
		}

		const formData = await event.request.formData()
		const id = formData.get('id')

		if (!id) {
			return fail(400, { error: 'ID가 필요합니다' })
		}

		try {
			sqlite.prepare(`DELETE FROM ${tableName} WHERE id = ?`).run(id)

			return { success: true, message: '레코드가 삭제되었습니다' }
		} catch (err) {
			console.error('Delete error:', err)
			return fail(500, { error: '레코드 삭제에 실패했습니다' })
		}
	},

	// 벌크 삭제
	bulkDelete: async (event) => {
		await requireAdmin(event)
		const { tableName } = event.params
		
		// Security: Validate table name
		if (!isValidTableName(tableName)) {
			return fail(400, { error: '유효하지 않은 테이블명입니다' })
		}
		
		const tableMetadata = getTableMetadata(tableName)

		if (!tableMetadata || !tableMetadata.canDelete) {
			return fail(403, { error: '삭제 권한이 없습니다' })
		}

		const formData = await event.request.formData()
		const idsJson = formData.get('ids')

		if (!idsJson) {
			return fail(400, { error: 'ID 목록이 필요합니다' })
		}

		try {
			const ids = JSON.parse(idsJson as string)
			if (!Array.isArray(ids) || ids.length === 0) {
				return fail(400, { error: '유효한 ID 목록이 필요합니다' })
			}

			const placeholders = ids.map(() => '?').join(', ')
			sqlite.prepare(`DELETE FROM ${tableName} WHERE id IN (${placeholders})`).run(...ids)

			return { success: true, message: `${ids.length}개의 레코드가 삭제되었습니다` }
		} catch (err) {
			console.error('Bulk delete error:', err)
			return fail(500, { error: '벌크 삭제에 실패했습니다' })
		}
	}
}
