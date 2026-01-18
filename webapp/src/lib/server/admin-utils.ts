/**
 * Admin Database 유틸리티 함수
 * 
 * 공통으로 사용되는 헬퍼 함수들을 모아둔 파일
 */

/**
 * 바이트를 사람이 읽기 쉬운 형식으로 변환
 * @param bytes - 바이트 수
 * @returns 포맷팅된 문자열 (예: "1.5 MB")
 */
export function formatBytes(bytes: number): string {
	if (bytes === 0) return '0 Bytes'
	const k = 1024
	const sizes = ['Bytes', 'KB', 'MB', 'GB']
	const i = Math.floor(Math.log(bytes) / Math.log(k))
	return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i]
}

/**
 * SQL 쿼리가 SELECT 쿼리인지 확인
 * @param query - SQL 쿼리 문자열
 * @returns SELECT 쿼리 여부
 */
export function isSelectQuery(query: string): boolean {
	return query.trim().toUpperCase().startsWith('SELECT')
}

/**
 * 위험한 SQL 쿼리 패턴 감지
 * @param query - SQL 쿼리 문자열
 * @returns 위험한 쿼리 여부
 */
export function isDangerousQuery(query: string): boolean {
	const DANGEROUS_PATTERNS = [
		/DROP\s+TABLE/i,
		/DROP\s+DATABASE/i,
		/TRUNCATE/i,
		/DELETE\s+FROM\s+\w+\s*;?\s*$/i, // WHERE 절 없는 DELETE
		/UPDATE\s+\w+\s+SET\s+[^W]*$/i // WHERE 절 없는 UPDATE
	]
	
	return DANGEROUS_PATTERNS.some(pattern => pattern.test(query.trim()))
}

/**
 * 백업 파일명 생성
 * @returns 타임스탬프가 포함된 백업 파일명
 */
export function createBackupFilename(): string {
	const timestamp = new Date().toISOString().replace(/[:.]/g, '-').split('T').join('_')
	return `backup_${timestamp}.db`
}

/**
 * R2 키 생성
 * @param filename - 파일명
 * @returns R2 키 (backups/ 접두사 포함)
 */
export function createR2Key(filename: string): string {
	return `backups/${filename}`
}

/**
 * 파일명에서 경로 탐색 시도 감지
 * @param filename - 파일명
 * @returns 안전한 파일명 여부
 */
export function isSafeFilename(filename: string): boolean {
	const hasPathTraversal = filename.includes('..')
	const hasCommandInjection = filename.includes(';') || filename.includes('&&')
	const hasNullByte = filename.includes('\x00')
	
	return !(hasPathTraversal || hasCommandInjection || hasNullByte)
}
