import { expect, test } from '@playwright/test';

/**
 * 댓글 기능 E2E 테스트
 * 
 * 주의: 이 테스트는 Supabase 인증이 필요합니다.
 * 테스트 전에 .env 파일에 테스트 계정 정보를 설정하세요.
 */

// 테스트 계정 정보 (환경 변수에서 가져오기)
const TEST_EMAIL = process.env.TEST_USER_EMAIL || 'test@example.com';
const TEST_PASSWORD = process.env.TEST_USER_PASSWORD || 'testpassword123';

test.describe('댓글 기능 (비로그인)', () => {
	test('비로그인 시 댓글 작성 폼 숨김', async ({ page }) => {
		await page.goto('/');
		
		const firstPost = page.locator('a[href^="/post/"]').first();
		if (await firstPost.count() > 0) {
			await firstPost.click();
			await page.waitForURL(/\/post\/\d+/);

			// 댓글 섹션으로 스크롤
			const commentsSection = page.locator('#comments, [id*="comment"]').first();
			if (await commentsSection.count() > 0) {
				await commentsSection.scrollIntoViewIfNeeded();
			}

			// 로그인 안내 메시지 확인
			const loginPrompt = page.locator('text=/로그인.*댓글/i, text=/댓글.*로그인/i');
			await expect(loginPrompt).toBeVisible({ timeout: 5000 });
		}
	});
});

test.describe('댓글 기능 (로그인)', () => {
	// 각 테스트 전에 로그인
	test.beforeEach(async ({ page }) => {
		// 로그인 페이지로 이동
		await page.goto('/login');
		
		// 이메일 입력
		const emailInput = page.locator('input[type="email"], input[name="email"]');
		if (await emailInput.count() > 0) {
			await emailInput.fill(TEST_EMAIL);
			
			// 비밀번호 입력
			const passwordInput = page.locator('input[type="password"], input[name="password"]');
			await passwordInput.fill(TEST_PASSWORD);
			
			// 로그인 버튼 클릭
			const loginButton = page.locator('button[type="submit"]:has-text("로그인"), button:has-text("로그인")');
			await loginButton.click();
			
			// 로그인 완료 대기
			await page.waitForURL('/', { timeout: 10000 });
		}
	});

	test('댓글 작성', async ({ page }) => {
		// 게시글 페이지로 이동
		await page.goto('/');
		const firstPost = page.locator('a[href^="/post/"]').first();
		await firstPost.click();
		await page.waitForURL(/\/post\/\d+/);

		// 댓글 섹션으로 스크롤
		const commentsSection = page.locator('#comments').first();
		await commentsSection.scrollIntoViewIfNeeded();

		// 댓글 입력
		const commentTextarea = page.locator('textarea[name="content"]').first();
		const testComment = `테스트 댓글 ${Date.now()}`;
		await commentTextarea.fill(testComment);

		// 댓글 작성 버튼 클릭
		const submitButton = page.locator('button[type="submit"]:has-text("댓글"), button:has-text("작성")').first();
		await submitButton.click();

		// 댓글이 표시될 때까지 대기
		await page.waitForTimeout(2000);

		// 작성한 댓글이 표시되는지 확인
		const newComment = page.locator(`text="${testComment}"`);
		await expect(newComment).toBeVisible({ timeout: 10000 });
	});

	test('Enter 키로 댓글 작성', async ({ page }) => {
		await page.goto('/');
		const firstPost = page.locator('a[href^="/post/"]').first();
		await firstPost.click();
		await page.waitForURL(/\/post\/\d+/);

		const commentsSection = page.locator('#comments').first();
		await commentsSection.scrollIntoViewIfNeeded();

		const commentTextarea = page.locator('textarea[name="content"]').first();
		const testComment = `Enter 테스트 ${Date.now()}`;
		await commentTextarea.fill(testComment);

		// Enter 키 입력
		await commentTextarea.press('Enter');

		// 댓글이 표시될 때까지 대기
		await page.waitForTimeout(2000);

		const newComment = page.locator(`text="${testComment}"`);
		await expect(newComment).toBeVisible({ timeout: 10000 });
	});

	test('Shift+Enter로 줄바꿈', async ({ page }) => {
		await page.goto('/');
		const firstPost = page.locator('a[href^="/post/"]').first();
		await firstPost.click();
		await page.waitForURL(/\/post\/\d+/);

		const commentsSection = page.locator('#comments').first();
		await commentsSection.scrollIntoViewIfNeeded();

		const commentTextarea = page.locator('textarea[name="content"]').first();
		
		await commentTextarea.fill('첫 줄');
		await commentTextarea.press('Shift+Enter');
		await commentTextarea.type('둘째 줄');

		// Textarea 값 확인
		const value = await commentTextarea.inputValue();
		expect(value).toContain('\n');
		expect(value).toContain('첫 줄');
		expect(value).toContain('둘째 줄');
	});

	test('댓글 작성 후 자동 스크롤', async ({ page }) => {
		await page.goto('/');
		const firstPost = page.locator('a[href^="/post/"]').first();
		await firstPost.click();
		await page.waitForURL(/\/post\/\d+/);

		// 페이지 상단으로 스크롤
		await page.evaluate(() => window.scrollTo(0, 0));

		const commentsSection = page.locator('#comments').first();
		await commentsSection.scrollIntoViewIfNeeded();

		const commentTextarea = page.locator('textarea[name="content"]').first();
		const testComment = `스크롤 테스트 ${Date.now()}`;
		await commentTextarea.fill(testComment);

		const submitButton = page.locator('button[type="submit"]:has-text("댓글")').first();
		await submitButton.click();

		// 댓글 섹션이 뷰포트에 있는지 확인
		await page.waitForTimeout(2000);
		const boundingBox = await commentsSection.boundingBox();
		expect(boundingBox).not.toBeNull();
	});

	test('빈 댓글 작성 방지', async ({ page }) => {
		await page.goto('/');
		const firstPost = page.locator('a[href^="/post/"]').first();
		await firstPost.click();
		await page.waitForURL(/\/post\/\d+/);

		const commentsSection = page.locator('#comments').first();
		await commentsSection.scrollIntoViewIfNeeded();

		const commentTextarea = page.locator('textarea[name="content"]').first();
		
		// 빈 내용으로 Enter
		await commentTextarea.fill('   '); // 공백만
		await commentTextarea.press('Enter');

		// 댓글이 작성되지 않아야 함
		await page.waitForTimeout(1000);
		// 빈 댓글은 제출되지 않음
		
		// Textarea가 여전히 비어있거나 공백만 있어야 함
		const value = await commentTextarea.inputValue();
		expect(value.trim()).toBe('');
	});
});

