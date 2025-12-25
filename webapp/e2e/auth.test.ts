import { expect, test } from '@playwright/test';

/**
 * 인증 흐름 E2E 테스트
 */

const TEST_EMAIL = process.env.TEST_USER_EMAIL || 'test@example.com';
const TEST_PASSWORD = process.env.TEST_USER_PASSWORD || 'testpassword123';

test.describe('로그인/로그아웃', () => {
	test('로그인 페이지 접근', async ({ page }) => {
		await page.goto('/login');

		// 로그인 폼 확인
		await expect(page.locator('input[type="email"]')).toBeVisible();
		await expect(page.locator('input[type="password"]')).toBeVisible();
		await expect(page.locator('button[type="submit"]')).toBeVisible();
	});

	test('이메일 로그인', async ({ page }) => {
		await page.goto('/login');

		// 이메일 입력
		await page.locator('input[type="email"]').fill(TEST_EMAIL);
		
		// 비밀번호 입력
		await page.locator('input[type="password"]').fill(TEST_PASSWORD);
		
		// 로그인 버튼 클릭
		await page.locator('button[type="submit"]').click();
		
		// 메인 페이지로 리다이렉트 확인
		await expect(page).toHaveURL('/', { timeout: 10000 });
		
		// 사용자 메뉴 또는 프로필 아이콘 확인
		const userMenu = page.locator('[data-testid="user-menu"], button:has-text("로그아웃"), [class*="user"]');
		await expect(userMenu.first()).toBeVisible({ timeout: 5000 });
	});

	test('잘못된 비밀번호로 로그인 실패', async ({ page }) => {
		await page.goto('/login');

		await page.locator('input[type="email"]').fill(TEST_EMAIL);
		await page.locator('input[type="password"]').fill('wrongpassword123');
		await page.locator('button[type="submit"]').click();

		// 에러 메시지 확인
		const errorMessage = page.locator('text=/잘못|실패|오류|error|invalid/i');
		await expect(errorMessage.first()).toBeVisible({ timeout: 5000 });
	});

	test('로그아웃', async ({ page }) => {
		// 먼저 로그인
		await page.goto('/login');
		await page.locator('input[type="email"]').fill(TEST_EMAIL);
		await page.locator('input[type="password"]').fill(TEST_PASSWORD);
		await page.locator('button[type="submit"]').click();
		await page.waitForURL('/');

		// 로그아웃 버튼 찾기 (메뉴 열기 필요할 수 있음)
		const userMenuButton = page.locator('[data-testid="user-menu"], button[aria-label*="user"], button:has([class*="user"])').first();
		if (await userMenuButton.count() > 0) {
			await userMenuButton.click();
		}

		// 로그아웃 버튼 클릭
		const logoutButton = page.locator('button:has-text("로그아웃"), a:has-text("로그아웃")');
		await logoutButton.click();

		// 로그인 페이지로 리다이렉트 또는 로그인 버튼 표시 확인
		await page.waitForTimeout(2000);
		const loginButton = page.locator('a:has-text("로그인"), button:has-text("로그인")');
		await expect(loginButton.first()).toBeVisible({ timeout: 5000 });
	});
});

test.describe('회원가입', () => {
	test('회원가입 페이지 접근', async ({ page }) => {
		await page.goto('/signup');

		// 회원가입 폼 확인
		await expect(page.locator('input[type="email"]')).toBeVisible();
		await expect(page.locator('input[type="password"]').first()).toBeVisible();
	});

	test.skip('새 계정 회원가입', async ({ page }) => {
		// 실제 계정 생성을 방지하기 위해 skip
		// 필요시 테스트 환경에서만 실행
		await page.goto('/signup');

		const randomEmail = `test${Date.now()}@example.com`;
		
		await page.locator('input[type="email"]').fill(randomEmail);
		await page.locator('input[type="password"]').first().fill('testpassword123');
		
		// 비밀번호 확인 필드가 있다면
		const passwordConfirm = page.locator('input[name="password_confirm"], input[name="confirmPassword"]');
		if (await passwordConfirm.count() > 0) {
			await passwordConfirm.fill('testpassword123');
		}

		await page.locator('button[type="submit"]').click();

		// 성공 메시지 또는 리다이렉트 확인
		await page.waitForTimeout(3000);
	});
});

test.describe('비로그인 상태 제한', () => {
	test('비로그인 시 댓글 작성 불가', async ({ page }) => {
		await page.goto('/');
		
		const firstPost = page.locator('a[href^="/post/"]').first();
		if (await firstPost.count() > 0) {
			await firstPost.click();
			await page.waitForURL(/\/post\/\d+/);

			// 댓글 섹션 확인
			const commentsSection = page.locator('#comments').first();
			await commentsSection.scrollIntoViewIfNeeded();

			// 로그인 안내 메시지 확인
			const loginPrompt = page.locator('text=/로그인.*댓글/i, text=/댓글.*로그인/i');
			await expect(loginPrompt).toBeVisible({ timeout: 5000 });

			// 댓글 입력창이 없거나 비활성화되어 있어야 함
			const commentTextarea = page.locator('textarea[name="content"]');
			if (await commentTextarea.count() > 0) {
				await expect(commentTextarea).toBeDisabled();
			}
		}
	});

	test('비로그인 시 좋아요 불가', async ({ page }) => {
		await page.goto('/');
		
		const firstPost = page.locator('a[href^="/post/"]').first();
		if (await firstPost.count() > 0) {
			await firstPost.click();
			await page.waitForURL(/\/post\/\d+/);

			// 좋아요 버튼 찾기
			const likeButton = page.locator('button:has-text("좋아요"), button[aria-label*="like"]').first();
			
			if (await likeButton.count() > 0) {
				await likeButton.click();

				// 로그인 페이지로 리다이렉트 또는 로그인 모달 표시
				await page.waitForTimeout(1000);
				const currentUrl = page.url();
				expect(currentUrl).toMatch(/login|\/$/);
			}
		}
	});
});

test.describe('세션 유지', () => {
	test('로그인 후 새로고침해도 로그인 상태 유지', async ({ page }) => {
		// 로그인
		await page.goto('/login');
		await page.locator('input[type="email"]').fill(TEST_EMAIL);
		await page.locator('input[type="password"]').fill(TEST_PASSWORD);
		await page.locator('button[type="submit"]').click();
		await page.waitForURL('/');

		// 새로고침
		await page.reload();

		// 여전히 로그인 상태인지 확인
		const userMenu = page.locator('[data-testid="user-menu"], button:has-text("로그아웃")');
		await expect(userMenu.first()).toBeVisible({ timeout: 5000 });
	});
});
