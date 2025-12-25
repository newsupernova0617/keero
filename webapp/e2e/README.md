# 🧪 E2E 테스트 가이드

## 📋 개요

이 디렉토리에는 Playwright를 사용한 E2E (End-to-End) 테스트가 포함되어 있습니다.

## 📁 테스트 파일

| 파일               | 설명             | 테스트 수 |
| ------------------ | ---------------- | --------- |
| `posts.test.ts`    | 게시글 목록/상세 | 5개       |
| `comments.test.ts` | 댓글 CRUD        | 12개      |
| `auth.test.ts`     | 인증 흐름        | 8개       |
| `likes.test.ts`    | 좋아요 기능      | 6개       |

**총 31개 E2E 테스트**

---

## 🚀 실행 방법

### 1. 환경 설정

테스트 계정 정보를 환경 변수로 설정:

```bash
# .env.test 파일 생성
echo "TEST_USER_EMAIL=your-test-email@example.com" > .env.test
echo "TEST_USER_PASSWORD=your-test-password" >> .env.test
```

### 2. 테스트 실행

```bash
# 모든 E2E 테스트 실행
npm run test:e2e

# 특정 테스트 파일만 실행
npx playwright test e2e/comments.test.ts

# UI 모드로 실행 (디버깅)
npx playwright test --ui

# 헤드풀 모드 (브라우저 보이기)
npx playwright test --headed
```

### 3. 테스트 결과 확인

```bash
# HTML 리포트 생성
npx playwright show-report
```

---

## 📝 테스트 상세

### posts.test.ts - 게시글 기능

#### 게시글 목록

- ✅ 메인 페이지 로드 및 게시글 목록 표시
- ✅ 게시글 상세 페이지 접근
- ✅ 게시글 내용 및 이미지 표시
- ✅ 뒤로가기 버튼 작동

#### 페이지네이션

- ✅ 더 보기 버튼 작동

---

### comments.test.ts - 댓글 기능

#### 비로그인 상태

- ✅ 비로그인 시 댓글 작성 폼 숨김

#### 로그인 상태

- ✅ 댓글 작성
- ✅ Enter 키로 댓글 작성
- ✅ Shift+Enter로 줄바꿈
- ✅ 댓글 작성 후 자동 스크롤
- ✅ 빈 댓글 작성 방지

#### 댓글 수정/삭제

- ✅ 본인 댓글 수정
- ✅ 본인 댓글 삭제

#### 답글

- ✅ 답글 작성

---

### auth.test.ts - 인증 흐름

#### 로그인/로그아웃

- ✅ 로그인 페이지 접근
- ✅ 이메일 로그인
- ✅ 잘못된 비밀번호로 로그인 실패
- ✅ 로그아웃

#### 회원가입

- ✅ 회원가입 페이지 접근
- ⏭️ 새 계정 회원가입 (skip)

#### 비로그인 제한

- ✅ 비로그인 시 댓글 작성 불가
- ✅ 비로그인 시 좋아요 불가

#### 세션

- ✅ 로그인 후 새로고침해도 로그인 상태 유지

---

### likes.test.ts - 좋아요 기능

#### 로그인 상태

- ✅ 게시글 좋아요 토글
- ✅ 좋아요 상태 시각적 피드백
- ✅ 댓글 좋아요

#### 비로그인 상태

- ✅ 비로그인 시 좋아요 클릭하면 로그인 페이지로

#### 좋아요 수 표시

- ✅ 게시글 좋아요 수 표시
- ✅ 메인 페이지에서 좋아요 수 표시

---

## ⚙️ 설정

### playwright.config.ts

```typescript
export default defineConfig({
  webServer: {
    command: 'npm run build && npm run preview',
    port: 4173
  },
  testDir: 'e2e'
});
```

---

## 🔧 트러블슈팅

### 테스트 실패 시

1. **서버가 실행 중인지 확인**

   ```bash
   npm run dev
   ```

2. **테스트 계정 확인**
   - `.env.test` 파일에 올바른 계정 정보 입력
   - Supabase에 테스트 계정 존재 확인

3. **브라우저 업데이트**

   ```bash
   npx playwright install
   ```

4. **디버그 모드로 실행**
   ```bash
   npx playwright test --debug
   ```

---

## 📌 주의사항

### 테스트 계정

- 실제 프로덕션 계정 사용 금지
- 테스트 전용 계정 사용 권장
- 테스트 후 생성된 데이터 정리 필요

### 데이터베이스

- 테스트는 실제 데이터베이스에 데이터를 생성합니다
- 테스트 환경 분리 권장
- 정기적으로 테스트 데이터 정리

### CI/CD

- GitHub Actions 등에서 실행 시 환경 변수 설정 필요
- Headless 모드로 실행
- 테스트 결과 아티팩트 저장

---

## 🎯 다음 단계

### 추가 테스트 작성

- [ ] 관리자 페이지 테스트
- [ ] 검색 기능 테스트
- [ ] 사이트 필터링 테스트
- [ ] 북마크 기능 테스트
- [ ] 신고 기능 테스트

### 테스트 개선

- [ ] 테스트 데이터 자동 정리
- [ ] 테스트 환경 분리
- [ ] 시각적 회귀 테스트 (Visual Regression)
- [ ] 성능 테스트

---

## 📚 참고 자료

- [Playwright 공식 문서](https://playwright.dev/)
- [SvelteKit Testing](https://kit.svelte.dev/docs/testing)
- [TEST_PLAN.md](../TEST_PLAN.md) - 전체 테스트 계획