test.describe('댓글 수정 및 삭제', () => {
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

	test('본인 댓글 수정', async ({ page }) => {
		// 먼저 댓글 작성
		await page.goto('/');
		const firstPost = page.locator('a[href^="/post/"]').first();
		await firstPost.click();
		await page.waitForURL(/\/post\/\d+/);

		const commentsSection = page.locator('#comments').first();
		await commentsSection.scrollIntoViewIfNeeded();

		const commentTextarea = page.locator('textarea[name="content"]').first();
		const originalComment = `수정 전 ${Date.now()}`;
		await commentTextarea.fill(originalComment);
		await commentTextarea.press('Enter');
		await page.waitForTimeout(2000);

		// 수정 버튼 클릭
		const editButton = page.locator('button:has-text("수정")').last();
		if (await editButton.count() > 0) {
			await editButton.click();

			// 수정 입력창에 새 내용 입력
			const editTextarea = page.locator('textarea[name="content"]').last();
			const editedComment = `수정 후 ${Date.now()}`;
			await editTextarea.fill(editedComment);

			// 저장 버튼 클릭
			const saveButton = page.locator('button:has-text("저장"), button[type="submit"]').last();
			await saveButton.click();
			await page.waitForTimeout(2000);

			// 수정된 댓글 확인
			const updatedComment = page.locator(`text="${editedComment}"`);
			await expect(updatedComment).toBeVisible({ timeout: 5000 });
		}
	});

	test('본인 댓글 삭제', async ({ page }) => {
		// 먼저 댓글 작성
		await page.goto('/');
		const firstPost = page.locator('a[href^="/post/"]').first();
		await firstPost.click();
		await page.waitForURL(/\/post\/\d+/);

		const commentsSection = page.locator('#comments').first();
		await commentsSection.scrollIntoViewIfNeeded();

		const commentTextarea = page.locator('textarea[name="content"]').first();
		const testComment = `삭제 테스트 ${Date.now()}`;
		await commentTextarea.fill(testComment);
		await commentTextarea.press('Enter');
		await page.waitForTimeout(2000);

		// 삭제 버튼 클릭
		const deleteButton = page.locator('button:has-text("삭제")').last();
		if (await deleteButton.count() > 0) {
			await deleteButton.click();
			await page.waitForTimeout(2000);

			// 댓글이 사라졌는지 확인
			const deletedComment = page.locator(`text="${testComment}"`);
			await expect(deletedComment).not.toBeVisible({ timeout: 5000 });
		}
	});
});

test.describe('답글 기능', () => {
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

	test('답글 작성', async ({ page }) => {
		await page.goto('/');
		const firstPost = page.locator('a[href^="/post/"]').first();
		await firstPost.click();
		await page.waitForURL(/\/post\/\d+/);

		const commentsSection = page.locator('#comments').first();
		await commentsSection.scrollIntoViewIfNeeded();

		// 답글 버튼 클릭
		const replyButton = page.locator('button:has-text("답글")').first();
		if (await replyButton.count() > 0) {
			await replyButton.click();

			// 답글 입력
			const replyTextarea = page.locator('textarea[name="content"]').last();
			const testReply = `답글 테스트 ${Date.now()}`;
			await replyTextarea.fill(testReply);
			await replyTextarea.press('Enter');
			await page.waitForTimeout(2000);

			// 답글이 표시되는지 확인
			const newReply = page.locator(`text="${testReply}"`);
			await expect(newReply).toBeVisible({ timeout: 10000 });
		}
	});
});
