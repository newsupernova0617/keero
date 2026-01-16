# SvelteKit 5 개발 가이드

> 이 프로젝트는 **Svelte 5 + SvelteKit 2**를 사용합니다.
> AI는 이 가이드를 **반드시** 참조하여 코드를 작성해야 합니다.

---

## 📌 핵심 원칙

1. **Svelte 5 Runes 문법만 사용** (Svelte 4 문법 금지)
2. **TypeScript 필수**
3. **Server-side 로직은 +page.server.ts에 작성**
4. **클라이언트 컴포넌트는 .svelte 파일에 작성**

---

## 🎯 Svelte 5 Runes 문법

### 1. 반응형 상태: `$state`

```svelte
<script lang="ts">
  // ✅ Svelte 5 (사용)
  let count = $state(0)
  let user = $state<User | null>(null)

  // ❌ Svelte 4 (사용 금지)
  // import { writable } from 'svelte/store'
  // const count = writable(0)
</script>
```

### 2. 파생 상태: `$derived`

```svelte
<script lang="ts">
  let count = $state(0)

  // ✅ Svelte 5 (사용)
  let doubled = $derived(count * 2)
  let isEven = $derived(count % 2 === 0)

  // ❌ Svelte 4 (사용 금지)
  // $: doubled = count * 2
</script>
```

### 3. 사이드 이펙트: `$effect`

```svelte
<script lang="ts">
  import { onMount } from 'svelte'

  let count = $state(0)

  // ✅ Svelte 5 (사용)
  $effect(() => {
    console.log('Count changed:', count)
    // cleanup
    return () => {
      console.log('Cleanup')
    }
  })

  // onMount는 여전히 사용 가능 (초기화 로직)
  onMount(() => {
    console.log('Component mounted')
  })
</script>
```

### 4. Props: `$props`

```svelte
<script lang="ts">
  import type { Post } from '$lib/types'

  // ✅ Svelte 5 (사용)
  let { post, comments = [] }: {
    post: Post
    comments?: Comment[]
  } = $props()

  // ❌ Svelte 4 (사용 금지)
  // export let post: Post
  // export let comments: Comment[] = []
</script>
```

### 5. 이벤트 핸들러

```svelte
<script lang="ts">
  let count = $state(0)

  function increment() {
    count++
  }
</script>

<!-- ✅ Svelte 5 (사용) -->
<button onclick={increment}>+1</button>

<!-- ❌ Svelte 4 (사용 금지) -->
<!-- <button on:click={increment}>+1</button> -->
```

### 6. 양방향 바인딩

```svelte
<script lang="ts">
  let value = $state('')
</script>

<!-- ✅ 여전히 bind 사용 -->
<input bind:value />
```

### 7. Children (Slots)

```svelte
<script lang="ts">
  let { children }: { children: any } = $props()
</script>

<!-- ✅ Svelte 5 (사용) -->
{@render children()}

<!-- ❌ Svelte 4 (사용 금지) -->
<!-- <slot /> -->
```

---

## 🗂️ 파일 구조 규칙

### 페이지 구조

```
routes/
├── +layout.svelte          # 전역 레이아웃
├── +layout.server.ts       # 전역 서버 로직
├── +page.svelte            # 메인 페이지 (클라이언트)
├── +page.server.ts         # 메인 페이지 (서버)
└── post/
    └── [id]/
        ├── +page.svelte        # 게시글 상세 (클라이언트)
        └── +page.server.ts     # 게시글 상세 (서버)
```

### 서버 파일 (+page.server.ts)

```typescript
import type { PageServerLoad, Actions } from "./$types";
import { db } from "$lib/server/db";
import { fail } from "@sveltejs/kit";

// 데이터 로딩
export const load: PageServerLoad = async ({ params, locals }) => {
  const { user } = await locals.safeGetSession();

  const posts = await db.select().from(posts).limit(10);

  return {
    posts,
    user,
  };
};

// 폼 액션
export const actions: Actions = {
  create: async ({ request, locals }) => {
    const { user } = await locals.safeGetSession();

    if (!user) {
      return fail(401, { error: "로그인이 필요합니다." });
    }

    const formData = await request.formData();
    const title = formData.get("title")?.toString();

    // DB 작업
    await db.insert(posts).values({ title });

    return { success: true };
  },
};
```

### 클라이언트 파일 (+page.svelte)

