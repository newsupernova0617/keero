import { expect, test } from '@playwright/test';

/**
 * 좋아요 기능 E2E 테스트
 */

const TEST_EMAIL = process.env.TEST_USER_EMAIL || 'test@example.com';
const TEST_PASSWORD = process.env.TEST_USER_PASSWORD || 'testpassword123';

test.describe('좋아요 기능 (로그인)', () => {
	test.beforeEach(async ({ page }) => {
		// 로그인
		await page.goto('/login');
		const emailInput = page.locator('input[type="email"]');
		if (await emailInput.count() > 0) {
			await emailInput.fill(TEST_EMAIL);
			await page.locator('input[type="password"]').fill(TEST_PASSWORD);
			await page.locator('button[type="submit"]').click();
			await page.waitForURL('/');
		}
	});

	test('게시글 좋아요 토글', async ({ page }) => {
		await page.goto('/');
		
		const firstPost = page.locator('a[href^="/post/"]').first();
		await firstPost.click();
		await page.waitForURL(/\/post\/\d+/);

		// 좋아요 버튼 찾기
		const likeButton = page.locator('button:has-text("좋아요"), button[aria-label*="like"], button:has([class*="thumb"])').first();
		
		if (await likeButton.count() > 0) {
			// 현재 좋아요 수 확인
			const likeCountElement = page.locator('[class*="like"], [data-testid="like-count"]').first();
			const initialCount = await likeCountElement.textContent();

			// 좋아요 클릭
			await likeButton.click();
			await page.waitForTimeout(1000);

			// 좋아요 수 변경 확인
			const newCount = await likeCountElement.textContent();
			expect(newCount).not.toBe(initialCount);

			// 다시 클릭 (좋아요 취소)
			await likeButton.click();
			await page.waitForTimeout(1000);

			// 원래 수로 돌아왔는지 확인
			const finalCount = await likeCountElement.textContent();
			expect(finalCount).toBe(initialCount);
		}
	});

	test('좋아요 상태 시각적 피드백', async ({ page }) => {
		await page.goto('/');
		
		const firstPost = page.locator('a[href^="/post/"]').first();
		await firstPost.click();
		await page.waitForURL(/\/post\/\d+/);

		const likeButton = page.locator('button:has-text("좋아요"), button[aria-label*="like"]').first();
		
		if (await likeButton.count() > 0) {
			// 초기 상태 확인
			const initialClass = await likeButton.getAttribute('class');

			// 좋아요 클릭
			await likeButton.click();
			await page.waitForTimeout(500);

			// 클래스 변경 확인 (활성화 상태)
			const activeClass = await likeButton.getAttribute('class');
			expect(activeClass).not.toBe(initialClass);

			// 다시 클릭
			await likeButton.click();
			await page.waitForTimeout(500);

			// 원래 상태로 돌아왔는지 확인
			const finalClass = await likeButton.getAttribute('class');
			expect(finalClass).toBe(initialClass);
		}
	});

	test('댓글 좋아요', async ({ page }) => {
		await page.goto('/');
		
		const firstPost = page.locator('a[href^="/post/"]').first();
		await firstPost.click();
		await page.waitForURL(/\/post\/\d+/);

		// 댓글 섹션으로 스크롤
		const commentsSection = page.locator('#comments').first();
		await commentsSection.scrollIntoViewIfNeeded();

		// 첫 번째 댓글의 좋아요 버튼
		const commentLikeButton = page.locator('.comment button:has-text("좋아요"), .comment button[aria-label*="like"]').first();
		
		if (await commentLikeButton.count() > 0) {
			// 좋아요 클릭
			await commentLikeButton.click();
			await page.waitForTimeout(1000);

			// 좋아요 수 증가 확인
			const likeCount = page.locator('.comment [class*="like-count"]').first();
			const count = await likeCount.textContent();
			expect(parseInt(count || '0')).toBeGreaterThanOrEqual(1);
		}
	});
});

test.describe('좋아요 기능 (비로그인)', () => {
	test('비로그인 시 좋아요 클릭하면 로그인 페이지로', async ({ page }) => {
		await page.goto('/');
		
		const firstPost = page.locator('a[href^="/post/"]').first();
		if (await firstPost.count() > 0) {
			await firstPost.click();
			await page.waitForURL(/\/post\/\d+/);

			const likeButton = page.locator('button:has-text("좋아요"), button[aria-label*="like"]').first();
			
			if (await likeButton.count() > 0) {
				await likeButton.click();
				await page.waitForTimeout(1000);

				// 로그인 페이지로 리다이렉트되었는지 확인
				const currentUrl = page.url();
				expect(currentUrl).toMatch(/login/);
			}
		}
	});
});

test.describe('좋아요 수 표시', () => {
	test('게시글 좋아요 수 표시', async ({ page }) => {
		await page.goto('/');
		
		const firstPost = page.locator('a[href^="/post/"]').first();
		await firstPost.click();
		await page.waitForURL(/\/post\/\d+/);

		// 좋아요 수 요소 확인
		const likeCount = page.locator('[class*="like"], [data-testid="like-count"]').first();
		await expect(likeCount).toBeVisible({ timeout: 5000 });

		// 숫자 형식인지 확인
		const countText = await likeCount.textContent();
		expect(countText).toMatch(/\d+/);
	});

	test('메인 페이지에서 좋아요 수 표시', async ({ page }) => {
		await page.goto('/');

		// 게시글 카드의 좋아요 수 확인
		const likeCountElements = page.locator('[class*="like-count"], [data-testid="like-count"]');
		
		if (await likeCountElements.count() > 0) {
			const firstLikeCount = likeCountElements.first();
			await expect(firstLikeCount).toBeVisible();

			const countText = await firstLikeCount.textContent();
			expect(countText).toMatch(/\d+/);
		}
	});
});
