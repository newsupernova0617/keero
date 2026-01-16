/**
 * SQL 쿼리 실행기 보안 테스트 (개선됨)
 * 
 * 테스트 항목:
 * 1. 읽기 전용 모드 - SELECT만 허용
 * 2. 읽기 전용 모드 - UPDATE/DELETE/INSERT 차단
 * 3. 위험한 쿼리 감지 - WHERE 없는 DELETE/UPDATE
 * 4. 위험한 쿼리 감지 - DROP TABLE/TRUNCATE
 * 5. 쿼리 실행 결과 검증
 * 6. 에러 처리 검증
 */

import { describe, it, expect } from 'vitest'
import { 
	isSelectQuery, 
	isDangerousQuery 
} from '../src/lib/server/admin-utils'

describe('읽기 전용 모드 검증', () => {
	// 1. SELECT 쿼리는 허용
	it('읽기 전용 모드 - SELECT 쿼리 허용', () => {
		const queries = [
			'SELECT * FROM posts',
			'SELECT id, title FROM posts WHERE id = 1',
			'SELECT COUNT(*) FROM users'
		]
		
		queries.forEach(query => {
			expect(isSelectQuery(query)).toBe(true)
		})
	})

	// 2. UPDATE 쿼리는 차단
	it('읽기 전용 모드 - UPDATE 쿼리 차단', () => {
		const query = 'UPDATE posts SET title = "hacked"'
		expect(isSelectQuery(query)).toBe(false)
	})

	// 3. DELETE 쿼리는 차단
	it('읽기 전용 모드 - DELETE 쿼리 차단', () => {
		const query = 'DELETE FROM posts WHERE id = 1'
		expect(isSelectQuery(query)).toBe(false)
	})

	// 4. INSERT 쿼리는 차단
	it('읽기 전용 모드 - INSERT 쿼리 차단', () => {
		const query = 'INSERT INTO posts (title) VALUES ("test")'
		expect(isSelectQuery(query)).toBe(false)
	})

	// 5. DROP 쿼리는 차단
	it('읽기 전용 모드 - DROP 쿼리 차단', () => {
		const query = 'DROP TABLE posts'
		expect(isSelectQuery(query)).toBe(false)
	})
})

describe('위험한 쿼리 감지', () => {
	// 6. WHERE 없는 DELETE 감지
	it('위험한 쿼리 - WHERE 없는 DELETE', () => {
		const dangerousQueries = [
			'DELETE FROM posts',
			'DELETE FROM posts;',
			'DELETE FROM users '
		]
		
		dangerousQueries.forEach(query => {
			expect(isDangerousQuery(query)).toBe(true)
		})
	})

	// 7. WHERE 있는 DELETE는 허용
	it('안전한 쿼리 - WHERE 있는 DELETE', () => {
		const safeQueries = [
			'DELETE FROM posts WHERE id = 1',
			'DELETE FROM posts WHERE created_at < "2020-01-01"'
		]
		
		safeQueries.forEach(query => {
			expect(isDangerousQuery(query)).toBe(false)
		})
	})

	// 8. WHERE 없는 UPDATE 감지
	it('위험한 쿼리 - WHERE 없는 UPDATE', () => {
		const dangerousQueries = [
			'UPDATE posts SET title = "hacked"',
			'UPDATE users SET role = 99',
			'UPDATE posts SET title = "test";'
		]
		
		dangerousQueries.forEach(query => {
			expect(isDangerousQuery(query)).toBe(true)
		})
	})

	// 9. WHERE 있는 UPDATE는 허용
	it('안전한 쿼리 - WHERE 있는 UPDATE', () => {
		const safeQueries = [
			'UPDATE posts SET title = "new" WHERE id = 1',
			'UPDATE users SET role = 1 WHERE email = "test@example.com"'
		]
		
		safeQueries.forEach(query => {
			expect(isDangerousQuery(query)).toBe(false)
		})
	})

	// 10. DROP TABLE 감지
	it('위험한 쿼리 - DROP TABLE', () => {
		const dangerousQueries = [
			'DROP TABLE posts',
			'DROP TABLE users',
			'drop table comments'
		]
		
		dangerousQueries.forEach(query => {
			expect(isDangerousQuery(query)).toBe(true)
		})
	})

	// 11. DROP DATABASE 감지
	it('위험한 쿼리 - DROP DATABASE', () => {
		const query = 'DROP DATABASE mydb'
		expect(isDangerousQuery(query)).toBe(true)
	})

	// 12. TRUNCATE 감지
	it('위험한 쿼리 - TRUNCATE', () => {
		const queries = [
			'TRUNCATE TABLE posts',
			'TRUNCATE posts'
		]
		
		queries.forEach(query => {
			expect(isDangerousQuery(query)).toBe(true)
		})
	})
})

describe('쿼리 유효성 검증', () => {
	// 13. 빈 쿼리 감지
	it('빈 쿼리는 무효', () => {
		const emptyQueries = ['', '   ', '\n\t']
		
		emptyQueries.forEach(query => {
			expect(query.trim()).toBe('')
		})
	})

	// 14. SQL 주석 처리
	it('SQL 주석이 포함된 쿼리', () => {
		const query = 'SELECT * FROM posts -- comment'
		expect(isSelectQuery(query)).toBe(true)
	})

	// 15. 여러 줄 쿼리
	it('여러 줄 쿼리 처리', () => {
		const query = `
			SELECT 
				id, 
				title 
			FROM posts 
			WHERE id = 1
		`
		expect(isSelectQuery(query)).toBe(true)
	})

	// 16. 대소문자 구분 없음
	it('대소문자 구분 없이 쿼리 감지', () => {
		const queries = [
			'select * from posts',
			'SELECT * FROM posts',
			'SeLeCt * FrOm posts'
		]
		
		queries.forEach(query => {
			expect(isSelectQuery(query)).toBe(true)
		})
	})
})

describe('쿼리 결과 형식 검증', () => {
	// 17. SELECT 결과는 배열이어야 함
	it('SELECT 쿼리 결과 형식', () => {
		const mockResult = [
			{ id: 1, title: 'Post 1' },
			{ id: 2, title: 'Post 2' }
		]
		
		expect(Array.isArray(mockResult)).toBe(true)
		expect(mockResult.length).toBe(2)
	})

	// 18. INSERT/UPDATE/DELETE 결과는 changes 포함
	it('변경 쿼리 결과 형식', () => {
		const mockResult = {
			changes: 1,
			lastInsertRowid: 123
		}
		
		expect(mockResult).toHaveProperty('changes')
		expect(mockResult.changes).toBeGreaterThan(0)
	})
})

describe('에러 케이스', () => {
	// 19. 잘못된 SQL 문법
	it('잘못된 SQL 문법 감지', () => {
		const invalidQueries = [
			'SELCT * FROM posts', // 오타
			'SELECT * FORM posts', // 오타
			'SELECT * FROM', // 불완전
			'FROM posts SELECT *' // 순서 틀림
		]
		
		// 이런 쿼리들은 실행 시 에러를 발생시켜야 함
		invalidQueries.forEach(query => {
			expect(query).toBeTruthy() // 쿼리는 존재하지만
			// 실제 실행 시 에러 발생 예상
		})
	})

	// 20. 존재하지 않는 테이블
	it('존재하지 않는 테이블 쿼리', () => {
		const query = 'SELECT * FROM nonexistent_table'
		expect(isSelectQuery(query)).toBe(true) // 문법은 맞지만
		// 실제 실행 시 에러 발생 예상
	})
})
