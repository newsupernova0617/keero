/**
 * 백업 유틸리티 함수 테스트 (실제 함수)
 * 
 * 테스트 항목:
 * 1. createBackupFilename - 백업 파일명 생성
 * 2. createR2Key - R2 키 생성
 * 3. isSafeFilename - 안전한 파일명 검증
 * 4. formatBytes - 바이트 포맷팅
 */

import { describe, it, expect } from 'vitest'
import { 
	createBackupFilename, 
	createR2Key, 
	isSafeFilename,
	formatBytes
} from '../src/lib/server/admin-utils'

describe('백업 파일명 생성 (실제 함수)', () => {
	// 1. 백업 파일명 형식 검증
	it('타임스탬프 형식의 백업 파일명 생성', () => {
		const filename = createBackupFilename()
		
		// backup_YYYY-MM-DD_HH-MM-SS...db 형식
		expect(filename).toMatch(/^backup_\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}.*\.db$/)
		expect(filename).toContain('backup_')
		expect(filename).toMatch(/\.db$/)
	})

	// 2. 매번 다른 파일명 생성
	it('연속 호출 시 다른 파일명 생성', async () => {
		const filename1 = createBackupFilename()
		// 밀리초 단위 차이를 위해 약간 대기
		await new Promise(resolve => setTimeout(resolve, 10))
		const filename2 = createBackupFilename()
		
		// 타임스탬프가 다르므로 파일명도 달라야 함
		expect(filename1).not.toBe(filename2)
	})
})

describe('R2 키 생성 (실제 함수)', () => {
	// 3. R2 키 형식 검증
	it('backups/ 접두사 포함', () => {
		const key = createR2Key('test.db')
		
		expect(key).toBe('backups/test.db')
		expect(key.startsWith('backups/')).toBe(true)
	})

	// 4. 다양한 파일명 처리
	it('다양한 파일명으로 키 생성', () => {
		expect(createR2Key('backup_2026-01-16.db')).toBe('backups/backup_2026-01-16.db')
		expect(createR2Key('temp.db')).toBe('backups/temp.db')
	})
})

describe('안전한 파일명 검증 (실제 함수)', () => {
	// 5. 경로 탐색 시도 감지
	it('경로 탐색 시도 차단', () => {
		expect(isSafeFilename('../../../etc/passwd')).toBe(false)
		expect(isSafeFilename('../../backup.db')).toBe(false)
		expect(isSafeFilename('normal.db')).toBe(true)
	})

	// 6. 명령어 주입 시도 감지
	it('명령어 주입 시도 차단', () => {
		expect(isSafeFilename('backup.db; rm -rf /')).toBe(false)
		expect(isSafeFilename('backup.db && cat /etc/passwd')).toBe(false)
		expect(isSafeFilename('backup.db')).toBe(true)
	})

	// 7. Null byte 공격 감지
	it('Null byte 공격 차단', () => {
		expect(isSafeFilename('backup\x00.db')).toBe(false)
		expect(isSafeFilename('normal.db')).toBe(true)
	})
})

describe('바이트 포맷팅 (실제 함수)', () => {
	// 8. Bytes 단위
	it('1KB 미만은 Bytes로 표시', () => {
		expect(formatBytes(0)).toBe('0 Bytes')
		expect(formatBytes(512)).toBe('512 Bytes')
		expect(formatBytes(1023)).toBe('1023 Bytes')
	})

	// 9. KB 단위
	it('1KB 이상은 KB로 표시', () => {
		expect(formatBytes(1024)).toBe('1 KB')
		expect(formatBytes(2048)).toBe('2 KB')
		expect(formatBytes(1536)).toBe('1.5 KB')
	})

	// 10. MB 단위
	it('1MB 이상은 MB로 표시', () => {
		expect(formatBytes(1048576)).toBe('1 MB')
		expect(formatBytes(2097152)).toBe('2 MB')
	})

	// 11. GB 단위
	it('1GB 이상은 GB로 표시', () => {
		expect(formatBytes(1073741824)).toBe('1 GB')
	})
})
