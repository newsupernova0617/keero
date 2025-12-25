import { expect, test } from '@playwright/test';

/**
 * 게시글 목록 및 상세 E2E 테스트
 */

test.describe('게시글 기능', () => {
	test('메인 페이지 로드 및 게시글 목록 표시', async ({ page }) => {
		await page.goto('/');

		// 헤더 확인
		await expect(page.locator('h1')).toBeVisible();

		// 게시글 카드가 표시되는지 확인
		const postCards = page.locator('article, .post-card, a[href^="/post/"]').first();
		await expect(postCards).toBeVisible({ timeout: 10000 });
	});

	test('게시글 상세 페이지 접근', async ({ page }) => {
		await page.goto('/');

		// 첫 번째 게시글 클릭
		const firstPost = page.locator('a[href^="/post/"]').first();
		await firstPost.click();

		// URL이 /post/[id] 형식인지 확인
		await expect(page).toHaveURL(/\/post\/\d+/);

		// 게시글 제목이 표시되는지 확인
		await expect(page.locator('h1, h2').first()).toBeVisible();
	});

	test('게시글 내용 및 이미지 표시', async ({ page }) => {
		// 게시글이 있다고 가정하고 직접 접근
		await page.goto('/');
		
		const firstPost = page.locator('a[href^="/post/"]').first();
		if (await firstPost.count() > 0) {
			await firstPost.click();

			// 게시글 내용 확인
			const content = page.locator('.content, [class*="content"]').first();
			await expect(content).toBeVisible({ timeout: 5000 });
		}
	});

	test('뒤로가기 버튼 작동', async ({ page }) => {
		await page.goto('/');
		
		const firstPost = page.locator('a[href^="/post/"]').first();
		if (await firstPost.count() > 0) {
			await firstPost.click();
			await page.waitForURL(/\/post\/\d+/);

			// 뒤로가기 버튼 클릭
			const backButton = page.locator('button:has-text("뒤로"), a:has-text("뒤로")').first();
			if (await backButton.count() > 0) {
				await backButton.click();
				await expect(page).toHaveURL('/');
			}
		}
	});
});

test.describe('페이지네이션', () => {
	test('더 보기 버튼 작동', async ({ page }) => {
		await page.goto('/');

		// 더 보기 버튼 찾기
		const loadMoreButton = page.locator('button:has-text("더 보기"), button:has-text("Load More")');
		
		if (await loadMoreButton.count() > 0) {
			const initialPostCount = await page.locator('a[href^="/post/"]').count();
			
			await loadMoreButton.click();
			await page.waitForTimeout(1000);

			const newPostCount = await page.locator('a[href^="/post/"]').count();
			expect(newPostCount).toBeGreaterThan(initialPostCount);
		}
	});
});
