# 🤖 AI와 함께 개발하기

> Svelte 5 + SvelteKit 프로젝트에서 AI를 최대한 활용하는 방법

---

## 🎯 빠른 시작

### AI에게 이렇게 요청하세요:

```
이 프로젝트는 Svelte 5 + SvelteKit을 사용합니다.
.agent/AI_ASSISTANT_SETUP.md의 규칙을 따라서 작업해줘.

모든 Svelte 코드 작성 전에 Svelte MCP로 최신 문서를 확인하고,
Svelte 5 Runes 문법만 사용해줘.

[여기에 구체적인 요청 작성]
```

---

## 📚 주요 문서

### 1. `.agent/AI_ASSISTANT_SETUP.md` ⭐ **가장 중요**

AI가 자동으로 따라야 할 워크플로우 및 규칙

### 2. `.agent/SVELTE_GUIDE.md`

Svelte 5 Runes 문법 완벽 가이드

### 3. `.agent/MCP_GUIDE.md`

Svelte MCP 서버 사용법

### 4. `.agent/PROMPT_TEMPLATES.md`

효과적인 AI 프롬프트 템플릿

### 5. `.agent/README.md`

모든 문서 개요 및 사용법

---

## 🚀 실전 예시

### 예시 1: 새 컴포넌트 만들기

```
.agent/AI_ASSISTANT_SETUP.md를 따라서 북마크 버튼 컴포넌트를 만들어줘.

1. Svelte MCP로 다음 문서 먼저 확인:
   - svelte/$state
   - svelte/$props
   - svelte/event-handlers

2. webapp/src/lib/components/LikeButton.svelte 스타일 참고

3. 요구사항:
   - $state로 북마크 상태 관리
   - 클릭 시 서버 액션 호출
   - 낙관적 UI 업데이트
   - TypeScript 타입 정의

4. .agent/SVELTE_GUIDE.md 규칙 준수
```

### 예시 2: 새 페이지 추가

```
.agent/AI_ASSISTANT_SETUP.md를 따라서 /profile/bookmarks 페이지를 만들어줘.

1. Svelte MCP로 다음 문서 먼저 확인:
   - kit/routing
   - kit/load
   - kit/form-actions

2. webapp/src/routes/profile/activity/ 구조 참고

3. 요구사항:
   - 사용자 북마크 목록 표시
   - 그리드 레이아웃 (메인 페이지와 동일)
   - 페이지네이션 (24개씩)
   - 북마크 해제 기능

4. .agent/SVELTE_GUIDE.md 규칙 준수
```

### 예시 3: 버그 수정

```
.agent/AI_ASSISTANT_SETUP.md를 따라서 버그를 수정해줘.

1. Svelte MCP로 다음 문서 먼저 확인:
   - svelte/v5-migration-guide

2. 문제: webapp/src/lib/components/Comment.svelte에서
   좋아요 클릭 후 UI가 즉시 업데이트되지 않음

3. 해결 방법:
   - Svelte 5 $state로 낙관적 업데이트 구현
   - 서버 요청 실패 시 롤백

4. .agent/SVELTE_GUIDE.md 규칙 준수
```

---

## ✅ Svelte MCP 활성화 확인

### 테스트 명령어

```bash
# MCP 작동 확인
npx -y @sveltejs/mcp list-sections

# Svelte 5 Runes 문서 조회
npx -y @sveltejs/mcp get-documentation "svelte/\$state,svelte/\$derived"

# 코드 검증
npx -y @sveltejs/mcp svelte-autofixer "
<script lang=\"ts\">
  let count = \$state(0)
</script>
<button onclick={() => count++}>Click</button>
"
```

---

## 🎯 핵심 규칙

### ✅ 반드시 해야 할 것

1. **Svelte MCP로 최신 문서 확인**

   ```bash
   npx -y @sveltejs/mcp get-documentation "svelte/\$state"
   ```

