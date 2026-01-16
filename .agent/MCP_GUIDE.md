# Svelte MCP 서버 사용 가이드

> AI가 Svelte 5 최신 문서를 참조하여 정확한 코드를 생성하도록 돕는 도구

---

## 🎯 Svelte MCP란?

**Model Context Protocol (MCP) for Svelte**는 AI가 최신 Svelte 5 및 SvelteKit 문서에 접근하여 정확한 코드를 생성할 수 있도록 돕는 도구입니다.

### 주요 기능

1. **list-sections**: 사용 가능한 모든 문서 섹션 목록 조회
2. **get-documentation**: 특정 섹션의 전체 문서 가져오기
3. **svelte-autofixer**: Svelte 코드 분석 및 개선 제안
4. **playground-link**: Svelte Playground 링크 생성

---

## 🚀 빠른 시작

### 1. 사용 가능한 문서 섹션 확인

```bash
npx -y @sveltejs/mcp list-sections
```

### 2. 특정 문서 가져오기

```bash
# Svelte 5 Runes 문서
npx -y @sveltejs/mcp get-documentation "svelte/what-are-runes"

# 여러 섹션 동시 조회
npx -y @sveltejs/mcp get-documentation "svelte/what-are-runes,svelte/$state,svelte/$derived"
```

### 3. 코드 검증

```bash
npx -y @sveltejs/mcp svelte-autofixer "
<script lang=\"ts\">
  let count = \$state(0)
</script>
<button onclick={() => count++}>Click</button>
"
```

---

## 📚 주요 문서 섹션

### Svelte 5 핵심 개념

- `svelte/what-are-runes` - Runes 개요
- `svelte/$state` - 반응형 상태
- `svelte/$derived` - 파생 상태
- `svelte/$effect` - 사이드 이펙트
- `svelte/$props` - 컴포넌트 Props
- `svelte/snippets` - 재사용 가능한 마크업

### SvelteKit

- `kit/introduction` - SvelteKit 소개
- `kit/routing` - 라우팅 시스템
- `kit/load` - 데이터 로딩
- `kit/form-actions` - 폼 액션
- `kit/page-options` - 페이지 옵션
- `kit/server-only-modules` - 서버 전용 모듈

### 마이그레이션

- `svelte/v5-migration-guide` - Svelte 5 마이그레이션
- `svelte/legacy-overview` - 레거시 기능 개요

---

## 💡 AI 프롬프트에서 활용하기

### 방법 1: 문서 참조 요청

```
Svelte MCP를 사용해서 최신 Svelte 5 $state 문법을 확인하고,
댓글 컴포넌트를 만들어줘.

필요한 문서:
- svelte/$state
- svelte/$derived
- svelte/$effect
```

### 방법 2: 코드 검증 요청

```
다음 코드를 Svelte MCP autofixer로 검증하고 개선해줘:

[코드 붙여넣기]
```

### 방법 3: 마이그레이션 지원

```
Svelte MCP의 v5-migration-guide를 참조해서
이 Svelte 4 코드를 Svelte 5로 변환해줘:

[Svelte 4 코드]
```

---

## 🔧 자주 사용하는 명령어

### 1. Runes 문법 확인

```bash
npx -y @sveltejs/mcp get-documentation "svelte/what-are-runes,svelte/\$state,svelte/\$derived,svelte/\$effect,svelte/\$props"
```

### 2. SvelteKit 라우팅 및 데이터 로딩

```bash
npx -y @sveltejs/mcp get-documentation "kit/routing,kit/load,kit/form-actions"
```

### 3. 이벤트 핸들링

```bash
npx -y @sveltejs/mcp get-documentation "svelte/event-handlers,svelte/component-events"
```

### 4. 타입스크립트 설정

```bash
npx -y @sveltejs/mcp get-documentation "svelte/typescript,kit/types"
```

---

## 📋 프로젝트별 추천 문서

### 이 프로젝트 (AAGAG Clone)에서 자주 사용할 섹션

#### 기본 구조

- `svelte/what-are-runes` - Runes 기본 개념
- `svelte/$state` - 상태 관리 (댓글, 좋아요 등)
- `svelte/$derived` - 파생 상태 (댓글 개수, 필터링 등)
- `svelte/$props` - 컴포넌트 Props

#### 라우팅 & 데이터

- `kit/routing` - 파일 기반 라우팅
- `kit/load` - +page.server.ts 데이터 로딩
- `kit/form-actions` - 댓글 작성, 좋아요 등

#### 고급 기능

- `svelte/$effect` - 자동 스크롤, 실시간 업데이트
- `svelte/snippets` - 재사용 가능한 UI 조각
- `kit/hooks` - 인증 미들웨어

