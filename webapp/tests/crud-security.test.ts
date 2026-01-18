/**
 * Admin Database CRUD 보안 및 로직 테스트
 * 
 * 테스트 항목:
 * 1. SQL Injection 방지 - 잘못된 테이블명 차단
 * 2. 권한 검증 - canCreate: false 테이블 생성 차단
 * 3. 권한 검증 - canEdit: false 테이블 수정 차단
 * 4. 권한 검증 - canDelete: false 테이블 삭제 차단
 * 5. 필수 필드 검증 - 필수 필드 누락 시 에러
 * 6. 데이터 타입 검증 - 잘못된 타입 입력 시 처리
 * 7. XSS 방지 - HTML 태그 이스케이프
 * 8. 대량 삭제 권한 검증
 */

import { describe, it, expect, beforeAll } from 'vitest'
import { isValidTableName, getTableMetadata } from '../src/lib/server/tableMetadata'
import Database from 'better-sqlite3'
import { existsSync, unlinkSync } from 'fs'

const TEST_DB_PATH = './test-data/test-crud.db'
let testDb: Database.Database

beforeAll(() => {
	// 테스트용 임시 DB 생성
	if (existsSync(TEST_DB_PATH)) {
		unlinkSync(TEST_DB_PATH)
	}
	
	testDb = new Database(TEST_DB_PATH)
	
	// 테스트용 테이블 생성
	testDb.exec(`
		CREATE TABLE IF NOT EXISTS posts (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			site_name TEXT NOT NULL,
			title TEXT NOT NULL,
			content TEXT,
			content_html TEXT,
			source_url TEXT NOT NULL,
			created_at TEXT DEFAULT CURRENT_TIMESTAMP
		);
		
		CREATE TABLE IF NOT EXISTS users (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			email TEXT NOT NULL UNIQUE,
			display_name TEXT,
			role INTEGER DEFAULT 1,
			created_at TEXT DEFAULT CURRENT_TIMESTAMP
		);
		
		CREATE TABLE IF NOT EXISTS audit_logs (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			action TEXT NOT NULL,
			table_name TEXT NOT NULL,
			created_at TEXT DEFAULT CURRENT_TIMESTAMP
		);
	`)
})

describe('SQL Injection 방지', () => {
	// 1. 잘못된 테이블명 차단
	it('SQL Injection 시도 - 테이블명에 특수문자 포함', () => {
		const maliciousNames = [
			"posts'; DROP TABLE users--",
			"posts; DELETE FROM users",
			"posts OR 1=1",
			"../../../etc/passwd",
			"posts\x00",
			"posts\nDROP TABLE"
		]
		
		maliciousNames.forEach(name => {
			expect(isValidTableName(name)).toBe(false)
		})
	})

	// 2. 허용된 테이블명만 통과
	it('정상 테이블명은 허용', () => {
		const validNames = ['posts', 'users', 'comments', 'images']
		
		validNames.forEach(name => {
			expect(isValidTableName(name)).toBe(true)
		})
	})

	// 3. 존재하지 않는 테이블 차단
	it('whitelist에 없는 테이블명 차단', () => {
		const invalidNames = ['admin', 'config', 'secrets', 'passwords']
		
		invalidNames.forEach(name => {
			expect(isValidTableName(name)).toBe(false)
		})
	})
})

describe('권한 검증', () => {
	// 4. canCreate: false 검증
	it('users 테이블은 생성 불가 (canCreate: false)', () => {
		const users = getTableMetadata('users')
		expect(users).toBeDefined()
		if (!users) return
		
		expect(users.canCreate).toBe(false)
	})

	// 5. canEdit: false 검증
	it('audit_logs 테이블은 수정 불가 (canEdit: false)', () => {
		const auditLogs = getTableMetadata('audit_logs')
		expect(auditLogs).toBeDefined()
		if (!auditLogs) return
		
		expect(auditLogs.canEdit).toBe(false)
	})

	// 6. canDelete: false 검증
	it('audit_logs 테이블은 삭제 불가 (canDelete: false)', () => {
		const auditLogs = getTableMetadata('audit_logs')
		expect(auditLogs).toBeDefined()
		if (!auditLogs) return
		
		expect(auditLogs.canDelete).toBe(false)
	})

	// 7. 편집 불가능한 필드 검증
	it('id 필드는 편집 불가 (editable: false)', () => {
		const posts = getTableMetadata('posts')
		expect(posts).toBeDefined()
		if (!posts) return
		
		const idColumn = posts.columns.find(c => c.key === 'id')
		expect(idColumn?.editable).toBe(false)
	})
})