2. **Svelte 5 Runes 사용**

   - `$state` - 반응형 상태
   - `$derived` - 파생 상태
   - `$effect` - 사이드 이펙트
   - `$props` - 컴포넌트 Props

3. **TypeScript 타입 정의**

   ```typescript
   let count = $state<number>(0);
   ```

4. **기존 코드 참조**
   - `webapp/src/routes/` - 페이지 예시
   - `webapp/src/lib/components/` - 컴포넌트 예시

### ❌ 절대 하지 말아야 할 것

1. **Svelte 4 문법 사용 금지**

   ```svelte
   <!-- ❌ 금지 -->
   <script>
     export let data
     $: posts = data.posts
   </script>
   <button on:click={handler}>Click</button>
   ```

2. **any 타입 남용 금지**

   ```typescript
   // ❌ 금지
   const data: any = await fetch();
   ```

3. **MCP 없이 추측으로 코드 작성 금지**
   - 반드시 MCP로 최신 문서 확인 후 작성

---

## 📊 성공 체크리스트

AI가 생성한 코드는 다음을 만족해야 합니다:

- [ ] Svelte 5 Runes 사용 (`$state`, `$derived`, `$effect`, `$props`)
- [ ] Svelte 4 문법 없음 (`export let`, `$:`, `on:`)
- [ ] TypeScript 타입 정의
- [ ] MCP autofixer 검증 통과
- [ ] 기존 코드 스타일 일관성
- [ ] TypeScript 컴파일 에러 없음
- [ ] ESLint 경고 없음

---

## 🔧 유용한 명령어

### Svelte MCP 명령어

```bash
# 사용 가능한 문서 섹션 목록
npx -y @sveltejs/mcp list-sections

# Svelte 5 Runes 문서
npx -y @sveltejs/mcp get-documentation "svelte/what-are-runes,svelte/\$state,svelte/\$derived,svelte/\$effect,svelte/\$props"

# SvelteKit 핵심 문서
npx -y @sveltejs/mcp get-documentation "kit/routing,kit/load,kit/form-actions"

# 코드 검증
npx -y @sveltejs/mcp svelte-autofixer "[코드]"
```

### 프로젝트 명령어

```bash
# 개발 서버 실행
cd webapp && npm run dev

# 타입 체크
cd webapp && npm run check

# 린트
cd webapp && npm run lint

# 테스트
cd webapp && npm run test
```

---

## 📖 추가 리소스

### 프로젝트 문서

- `.agent/README.md` - 모든 가이드 개요
- `.agent/AI_ASSISTANT_SETUP.md` - AI 워크플로우
- `.agent/SVELTE_GUIDE.md` - Svelte 5 문법
- `.agent/MCP_GUIDE.md` - MCP 사용법
- `.agent/PROMPT_TEMPLATES.md` - 프롬프트 템플릿

### 공식 문서

- [Svelte 5 공식 문서](https://svelte.dev/docs/svelte/overview)
- [SvelteKit 공식 문서](https://kit.svelte.dev/docs)
- [Svelte MCP GitHub](https://github.com/sveltejs/mcp)

### 캐시된 참조 문서

- `.agent/svelte5-runes-reference.txt` - Svelte 5 Runes 전체 문서
- `.agent/sveltekit-core-reference.txt` - SvelteKit 핵심 문서

---

## 🎉 시작하기

1. **AI에게 요청할 때 항상 이렇게 시작하세요:**

   ```
   .agent/AI_ASSISTANT_SETUP.md를 따라서 [요청 내용]
   ```

2. **복잡한 작업은 단계별로:**

   ```
   1단계: Svelte MCP로 [문서] 확인
   2단계: [기존 파일] 참고
   3단계: 코드 작성
   4단계: MCP autofixer로 검증
   ```

3. **항상 검증:**
   ```bash
   npx -y @sveltejs/mcp svelte-autofixer "[생성된 코드]"
   ```

---

**행복한 코딩 되세요! 🚀**

**마지막 업데이트**: 2026-01-12
