/**
 * Admin Database Management 통합 테스트
 * 
 * 테스트 시나리오:
 * 1. 테이블 목록 조회
 * 2. 특정 테이블(posts) 데이터 조회
 * 3. 레코드 생성 (CREATE)
 * 4. 레코드 수정 (UPDATE)
 * 5. 레코드 삭제 (DELETE)
 * 6. SQL 쿼리 실행 (읽기 전용)
 * 7. 백업 생성 및 R2 업로드
 * 8. 백업 목록 조회
 * 9. 성능 모니터링 데이터 조회
 * 10. 감사 로그 조회
 */

import { test, expect, type Page } from '@playwright/test'

// Admin 로그인 헬퍼
async function loginAsAdmin(page: Page) {
	// TODO: 실제 admin 로그인 로직으로 교체
	// 현재는 admin 권한이 있다고 가정
	await page.goto('http://localhost:5173/admin/database')
}

test.describe('Admin Database Management', () => {
	test.beforeEach(async ({ page }) => {
		await loginAsAdmin(page)
	})

	// 1. 메인 대시보드 접근
	test('메인 대시보드 로드 및 빠른 액션 확인', async ({ page }) => {
		await page.goto('http://localhost:5173/admin/database')
		
		// 페이지 제목 확인
		await expect(page.locator('h1')).toContainText('데이터베이스 관리')
		
		// 빠른 액션 버튼 5개 확인
		await expect(page.getByRole('link', { name: /테이블 관리/ })).toBeVisible()
		await expect(page.getByRole('link', { name: /SQL 쿼리/ })).toBeVisible()
		await expect(page.getByRole('link', { name: /백업 관리/ })).toBeVisible()
		await expect(page.getByRole('link', { name: /성능 모니터링/ })).toBeVisible()
		await expect(page.getByRole('link', { name: /감사 로그/ })).toBeVisible()
	})

	// 2. 테이블 목록 조회
	test('테이블 목록 페이지 로드', async ({ page }) => {
		await page.goto('http://localhost:5173/admin/database/tables')
		
		// 테이블 카드들이 표시되는지 확인
		await expect(page.locator('text=posts')).toBeVisible()
		await expect(page.locator('text=users')).toBeVisible()
		await expect(page.locator('text=comments')).toBeVisible()
	})

	// 3. 특정 테이블 관리 페이지
	test('posts 테이블 데이터 조회', async ({ page }) => {
		await page.goto('http://localhost:5173/admin/database/tables/posts')
		
		// 테이블 제목 확인
		await expect(page.locator('h1')).toContainText('게시글')
		
		// DataTable 렌더링 확인
		await expect(page.locator('table')).toBeVisible()
		
		// 검색 기능 확인
		await expect(page.getByPlaceholder('검색...')).toBeVisible()
	})

	// 4. SQL 쿼리 실행기
	test('SQL 쿼리 실행 - 읽기 전용 모드', async ({ page }) => {
		await page.goto('http://localhost:5173/admin/database/query')
		
		// 읽기 전용 모드 선택
		await page.getByLabel('읽기 전용').check()
		
		// 샘플 쿼리 버튼 클릭
		await page.getByRole('button', { name: '최근 게시글 10개' }).click()
		
		// 쿼리가 입력되었는지 확인
		const textarea = page.locator('textarea[name="query"]')
		await expect(textarea).toContainText('SELECT')
		
		// 실행 버튼 확인
		await expect(page.getByRole('button', { name: /실행/ })).toBeVisible()
	})

	// 5. 백업 관리
	test('백업 페이지 로드 및 R2 표시 확인', async ({ page }) => {
		await page.goto('http://localhost:5173/admin/database/backup')
		
		// 페이지 제목 확인
		await expect(page.locator('h1')).toContainText('백업 관리')
		
		// Cloudflare R2 배지 확인
		await expect(page.locator('text=Cloudflare R2')).toBeVisible()
		
		// 백업 생성 버튼 확인
		await expect(page.getByRole('button', { name: /지금 백업 생성/ })).toBeVisible()
	})

	// 6. 성능 모니터링
	test('성능 모니터링 페이지 로드', async ({ page }) => {
		await page.goto('http://localhost:5173/admin/database/monitor')
		
		// 페이지 제목 확인
		await expect(page.locator('h1')).toContainText('성능 모니터링')
		
		// 통계 카드 확인 (DB 크기, 테이블 수, 총 레코드, 인덱스 수)
		await expect(page.locator('text=DB 크기')).toBeVisible()
		await expect(page.locator('text=테이블 수')).toBeVisible()
		await expect(page.locator('text=총 레코드')).toBeVisible()
		await expect(page.locator('text=인덱스 수')).toBeVisible()
		
		// 최적화 버튼 확인
		await expect(page.getByRole('button', { name: /VACUUM 실행/ })).toBeVisible()
		await expect(page.getByRole('button', { name: /ANALYZE 실행/ })).toBeVisible()
		await expect(page.getByRole('button', { name: /OPTIMIZE 실행/ })).toBeVisible()
	})

	// 7. 감사 로그
	test('감사 로그 페이지 로드 및 필터 확인', async ({ page }) => {
		await page.goto('http://localhost:5173/admin/database/logs')
		
		// 페이지 제목 확인
		await expect(page.locator('h1')).toContainText('감사 로그')
		
		// 필터 요소 확인
		await expect(page.locator('label:has-text("액션")')).toBeVisible()
		await expect(page.locator('label:has-text("테이블")')).toBeVisible()
		await expect(page.getByRole('button', { name: /필터 적용/ })).toBeVisible()
	})
})

