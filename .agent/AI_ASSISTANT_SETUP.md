# AI 어시스턴트 설정 가이드

> 이 문서는 AI가 **자동으로 읽고 따라야 할** 프로젝트 규칙입니다.

---

## 🎯 필수 규칙

AI는 코드 작성 시 **반드시** 다음 순서를 따라야 합니다:

### 1단계: 문서 확인 ✅

모든 Svelte/SvelteKit 관련 작업 전에 **반드시** 다음 중 하나를 수행:

#### Option A: Svelte MCP 사용 (권장)

```bash
# 필요한 문서 섹션 조회
npx -y @sveltejs/mcp get-documentation "svelte/\$state,svelte/\$derived,svelte/\$props"
```

#### Option B: 프로젝트 가이드 참조

- `.agent/SVELTE_GUIDE.md` - Svelte 5 문법 가이드
- `.agent/MCP_GUIDE.md` - MCP 사용법
- `.agent/PROMPT_TEMPLATES.md` - 프롬프트 템플릿

### 2단계: 기존 코드 분석 ✅

유사한 기능이 있는지 확인:

```
webapp/src/routes/ - 페이지 예시
webapp/src/lib/components/ - 컴포넌트 예시
```

### 3단계: 코드 작성 ✅

**필수 사항:**

- ✅ Svelte 5 Runes 사용 (`$state`, `$derived`, `$effect`, `$props`)
- ✅ TypeScript 타입 정의
- ✅ 기존 코드 스타일 유지
- ❌ Svelte 4 문법 절대 금지
- ❌ `any` 타입 최소화

### 4단계: 검증 ✅

```bash
# Svelte MCP로 코드 검증
npx -y @sveltejs/mcp svelte-autofixer "[코드]"
```

---

## 📚 자주 사용하는 MCP 명령어

### Svelte 5 Runes 문법 확인

```bash
npx -y @sveltejs/mcp get-documentation "svelte/what-are-runes,svelte/\$state,svelte/\$derived,svelte/\$effect,svelte/\$props"
```

### SvelteKit 라우팅 & 데이터

```bash
npx -y @sveltejs/mcp get-documentation "kit/routing,kit/load,kit/form-actions"
```

### 이벤트 핸들링

```bash
npx -y @sveltejs/mcp get-documentation "svelte/event-handlers,svelte/component-events"
```

### 마이그레이션 가이드

```bash
npx -y @sveltejs/mcp get-documentation "svelte/v5-migration-guide"
```

---

## 🚀 프로젝트별 추천 워크플로우

### 새 컴포넌트 작성

1. **MCP로 문서 확인**

   ```bash
   npx -y @sveltejs/mcp get-documentation "svelte/\$state,svelte/\$props,svelte/event-handlers"
   ```

2. **기존 컴포넌트 참조**

   ```
   webapp/src/lib/components/Comment.svelte
   webapp/src/lib/components/LikeButton.svelte
   ```

3. **코드 작성** (Svelte 5 Runes 사용)

4. **검증**
   ```bash
   npx -y @sveltejs/mcp svelte-autofixer "[생성한 코드]"
   ```

### 새 페이지 추가

1. **MCP로 문서 확인**

   ```bash
   npx -y @sveltejs/mcp get-documentation "kit/routing,kit/load,kit/form-actions"
   ```

2. **기존 페이지 참조**

   ```
   webapp/src/routes/post/[id]/+page.svelte
   webapp/src/routes/post/[id]/+page.server.ts
   ```

3. **파일 생성**

   - `routes/[경로]/+page.svelte` (클라이언트)
   - `routes/[경로]/+page.server.ts` (서버)

4. **검증**

### 버그 수정

1. **MCP로 관련 문서 확인**

   ```bash
   npx -y @sveltejs/mcp get-documentation "svelte/v5-migration-guide"
   ```

2. **코드 분석**

3. **수정 및 검증**
   ```bash
   npx -y @sveltejs/mcp svelte-autofixer "[수정한 코드]"
   ```

---

## 🎯 실전 예시

### 예시 1: 댓글 컴포넌트 작성

**AI 프롬프트:**

```
Svelte MCP를 사용해서 다음 문서를 먼저 확인해줘:
- svelte/$state
- svelte/$derived
- svelte/$props
- svelte/event-handlers

그 다음 webapp/src/lib/components/Comment.svelte를 참고해서
답글 기능이 있는 댓글 컴포넌트를 만들어줘.

요구사항:
1. $state로 답글 입력 상태 관리
2. $derived로 답글 개수 계산
3. TypeScript 타입 정의
4. 기존 스타일 유지
```

