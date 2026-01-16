# 프로젝트 코딩 규칙

> AI는 코드 작성 시 이 규칙을 **반드시** 따라야 합니다.

---

## 🎯 핵심 원칙

1. **Svelte 5 Runes 문법만 사용** (Svelte 4 문법 절대 금지)
2. **TypeScript 필수 사용**
3. **기존 코드 스타일 유지**
4. **타입 안정성 최우선**

---

## 📖 필수 참조 문서

코드 작성 전 **반드시** 다음 문서를 읽으세요:

- [.agent/SVELTE_GUIDE.md](.agent/SVELTE_GUIDE.md) - Svelte 5 문법 가이드

---

## 🚀 코드 작성 프로세스

### 1단계: 요구사항 확인

- 어떤 기능을 구현해야 하는가?
- 기존 코드 중 참고할 파일이 있는가?

### 2단계: 기존 코드 분석

```bash
# 유사한 기능 찾기
grep -r "비슷한 기능" webapp/src/routes/
```

### 3단계: Svelte 5 문법 확인

- `.agent/SVELTE_GUIDE.md` 참조
- `$state`, `$derived`, `$effect`, `$props` 사용

### 4단계: 타입 정의

```typescript
import type { PageData } from "./$types";
import type { Post } from "$lib/server/schema";
```

### 5단계: 코드 작성

- 서버 로직: `+page.server.ts`
- 클라이언트 UI: `+page.svelte`

### 6단계: 검증

- TypeScript 에러 확인
- ESLint 경고 확인
- Svelte 5 문법 준수 확인

---

## 🔍 자주 하는 실수

### ❌ 실수 1: Svelte 4 문법 사용

```svelte
<!-- ❌ 잘못된 예 -->
<script>
  export let data
  $: posts = data.posts
</script>

<!-- ✅ 올바른 예 -->
<script lang="ts">
  let { data } = $props()
  let posts = $derived(data.posts)
</script>
```

### ❌ 실수 2: any 타입 남용

```typescript
// ❌ 잘못된 예
const posts: any = await db.select();

// ✅ 올바른 예
const posts: Post[] = await db.select().from(posts);
```

### ❌ 실수 3: 클라이언트에서 DB 접근

```svelte
<!-- ❌ 잘못된 예 -->
<script lang="ts">
  import { db } from '$lib/server/db' // 에러!
</script>

<!-- ✅ 올바른 예: +page.server.ts에서 처리 -->
```

---

## 📋 체크리스트

코드 작성 후 확인:

- [ ] Svelte 5 Runes 문법 사용
- [ ] TypeScript 타입 정의
- [ ] 기존 코드 스타일 유지
- [ ] 에러 및 경고 없음
- [ ] `.agent/SVELTE_GUIDE.md` 규칙 준수

---

## 💡 도움이 필요할 때

1. **기존 코드 참조**: `webapp/src/routes/` 폴더의 유사 기능 확인
2. **가이드 확인**: `.agent/SVELTE_GUIDE.md` 읽기
3. **구체적 질문**: "Svelte 5에서 [기능]을 어떻게 구현하나요?"

---

**마지막 업데이트**: 2026-01-12