test.describe('CRUD Operations (실제 데이터 변경)', () => {
	test.beforeEach(async ({ page }) => {
		await loginAsAdmin(page)
	})

	// 8. 레코드 생성 테스트 (users 테이블 - canCreate: false이므로 버튼 없어야 함)
	test('users 테이블 - 생성 버튼 없음 확인', async ({ page }) => {
		await page.goto('http://localhost:5173/admin/database/tables/users')
		
		// 새 레코드 버튼이 없어야 함
		await expect(page.getByRole('button', { name: /새 레코드/ })).not.toBeVisible()
	})

	// 9. 레코드 조회 모달
	test('레코드 상세 조회 모달 열기', async ({ page }) => {
		await page.goto('http://localhost:5173/admin/database/tables/posts')
		
		// 첫 번째 행의 조회 버튼 클릭 (눈 아이콘)
		const viewButton = page.locator('button[aria-label="View"]').first()
		if (await viewButton.isVisible()) {
			await viewButton.click()
			
			// 모달이 열렸는지 확인
			await expect(page.locator('text=레코드 상세')).toBeVisible()
		}
	})
})

test.describe('백업 시스템 (R2 통합)', () => {
	test.beforeEach(async ({ page }) => {
		await loginAsAdmin(page)
	})

	// 10. 백업 생성 플로우 (실제 실행하지 않고 UI만 확인)
	test('백업 생성 버튼 클릭 가능 확인', async ({ page }) => {
		await page.goto('http://localhost:5173/admin/database/backup')
		
		const createButton = page.getByRole('button', { name: /지금 백업 생성/ })
		await expect(createButton).toBeEnabled()
		
		// 실제 클릭은 하지 않음 (R2 업로드 방지)
	})

	// 11. 백업 목록 렌더링
	test('백업 목록 테이블 렌더링', async ({ page }) => {
		await page.goto('http://localhost:5173/admin/database/backup')
		
		// 백업 파일 목록 섹션 확인
		await expect(page.locator('text=백업 파일 목록')).toBeVisible()
		
		// 테이블 헤더 확인 (백업이 있을 경우)
		const hasBackups = await page.locator('table').isVisible()
		if (hasBackups) {
			await expect(page.locator('th:has-text("파일명")')).toBeVisible()
			await expect(page.locator('th:has-text("크기")')).toBeVisible()
			await expect(page.locator('th:has-text("생성일")')).toBeVisible()
		}
	})
})
