/**
 * R2 백업 시스템 단위 테스트
 * 
 * 테스트 항목:
 * 1. uploadBackupToR2 - 백업 파일 R2 업로드
 * 2. listBackupsFromR2 - R2 백업 목록 조회
 * 3. downloadBackupFromR2 - R2에서 백업 다운로드
 * 4. deleteBackupFromR2 - R2에서 백업 삭제
 */

import { describe, it, expect, beforeAll, afterAll } from 'vitest'
import { existsSync, writeFileSync, unlinkSync, mkdirSync } from 'fs'
import { join } from 'path'
import {
	uploadBackupToR2,
	listBackupsFromR2,
	downloadBackupFromR2,
	deleteBackupFromR2
} from '../src/lib/server/r2-backup'

const TEST_DIR = './test-temp'
const TEST_FILENAME = 'test-backup.db'
const TEST_FILE_PATH = join(TEST_DIR, TEST_FILENAME)

describe('R2 Backup System', () => {
	beforeAll(() => {
		// 테스트 디렉토리 생성
		if (!existsSync(TEST_DIR)) {
			mkdirSync(TEST_DIR, { recursive: true })
		}
		
		// 테스트용 더미 DB 파일 생성 (1KB)
		const dummyData = Buffer.alloc(1024, 'test')
		writeFileSync(TEST_FILE_PATH, dummyData)
	})

	afterAll(() => {
		// 테스트 파일 정리
		if (existsSync(TEST_FILE_PATH)) {
			unlinkSync(TEST_FILE_PATH)
		}
	})

	// 1. R2 업로드 테스트
	it('백업 파일을 R2에 업로드', async () => {
		const result = await uploadBackupToR2(TEST_FILE_PATH, TEST_FILENAME)
		
		expect(result).toBeDefined()
		expect(result.key).toBe(`backups/${TEST_FILENAME}`)
		expect(result.filename).toBe(TEST_FILENAME)
		expect(result.size).toBeGreaterThan(0)
	}, 30000) // 30초 타임아웃

	// 2. R2 목록 조회 테스트
	it('R2에서 백업 목록 조회', async () => {
		const backups = await listBackupsFromR2()
		
		expect(Array.isArray(backups)).toBe(true)
		
		// 방금 업로드한 파일이 목록에 있는지 확인
		const uploadedFile = backups.find(b => b.filename === TEST_FILENAME)
		expect(uploadedFile).toBeDefined()
		if (uploadedFile) {
			expect(uploadedFile.size).toBeGreaterThan(0)
			expect(uploadedFile.lastModified).toBeInstanceOf(Date)
		}
	}, 30000)

	// 3. R2 다운로드 테스트
	it('R2에서 백업 다운로드', async () => {
		const buffer = await downloadBackupFromR2(TEST_FILENAME)
		
		expect(buffer).toBeInstanceOf(Buffer)
		expect(buffer.length).toBeGreaterThan(0)
		expect(buffer.length).toBe(1024) // 업로드한 파일 크기와 동일
	}, 30000)

	// 4. R2 삭제 테스트
	it('R2에서 백업 삭제', async () => {
		await deleteBackupFromR2(TEST_FILENAME)
		
		// 삭제 후 목록에서 사라졌는지 확인
		const backups = await listBackupsFromR2()
		const deletedFile = backups.find(b => b.filename === TEST_FILENAME)
		expect(deletedFile).toBeUndefined()
	}, 30000)
})

describe('R2 Backup Error Handling', () => {
	// 5. 존재하지 않는 파일 다운로드 시도
	it('존재하지 않는 파일 다운로드 시 에러', async () => {
		await expect(
			downloadBackupFromR2('nonexistent-file.db')
		).rejects.toThrow()
	}, 30000)

	// 6. 존재하지 않는 파일 삭제 시도
	it('존재하지 않는 파일 삭제 시 에러 (또는 무시)', async () => {
		// R2는 존재하지 않는 파일 삭제 시 에러를 던지지 않을 수 있음
		await expect(
			deleteBackupFromR2('nonexistent-file.db')
		).resolves.not.toThrow()
	}, 30000)
})
