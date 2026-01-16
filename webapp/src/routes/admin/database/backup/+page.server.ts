import { requireAdmin } from '$lib/server/auth'
import Database from 'better-sqlite3'
import { fail } from '@sveltejs/kit'
import type { PageServerLoad, Actions } from './$types'
import { statSync, writeFileSync, unlinkSync, existsSync, mkdirSync } from 'fs'
import { join } from 'path'
import {
	uploadBackupToR2,
	listBackupsFromR2,
	downloadBackupFromR2,
	deleteBackupFromR2
} from '$lib/server/r2-backup'

const DB_PATH = process.env.DATABASE_PATH || './data/posts.db'
const TEMP_DIR = process.env.TEMP_DIR || './temp'

// 임시 디렉토리 생성
if (!existsSync(TEMP_DIR)) {
	mkdirSync(TEMP_DIR, { recursive: true })
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

	// 현재 DB 정보
	let dbInfo = {
		path: DB_PATH,
		size: 0,
		lastModified: new Date()
	}

	try {
		const stats = statSync(DB_PATH)
		dbInfo = {
			path: DB_PATH,
			size: stats.size,
			lastModified: stats.mtime
		}
	} catch (err) {
		console.error('Error reading DB file:', err)
	}

	// R2에서 백업 파일 목록 조회
	const backups = await listBackupsFromR2()

	return {
		dbInfo: {
			...dbInfo,
			sizeFormatted: formatBytes(dbInfo.size)
		},
		backups: backups.map((b) => ({
			...b,
			sizeFormatted: formatBytes(b.size),
			lastModifiedFormatted: b.lastModified.toLocaleString('ko-KR')
		})),
		storageType: 'R2' // 스토리지 타입 표시
	}
}

export const actions: Actions = {
	// 백업 생성 및 R2 업로드
	createBackup: async (event) => {
		await requireAdmin(event)

		try {
			const timestamp = new Date().toISOString().replace(/[:.]/g, '-').split('T').join('_')
			const backupFilename = `backup_${timestamp}.db`
			const tempBackupPath = join(TEMP_DIR, backupFilename)

			// SQLite VACUUM INTO로 백업 생성
			const sqlite = new Database(DB_PATH)
			sqlite.exec(`VACUUM INTO '${tempBackupPath}'`)
			sqlite.close()

			// R2에 업로드
			const uploadResult = await uploadBackupToR2(tempBackupPath, backupFilename)

			// 임시 파일 삭제
			unlinkSync(tempBackupPath)

			return {
				success: true,
				message: `백업이 R2에 생성되었습니다: ${backupFilename} (${formatBytes(uploadResult.size)})`
			}
		} catch (err) {
			console.error('Backup creation error:', err)
			return fail(500, {
				error: err instanceof Error ? err.message : '백업 생성에 실패했습니다'
			})
		}
	},

	// R2에서 백업 삭제
	deleteBackup: async (event) => {
		await requireAdmin(event)

		const formData = await event.request.formData()
		const filename = formData.get('filename') as string

		if (!filename) {
			return fail(400, { error: '파일명이 필요합니다' })
		}

		try {
			await deleteBackupFromR2(filename)

			return {
				success: true,
				message: `백업 파일이 R2에서 삭제되었습니다: ${filename}`
			}
		} catch (err) {
			console.error('Backup deletion error:', err)
			return fail(500, {
				error: err instanceof Error ? err.message : '백업 삭제에 실패했습니다'
			})
		}
	},

	// R2에서 백업 복원
	restoreBackup: async (event) => {
		await requireAdmin(event)

		const formData = await event.request.formData()
		const filename = formData.get('filename') as string

		if (!filename) {
			return fail(400, { error: '파일명이 필요합니다' })
		}

		try {
			// R2에서 백업 다운로드
			const backupBuffer = await downloadBackupFromR2(filename)

			// 현재 DB를 임시 백업 (R2에 업로드)
			const timestamp = Date.now()
			const tempBackupFilename = `temp_before_restore_${timestamp}.db`
			const tempBackupPath = join(TEMP_DIR, tempBackupFilename)
			const sqlite = new Database(DB_PATH)
			sqlite.exec(`VACUUM INTO '${tempBackupPath}'`)
			sqlite.close()

			// 임시 백업을 R2에 업로드
			await uploadBackupToR2(tempBackupPath, tempBackupFilename)
			unlinkSync(tempBackupPath)

			// 다운로드한 백업으로 DB 교체
			writeFileSync(DB_PATH, backupBuffer)

			return {
				success: true,
				message: `백업이 복원되었습니다. 이전 DB는 ${tempBackupFilename}로 R2에 저장되었습니다.`
			}
		} catch (err) {
			console.error('Backup restoration error:', err)
			return fail(500, {
				error: err instanceof Error ? err.message : '백업 복원에 실패했습니다'
			})
		}
	},

	// R2에서 백업 다운로드
	downloadBackup: async (event) => {
		await requireAdmin(event)

		const formData = await event.request.formData()
		const filename = formData.get('filename') as string

		if (!filename) {
			return fail(400, { error: '파일명이 필요합니다' })
		}

		try {
			const backupBuffer = await downloadBackupFromR2(filename)

			// 다운로드 응답 반환
			return new Response(new Uint8Array(backupBuffer), {
				headers: {
					'Content-Type': 'application/x-sqlite3',
					'Content-Disposition': `attachment; filename="${filename}"`
				}
			})
		} catch (err) {
			console.error('Backup download error:', err)
			return fail(500, {
				error: err instanceof Error ? err.message : '백업 다운로드에 실패했습니다'
			})
		}
	}
}