#### 마이그레이션 & 레거시

- `svelte/v5-migration-guide` - Svelte 4→5 변환
- `svelte/legacy-on` - 이벤트 핸들러 변경사항
- `svelte/legacy-slots` - Slot → Children 변환

---

## 🎯 실전 예시

### 예시 1: 새 컴포넌트 작성 시

**프롬프트:**

```
Svelte MCP를 사용해서 다음 문서를 참조하고 북마크 버튼 컴포넌트를 만들어줘:
- svelte/$state (버튼 상태 관리)
- svelte/$props (post_id prop)
- svelte/event-handlers (클릭 이벤트)

요구사항:
1. 북마크 상태를 $state로 관리
2. 클릭 시 서버 액션 호출
3. 낙관적 UI 업데이트
```

### 예시 2: 버그 수정 시

**프롬프트:**

```
Svelte MCP autofixer로 다음 코드를 검증하고,
svelte/v5-migration-guide를 참조해서 Svelte 5 문법으로 수정해줘:

<script>
  export let data
  $: posts = data.posts
</script>
```

### 예시 3: 새 페이지 추가 시

**프롬프트:**

```
Svelte MCP에서 다음 문서를 참조해서 /profile/bookmarks 페이지를 만들어줘:
- kit/routing (라우팅 구조)
- kit/load (데이터 로딩)
- kit/form-actions (북마크 해제 액션)
- svelte/$state (클라이언트 상태)

기존 /profile/activity/+page.svelte 구조를 참고해줘.
```

---

## 🔍 문서 섹션 전체 목록

<details>
<summary>클릭하여 전체 섹션 보기</summary>

### Svelte 5 Core

- svelte/what-are-runes
- svelte/$state
- svelte/$derived
- svelte/$effect
- svelte/$props
- svelte/$bindable
- svelte/$inspect
- svelte/snippets
- svelte/event-handlers
- svelte/component-events
- svelte/run

### SvelteKit

- kit/introduction
- kit/creating-a-project
- kit/project-structure
- kit/routing
- kit/load
- kit/form-actions
- kit/page-options
- kit/link-options
- kit/hooks
- kit/modules
- kit/server-only-modules
- kit/state-management
- kit/errors
- kit/configuration
- kit/cli
- kit/types
- kit/adapters
- kit/seo
- kit/accessibility

### Migration

- svelte/v5-migration-guide
- svelte/v4-migration-guide
- svelte/legacy-overview
- svelte/legacy-let
- svelte/legacy-reactive-assignments
- svelte/legacy-export-let
- svelte/legacy-on
- svelte/legacy-slots

</details>

---

## ⚡ 성능 팁

### 1. 여러 섹션 동시 조회

```bash
# ❌ 느림 (3번 호출)
npx -y @sveltejs/mcp get-documentation "svelte/\$state"
npx -y @sveltejs/mcp get-documentation "svelte/\$derived"
npx -y @sveltejs/mcp get-documentation "svelte/\$effect"

# ✅ 빠름 (1번 호출)
npx -y @sveltejs/mcp get-documentation "svelte/\$state,svelte/\$derived,svelte/\$effect"
```

### 2. 캐싱 활용

AI는 한 번 조회한 문서를 세션 동안 기억합니다. 같은 문서를 반복 요청하지 마세요.

---

## 🚫 주의사항

1. **문서 섹션 이름 정확히 입력**

   - ❌ `svelte/state` (잘못됨)
   - ✅ `svelte/$state` (올바름)

2. **여러 섹션 조회 시 쉼표로 구분**

   - ❌ `"svelte/$state svelte/$derived"`
   - ✅ `"svelte/$state,svelte/$derived"`

3. **코드 검증 시 이스케이프 처리**
   - `$` 기호는 `\$`로 이스케이프

---

## 📖 추가 리소스

- [Svelte 5 공식 문서](https://svelte.dev/docs/svelte/overview)
- [SvelteKit 공식 문서](https://kit.svelte.dev/docs)
- [Svelte MCP GitHub](https://github.com/sveltejs/mcp)

---

## ✅ 체크리스트

코드 작성 전:

- [ ] 필요한 문서 섹션 확인 (`list-sections`)
- [ ] 관련 문서 조회 (`get-documentation`)
- [ ] 기존 프로젝트 코드 참고
- [ ] Svelte 5 문법 준수

코드 작성 후:

- [ ] MCP autofixer로 검증
- [ ] TypeScript 에러 확인
- [ ] .agent/SVELTE_GUIDE.md 규칙 준수

---

**마지막 업데이트**: 2026-01-12