```svelte
<script lang="ts">
  import type { PageData } from './$types'
  import { enhance } from '$app/forms'

  let { data }: { data: PageData } = $props()
  let { posts, user } = $derived(data)

  let isSubmitting = $state(false)
</script>

<h1>게시글 목록</h1>

{#each posts as post}
  <article>
    <h2>{post.title}</h2>
  </article>
{/each}

<form method="POST" action="?/create" use:enhance>
  <input name="title" required />
  <button type="submit">작성</button>
</form>
```

---

## 🔧 컴포넌트 작성 규칙

### 1. 타입 정의

```svelte
<script lang="ts">
  import type { Post } from '$lib/server/schema'

  interface Props {
    post: Post
    onLike?: () => void
  }

  let { post, onLike }: Props = $props()
</script>
```

### 2. 조건부 렌더링

```svelte
{#if user}
  <p>환영합니다, {user.name}!</p>
{:else}
  <a href="/auth/login">로그인</a>
{/if}
```

### 3. 리스트 렌더링

```svelte
{#each posts as post (post.id)}
  <PostCard {post} />
{/each}
```

### 4. 비동기 데이터

```svelte
{#await promise}
  <p>로딩 중...</p>
{:then data}
  <p>데이터: {data}</p>
{:catch error}
  <p>에러: {error.message}</p>
{/await}
```

---

## 🎨 스타일링 규칙

### TailwindCSS 사용

```svelte
<div class="flex items-center gap-4 rounded-lg bg-card p-4">
  <h2 class="text-xl font-bold">제목</h2>
</div>
```

### 컴포넌트 스타일

```svelte
<style>
  /* 컴포넌트 스코프 스타일 */
  .custom-class {
    color: red;
  }
</style>
```

---

## 📡 API 호출

### Server Actions 사용 (권장)

```svelte
<script lang="ts">
  import { enhance } from '$app/forms'
</script>

<form method="POST" action="?/like" use:enhance>
  <input type="hidden" name="post_id" value={post.id} />
  <button type="submit">좋아요</button>
</form>
```

### fetch 사용 (필요시)

```svelte
<script lang="ts">
  async function handleLike() {
    const res = await fetch('/api/like', {
      method: 'POST',
      body: JSON.stringify({ post_id: post.id })
    })

    if (res.ok) {
      // 성공 처리
    }
  }
</script>
```

---

## 🔐 인증 처리

### 서버 사이드

```typescript
export const load: PageServerLoad = async ({ locals }) => {
  const { user } = await locals.safeGetSession();

  if (!user) {
    throw redirect(303, "/auth/login");
  }

  return { user };
};
```

### 클라이언트 사이드

```svelte
<script lang="ts">
  let { data } = $props()
  let { user } = $derived(data)
</script>

{#if user}
  <p>{user.email}</p>
{/if}
```

---

## 🚫 금지 사항

### ❌ Svelte 4 문법 사용 금지

```svelte
<!-- ❌ 사용 금지 -->
<script>
  import { writable } from 'svelte/store'
  const count = writable(0)

  export let data

  $: doubled = count * 2
</script>

<button on:click={increment}>Click</button>
<slot />
```

### ❌ 클라이언트에서 직접 DB 접근 금지

```svelte
<!-- ❌ 사용 금지 -->
<script lang="ts">
  import { db } from '$lib/server/db' // 클라이언트에서 불가능!
</script>
```

### ❌ any 타입 사용 최소화

```typescript
// ❌ 나쁜 예
let data: any = $props();

// ✅ 좋은 예
let { data }: { data: PageData } = $props();
```

---

## 📚 참고 자료

- [Svelte 5 공식 문서](https://svelte.dev/docs/svelte/overview)
- [SvelteKit 공식 문서](https://kit.svelte.dev/docs)
- [Svelte 5 Runes](https://svelte.dev/docs/svelte/what-are-runes)

---

## ✅ 체크리스트

코드 작성 전 확인:

- [ ] Svelte 5 Runes 문법 사용 ($state, $derived, $effect, $props)
- [ ] TypeScript 타입 정의
- [ ] 서버 로직은 +page.server.ts에 작성
- [ ] 클라이언트 로직은 .svelte에 작성
- [ ] TailwindCSS 사용
- [ ] 기존 컴포넌트 스타일 참고

---

**마지막 업데이트**: 2026-01-12
