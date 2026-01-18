/**
 * 테이블 메타데이터 시스템 테스트 (개선됨)
 * 
 * 테스트 항목:
 * 1. getAllTables - 모든 테이블 메타데이터 조회
 * 2. getTableMetadata - 특정 테이블 메타데이터 조회
 * 3. 컬럼 타입 검증
 * 4. 권한 설정 검증 (canCreate, canEdit, canDelete)
 * 5. select/badge 타입 options 검증
 */

import { describe, it, expect } from 'vitest'
import { getAllTables, getTableMetadata } from '../src/lib/server/tableMetadata'

describe('Table Metadata System', () => {
	// 1. 전체 테이블 목록 조회
	it('모든 테이블 메타데이터 조회', () => {
		const tables = getAllTables()
		
		expect(Array.isArray(tables)).toBe(true)
		expect(tables.length).toBeGreaterThan(0)
		
		// 필수 테이블 존재 확인
		const tableNames = tables.map(t => t.name)
		expect(tableNames).toContain('posts')
		expect(tableNames).toContain('users')
		expect(tableNames).toContain('comments')
		expect(tableNames).toContain('images')
	})

	// 2. posts 테이블 메타데이터
	it('posts 테이블 메타데이터 구조 검증', () => {
		const posts = getTableMetadata('posts')
		
		expect(posts).toBeDefined()
		if (!posts) return
		
		expect(posts.name).toBe('posts')
		expect(posts.displayName).toBe('게시글')
		expect(posts.primaryKey).toBe('id')
		expect(Array.isArray(posts.columns)).toBe(true)
		
		// 주요 컬럼 존재 확인
		const columnKeys = posts.columns.map(c => c.key)
		expect(columnKeys).toContain('id')
		expect(columnKeys).toContain('title')
		expect(columnKeys).toContain('content')
		expect(columnKeys).toContain('site_name')
	})

	// 3. users 테이블 권한 검증
	it('users 테이블 권한 설정 확인', () => {
		const users = getTableMetadata('users')
		
		expect(users).toBeDefined()
		if (!users) return
		
		expect(users.canCreate).toBe(false) // 사용자는 직접 생성 불가
		expect(users.canEdit).toBe(true)
		expect(users.canDelete).toBe(true)
	})

	// 4. 컬럼 타입 검증
	it('컬럼 타입이 올바르게 정의됨', () => {
		const posts = getTableMetadata('posts')
		
		expect(posts).toBeDefined()
		if (!posts) return
		
		const idColumn = posts.columns.find(c => c.key === 'id')
		expect(idColumn?.type).toBe('number')
		expect(idColumn?.editable).toBe(false)
		
		const titleColumn = posts.columns.find(c => c.key === 'title')
		expect(titleColumn?.type).toBe('text')
		expect(titleColumn?.required).toBe(true)
		
		const contentColumn = posts.columns.find(c => c.key === 'content')
		expect(contentColumn?.type).toBe('textarea')
	})

	// 5. badge 타입 컬럼의 options 검증
	it('badge 타입 컬럼에 options 존재', () => {
		const posts = getTableMetadata('posts')
		
		expect(posts).toBeDefined()
		if (!posts) return
		
		const siteNameColumn = posts.columns.find(c => c.key === 'site_name')
		expect(siteNameColumn?.type).toBe('badge')
		expect(Array.isArray(siteNameColumn?.options)).toBe(true)
		expect(siteNameColumn?.options?.length).toBeGreaterThan(0)
	})
})