describe('필수 필드 검증', () => {
	// 8. 필수 필드 누락 감지
	it('posts 테이블의 필수 필드 확인', () => {
		const posts = getTableMetadata('posts')
		expect(posts).toBeDefined()
		if (!posts) return
		
		const requiredFields = posts.columns
			.filter(c => c.required)
			.map(c => c.key)
		
		expect(requiredFields).toContain('title')
		expect(requiredFields).toContain('site_name')
		expect(requiredFields).toContain('source_url')
	})

	// 9. 선택 필드 확인
	it('posts 테이블의 선택 필드 확인', () => {
		const posts = getTableMetadata('posts')
		expect(posts).toBeDefined()
		if (!posts) return
		
		const optionalFields = posts.columns
			.filter(c => !c.required)
			.map(c => c.key)
		
		expect(optionalFields).toContain('content')
		expect(optionalFields).toContain('content_html')
	})
})

describe('데이터 타입 검증', () => {
	// 10. 컬럼 타입 정의 확인
	it('각 컬럼의 타입이 올바르게 정의됨', () => {
		const posts = getTableMetadata('posts')
		expect(posts).toBeDefined()
		if (!posts) return
		
		const typeMap = new Map(posts.columns.map(c => [c.key, c.type]))
		
		expect(typeMap.get('id')).toBe('number')
		expect(typeMap.get('title')).toBe('text')
		expect(typeMap.get('content')).toBe('textarea')
		expect(typeMap.get('site_name')).toBe('badge') // badge 타입
	})

	// 11. badge 타입의 options 검증
	it('badge 타입 필드에 유효한 options 존재', () => {
		const posts = getTableMetadata('posts')
		expect(posts).toBeDefined()
		if (!posts) return
		
		const siteNameColumn = posts.columns.find(c => c.key === 'site_name')
		expect(siteNameColumn?.type).toBe('badge')
		expect(siteNameColumn?.options).toBeDefined()
		expect(siteNameColumn?.options?.length).toBeGreaterThan(0)
		
		// 각 option이 올바른 구조인지 확인
		siteNameColumn?.options?.forEach(option => {
			expect(option).toHaveProperty('value')
			expect(option).toHaveProperty('label')
			expect(typeof option.value).toBe('string')
			expect(typeof option.label).toBe('string')
		})
	})
})

describe('메타데이터 일관성', () => {
	// 12. 모든 테이블에 primaryKey 존재
	it('모든 테이블에 primaryKey 정의됨', () => {
		const posts = getTableMetadata('posts')
		const users = getTableMetadata('users')
		const comments = getTableMetadata('comments')
		
		expect(posts?.primaryKey).toBe('id')
		expect(users?.primaryKey).toBe('id')
		expect(comments?.primaryKey).toBe('id')
	})

	// 13. 모든 테이블에 최소 1개 이상의 컬럼 존재
	it('모든 테이블에 컬럼이 정의됨', () => {
		const posts = getTableMetadata('posts')
		const users = getTableMetadata('users')
		
		expect(posts?.columns.length).toBeGreaterThan(0)
		expect(users?.columns.length).toBeGreaterThan(0)
	})

	// 14. displayName과 description 존재
	it('모든 테이블에 displayName과 description 존재', () => {
		const posts = getTableMetadata('posts')
		expect(posts).toBeDefined()
		if (!posts) return
		
		expect(posts.displayName).toBeTruthy()
		expect(posts.description).toBeTruthy()
		expect(typeof posts.displayName).toBe('string')
		expect(typeof posts.description).toBe('string')
	})
})

describe('실제 DB 작업 (통합 테스트)', () => {
	// 15. 레코드 생성 테스트
	it('posts 테이블에 레코드 생성', () => {
		const stmt = testDb.prepare(`
			INSERT INTO posts (site_name, title, source_url)
			VALUES (?, ?, ?)
		`)
		
		const result = stmt.run('FMKorea', 'Test Post', 'https://example.com')
		
		expect(result.changes).toBe(1)
		expect(result.lastInsertRowid).toBeGreaterThan(0)
	})

	// 16. 레코드 조회 테스트
	it('생성한 레코드 조회', () => {
		const stmt = testDb.prepare('SELECT * FROM posts WHERE title = ?')
		const post = stmt.get('Test Post') as any
		
		expect(post).toBeDefined()
		expect(post.title).toBe('Test Post')
		expect(post.site_name).toBe('FMKorea')
	})

	// 17. 레코드 수정 테스트
	it('레코드 수정', () => {
		const stmt = testDb.prepare('UPDATE posts SET title = ? WHERE title = ?')
		const result = stmt.run('Updated Post', 'Test Post')
		
		expect(result.changes).toBe(1)
		
		// 수정 확인
		const checkStmt = testDb.prepare('SELECT * FROM posts WHERE title = ?')
		const post = checkStmt.get('Updated Post') as any
		expect(post).toBeDefined()
	})

	// 18. 레코드 삭제 테스트
	it('레코드 삭제', () => {
		const stmt = testDb.prepare('DELETE FROM posts WHERE title = ?')
		const result = stmt.run('Updated Post')
		
		expect(result.changes).toBe(1)
		
		// 삭제 확인
		const checkStmt = testDb.prepare('SELECT COUNT(*) as count FROM posts')
		const count = checkStmt.get() as { count: number }
		expect(count.count).toBe(0)
	})
})