**AI 작업 순서:**

1. ✅ MCP로 문서 조회
2. ✅ Comment.svelte 분석
3. ✅ Svelte 5 문법으로 코드 작성
4. ✅ MCP autofixer로 검증
5. ✅ 최종 코드 제공

### 예시 2: 페이지 추가

**AI 프롬프트:**

```
Svelte MCP를 사용해서 다음 문서를 먼저 확인해줘:
- kit/routing
- kit/load
- kit/form-actions

그 다음 /profile/bookmarks 페이지를 만들어줘.
webapp/src/routes/profile/activity/+page.svelte 구조를 참고해줘.
```

**AI 작업 순서:**

1. ✅ MCP로 SvelteKit 문서 조회
2. ✅ 기존 profile 페이지 분석
3. ✅ +page.svelte, +page.server.ts 생성
4. ✅ 검증 및 제공

---

## 🚫 금지 사항

### ❌ 절대 하지 말 것

1. **Svelte 4 문법 사용**

   ```svelte
   <!-- ❌ 금지 -->
   <script>
     export let data
     $: posts = data.posts
   </script>
   <button on:click={handler}>Click</button>
   ```

2. **MCP 없이 추측으로 코드 작성**

   - 반드시 MCP로 최신 문서 확인 후 작성

3. **any 타입 남용**

   ```typescript
   // ❌ 금지
   const data: any = await fetch();

   // ✅ 올바름
   const data: Post[] = await fetch();
   ```

4. **클라이언트에서 DB 접근**
   ```svelte
   <!-- ❌ 금지 -->
   <script lang="ts">
     import { db } from '$lib/server/db'
   </script>
   ```

---

## ✅ 체크리스트

### 코드 작성 전

- [ ] Svelte MCP로 관련 문서 확인
- [ ] 기존 코드 참조
- [ ] .agent/SVELTE_GUIDE.md 읽기

### 코드 작성 중

- [ ] Svelte 5 Runes 사용
- [ ] TypeScript 타입 정의
- [ ] 기존 스타일 유지

### 코드 작성 후

- [ ] MCP autofixer로 검증
- [ ] TypeScript 에러 없음
- [ ] ESLint 경고 없음

---

## 📖 참고 문서

1. **프로젝트 가이드**

   - `.agent/SVELTE_GUIDE.md` - Svelte 5 문법
   - `.agent/MCP_GUIDE.md` - MCP 사용법
   - `.agent/PROMPT_TEMPLATES.md` - 프롬프트 템플릿
   - `.agent/CODING_RULES.md` - 코딩 규칙

2. **공식 문서** (MCP로 접근)

   - Svelte 5: `npx -y @sveltejs/mcp get-documentation "svelte/..."`
   - SvelteKit: `npx -y @sveltejs/mcp get-documentation "kit/..."`

3. **기존 코드**
   - `webapp/src/routes/` - 페이지 예시
   - `webapp/src/lib/components/` - 컴포넌트 예시
   - `webapp/src/lib/server/` - 서버 로직

---

## 🎯 성공 기준

AI가 생성한 코드는 다음 조건을 만족해야 합니다:

1. ✅ **Svelte 5 Runes 사용**

   - `$state`, `$derived`, `$effect`, `$props`

2. ✅ **TypeScript 타입 안정성**

   - 모든 변수와 함수에 타입 정의
   - `any` 타입 최소화

3. ✅ **MCP 검증 통과**

   - `svelte-autofixer`로 검증 완료

4. ✅ **기존 코드 스타일 일관성**

   - TailwindCSS 사용
   - 컴포넌트 구조 유지

5. ✅ **에러 없음**
   - TypeScript 컴파일 에러 없음
   - ESLint 경고 없음

---

**마지막 업데이트**: 2026-01-12

---

## 🚀 빠른 시작

AI에게 다음과 같이 요청하세요:

```
이 프로젝트는 Svelte 5 + SvelteKit을 사용합니다.
.agent/AI_ASSISTANT_SETUP.md의 규칙을 따라서 작업해줘.

모든 Svelte 코드 작성 전에 Svelte MCP로 최신 문서를 확인하고,
Svelte 5 Runes 문법만 사용해줘.

[구체적인 요청 내용]
```
