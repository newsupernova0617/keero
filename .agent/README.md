# .agent 폴더 가이드

> AI가 SvelteKit을 완벽하게 사용하도록 돕는 문서 모음

---

## 📚 문서 목록

### 1. **AI_ASSISTANT_SETUP.md** ⭐ (가장 중요)

**용도**: AI가 **자동으로 읽고 따라야 할** 프로젝트 설정
**내용**:

- Svelte MCP 사용 워크플로우
- 필수 규칙 및 체크리스트
- 실전 예시

**사용 시점**: 모든 작업 시작 전

---

### 2. **SVELTE_GUIDE.md**

**용도**: Svelte 5 문법 완벽 가이드
**내용**:

- Svelte 5 Runes 상세 설명 (`$state`, `$derived`, `$effect`, `$props`)
- 파일 구조 규칙
- 금지 사항 (Svelte 4 문법)
- 코드 예시

**사용 시점**: Svelte 컴포넌트/페이지 작성 시

---

### 3. **MCP_GUIDE.md**

**용도**: Svelte MCP 서버 사용법
**내용**:

- MCP 명령어 사용법
- 주요 문서 섹션 목록
- 실전 예시
- 성능 팁

**사용 시점**: 최신 Svelte 문서 참조가 필요할 때

---

### 4. **PROMPT_TEMPLATES.md**

**용도**: 효과적인 AI 프롬프트 템플릿
**내용**:

- 상황별 프롬프트 템플릿
- 효과적인 프롬프트 작성 팁
- 실제 사용 예시

**사용 시점**: AI에게 요청할 때

---

### 5. **CODING_RULES.md**

**용도**: 프로젝트 코딩 규칙
**내용**:

- 코드 작성 프로세스
- 자주 하는 실수
- 체크리스트

**사용 시점**: 코드 리뷰 및 검증 시

---

## 🚀 사용 방법

### 시나리오 1: 새 기능 추가

1. **AI_ASSISTANT_SETUP.md** 읽기 → 워크플로우 확인
2. **PROMPT_TEMPLATES.md** → "새 기능 추가" 템플릿 사용
3. **MCP_GUIDE.md** → 필요한 문서 섹션 조회
4. **SVELTE_GUIDE.md** → Svelte 5 문법 확인
5. 코드 작성
6. **CODING_RULES.md** → 체크리스트로 검증

### 시나리오 2: 버그 수정

1. **AI_ASSISTANT_SETUP.md** → 버그 수정 워크플로우
2. **MCP_GUIDE.md** → 관련 문서 조회
3. **SVELTE_GUIDE.md** → 올바른 문법 확인
4. 수정
5. MCP autofixer로 검증

### 시나리오 3: 코드 리뷰

1. **CODING_RULES.md** → 체크리스트 확인
2. **SVELTE_GUIDE.md** → 금지 사항 확인
3. MCP autofixer로 검증

---

## 💡 AI에게 요청하는 방법

### 기본 템플릿

```
이 프로젝트는 Svelte 5 + SvelteKit을 사용합니다.
.agent/AI_ASSISTANT_SETUP.md의 규칙을 따라서 작업해줘.

[구체적인 요청]

참고 문서:
- .agent/SVELTE_GUIDE.md (Svelte 5 문법)
- .agent/MCP_GUIDE.md (MCP 사용법)
```

### 예시 1: 컴포넌트 작성

```
.agent/AI_ASSISTANT_SETUP.md를 따라서 북마크 버튼 컴포넌트를 만들어줘.

1. Svelte MCP로 다음 문서 확인:
   - svelte/$state
   - svelte/$props
   - svelte/event-handlers

2. webapp/src/lib/components/LikeButton.svelte 참고

3. .agent/SVELTE_GUIDE.md 규칙 준수
```

### 예시 2: 페이지 추가

```
.agent/AI_ASSISTANT_SETUP.md를 따라서 /profile/bookmarks 페이지를 만들어줘.

1. Svelte MCP로 다음 문서 확인:
   - kit/routing
   - kit/load
   - kit/form-actions

2. webapp/src/routes/profile/activity/ 참고

3. .agent/SVELTE_GUIDE.md 규칙 준수
```

---

## 📊 문서 우선순위

### 🔴 필수 (모든 작업 시)

- **AI_ASSISTANT_SETUP.md** - 워크플로우
- **SVELTE_GUIDE.md** - Svelte 5 문법

### 🟡 권장 (복잡한 작업 시)

- **MCP_GUIDE.md** - 최신 문서 참조
- **PROMPT_TEMPLATES.md** - 효과적인 요청

### 🟢 선택 (검증 시)

- **CODING_RULES.md** - 코드 리뷰

---

## ✅ 성공 체크리스트

### AI가 생성한 코드는:

- [ ] Svelte 5 Runes 사용 (`$state`, `$derived`, `$effect`, `$props`)
- [ ] Svelte 4 문법 없음 (`export let`, `$:`, `on:`)
- [ ] TypeScript 타입 정의
- [ ] MCP autofixer 검증 통과
- [ ] 기존 코드 스타일 일관성

---

## 🎯 핵심 메시지

**이 프로젝트에서 AI가 SvelteKit을 잘 사용하려면:**

1. ✅ **항상 AI_ASSISTANT_SETUP.md부터 시작**
2. ✅ **Svelte MCP로 최신 문서 확인**
3. ✅ **SVELTE_GUIDE.md 규칙 준수**
4. ✅ **기존 코드 참조**
5. ✅ **검증 후 제공**

---

**마지막 업데이트**: 2026-01-12
