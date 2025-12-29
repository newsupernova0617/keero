# 🧪 AAGAG Clone - 전체 프로젝트 테스트 계획

## 📋 개요

| 항목              | 웹앱 (SvelteKit)    | 크롤러 (Python) |
| ----------------- | ------------------- | --------------- |
| 테스트 프레임워크 | Vitest + Playwright | pytest          |
| Unit 테스트       | ✅ 가능             | ✅ 가능         |
| E2E 테스트        | ✅ 가능             | ✅ 가능         |
| 커버리지 도구     | vitest coverage     | pytest-cov      |

---

## 📁 프로젝트 구조

```
aagag_clone/
├── webapp/                 # SvelteKit 웹앱
│   ├── src/
│   │   ├── routes/         # 페이지 (테스트 대상)
│   │   ├── lib/            # 컴포넌트, 유틸 (테스트 대상)
│   │   └── demo.spec.ts    # 기존 Unit 테스트
│   ├── e2e/
│   │   └── demo.test.ts    # 기존 E2E 테스트
│   └── tests/              # 추가 테스트 (생성 예정)
│
└── crawler/                # Python 크롤러
    ├── tests/              # Unit 테스트
    │   ├── test_scraper.py
    │   ├── test_storage.py
    │   ├── test_html_processing.py
    │   ├── test_logging_db.py
    │   └── test_main.py
    └── test_*.py           # E2E/통합 테스트
```

---

## 🎯 Phase 1: 웹앱 Unit 테스트

### 1.1 컴포넌트 테스트

| 컴포넌트          | 테스트 항목              | 우선순위 |
| ----------------- | ------------------------ | -------- |
| `Comment.svelte`  | 렌더링, 수정, 삭제, 답글 | 🔴 높음  |
| `Button.svelte`   | 클릭, 비활성화, 로딩     | 🟡 중간  |
| `Textarea.svelte` | 입력, 바인딩, Enter 키   | 🟡 중간  |
| `UserMenu.svelte` | 로그인/로그아웃          | 🔴 높음  |
| `Badge.svelte`    | 렌더링, 스타일           | 🟢 낮음  |
| `Card.svelte`     | 렌더링                   | 🟢 낮음  |

### 1.2 유틸리티 테스트

| 유틸리티          | 테스트 항목  | 우선순위 |
| ----------------- | ------------ | -------- |
| `ads.ts`          | 광고 설정 값 | 🟡 중간  |
| `sanitize`        | HTML 정제    | 🔴 높음  |
| `date formatting` | 날짜 포맷    | 🟢 낮음  |

### 1.3 실행 방법

```bash
cd webapp
npm run test:unit
```

---

## 🎯 Phase 2: 웹앱 E2E 테스트

### 2.1 인증 흐름

| 테스트 케이스 | 설명                  | 우선순위 |
| ------------- | --------------------- | -------- |
| 회원가입      | 이메일 회원가입       | 🔴 높음  |
| 로그인        | 이메일 로그인         | 🔴 높음  |
| 로그아웃      | 로그아웃 후 세션 확인 | 🔴 높음  |
| 비로그인 접근 | 비로그인 시 UI 확인   | 🟡 중간  |

### 2.2 게시글 기능

| 테스트 케이스    | 설명                    | 우선순위 |
| ---------------- | ----------------------- | -------- |
| 게시글 목록 조회 | 메인 페이지 게시글 표시 | 🔴 높음  |
| 게시글 상세 보기 | 제목, 내용, 이미지 표시 | 🔴 높음  |
| 페이지네이션     | 더 보기, 페이지 이동    | 🟡 중간  |
| 사이트 필터링    | 사이트별 필터 작동      | 🟡 중간  |
| 좋아요           | 좋아요 토글, 카운트     | 🔴 높음  |

### 2.3 댓글 기능

| 테스트 케이스      | 설명                 | 우선순위 |
| ------------------ | -------------------- | -------- |
| 댓글 작성          | 로그인 후 댓글 작성  | 🔴 높음  |
| 댓글 수정          | 본인 댓글 수정       | 🔴 높음  |
| 댓글 삭제          | 본인 댓글 삭제       | 🔴 높음  |
| 답글 작성          | 대댓글 작성          | 🔴 높음  |
| Enter 키 작성      | Enter로 댓글 제출    | 🟡 중간  |
| Shift+Enter 줄바꿈 | Shift+Enter로 줄바꿈 | 🟡 중간  |
| 실시간 업데이트    | 작성 후 즉시 표시    | 🔴 높음  |
| 스크롤 이동        | 댓글 작성 후 스크롤  | 🟡 중간  |

### 2.4 관리자 기능

| 테스트 케이스     | 설명           | 우선순위 |
| ----------------- | -------------- | -------- |
| 관리자 대시보드   | 접근 권한 확인 | 🔴 높음  |
| 데이터베이스 관리 | 통계 조회      | 🟡 중간  |
| 게시글 삭제       | 관리자 삭제    | 🟡 중간  |

### 2.5 실행 방법

```bash
cd webapp
npm run test:e2e
```

---

## 🎯 Phase 3: 크롤러 Unit 테스트

### 3.1 스크래퍼 테스트 (`tests/test_scraper.py`)

| 테스트 케이스 | 설명                    | 우선순위 |
| ------------- | ----------------------- | -------- |
| HTML 파싱     | BeautifulSoup 파싱      | 🔴 높음  |
| 이미지 추출   | src, data-original 추출 | 🔴 높음  |
| URL 정규화    | 상대 URL → 절대 URL     | 🔴 높음  |
| 에러 처리     | 네트워크 에러 처리      | 🔴 높음  |
| 사이트별 파서 | FMKorea, 뽐뿌 등        | 🔴 높음  |

### 3.2 저장소 테스트 (`tests/test_storage.py`)

| 테스트 케이스 | 설명                   | 우선순위 |
| ------------- | ---------------------- | -------- |
| 게시글 저장   | DB 저장 및 조회        | 🔴 높음  |
| 이미지 저장   | 이미지 메타데이터 저장 | 🔴 높음  |
| 중복 검사     | URL 중복 체크          | 🔴 높음  |
| R2 업로드     | 이미지 업로드          | 🔴 높음  |

### 3.3 HTML 처리 테스트 (`tests/test_html_processing.py`)

| 테스트 케이스        | 설명                | 우선순위 |
| -------------------- | ------------------- | -------- |
| HTML 정제            | 불필요 태그 제거    | 🔴 높음  |
| URL 치환             | 원본 URL → R2 URL   | 🔴 높음  |
| transparent.gif 필터 | 플레이스홀더 필터링 | 🔴 높음  |

### 3.4 실행 방법

```bash
cd crawler
source venv/bin/activate
pytest tests/ -v
```

---

## 🎯 Phase 4: 크롤러 E2E 테스트

### 4.1 사이트별 크롤링 테스트

| 사이트     | 테스트 파일                   | 상태    |
| ---------- | ----------------------------- | ------- |
| FMKorea    | `test_fmkorea_playwright.py`  | ✅ 존재 |
| MLBPark    | `test_mlbpark_playwright.py`  | ✅ 존재 |
| 뽐뿌       | `test_best_humor_scraping.py` | ✅ 존재 |
| 유머대학   | `test_humoruniv.py`           | ✅ 존재 |
| 개드립     | `test_dogdrip.py`             | ✅ 존재 |
| 클리앙     | `test_clien.py`               | ✅ 존재 |
| 루리웹     | `test_site.py`                | ✅ 존재 |
| 오늘의유머 | `test_with_playwright.py`     | ✅ 존재 |

### 4.2 인프라 테스트

| 테스트      | 파일                | 설명               |
| ----------- | ------------------- | ------------------ |
| R2 업로드   | `test_r2_upload.py` | Cloudflare R2 연결 |
| 미디어 처리 | `test_media.py`     | 이미지/GIF/비디오  |

### 4.3 실행 방법

```bash
cd crawler
source venv/bin/activate

# 특정 사이트 테스트
pytest test_fmkorea_playwright.py -v

# 전체 E2E 테스트
pytest test_*.py -v --ignore=tests/
```

---

## 📊 테스트 커버리지 목표

| 영역        | 현재 | 목표 |
| ----------- | ---- | ---- |
| 웹앱 Unit   | 0%   | 60%  |
| 웹앱 E2E    | 0%   | 80%  |
| 크롤러 Unit | ~30% | 70%  |
| 크롤러 E2E  | ~20% | 60%  |

---

## ⏰ 테스트 실행 일정

### 빠른 테스트 (CI용, 5분)

```bash
# 웹앱 타입 체크
cd webapp && npm run check

# 크롤러 Unit 테스트
cd ../crawler && pytest tests/ -v --tb=short
```

### 전체 테스트 (배포 전, 30분)

```bash
# 1. 웹앱 전체
cd webapp
npm run check
npm run test:unit -- --run
npm run test:e2e

# 2. 크롤러 전체
cd ../crawler
pytest tests/ -v
pytest test_*.py -v --ignore=tests/
```

---

## 📝 테스트 작성 규칙

### 웹앱 (Vitest + Playwright)

```typescript
// src/lib/components/ComponentName.test.ts
import { describe, it, expect } from "vitest";
import { render } from "@testing-library/svelte";
import ComponentName from "./ComponentName.svelte";

describe("ComponentName", () => {
  it("should render correctly", () => {
    const { getByText } = render(ComponentName, { props: {} });
    expect(getByText("expected text")).toBeTruthy();
  });
});
```

### 크롤러 (pytest)

```python
# tests/test_feature.py
import pytest
from module import function

class TestFeature:
    def test_basic_case(self):
        result = function(input)
        assert result == expected

    def test_error_case(self):
        with pytest.raises(ExpectedError):
            function(bad_input)
```

---

## 🚀 다음 단계

### Phase 1: 기존 테스트 실행 및 수정 (1시간)

1. [ ] 웹앱 기존 테스트 실행
2. [ ] 크롤러 기존 Unit 테스트 실행
3. [ ] 실패하는 테스트 수정

### Phase 2: 핵심 기능 테스트 추가 (2시간)

1. [ ] 댓글 CRUD E2E 테스트
2. [ ] 좋아요 기능 E2E 테스트
3. [ ] 인증 흐름 E2E 테스트

### Phase 3: 커버리지 확대 (3시간)

1. [ ] 컴포넌트 Unit 테스트
2. [ ] 유틸리티 Unit 테스트
3. [ ] 크롤러 사이트별 테스트 검증

---

## 📌 테스트 실행 명령어 요약

```bash
# 웹앱
cd webapp
npm run check              # 타입 체크
npm run test:unit          # Unit 테스트 (watch mode)
npm run test:unit -- --run # Unit 테스트 (1회 실행)
npm run test:e2e           # E2E 테스트
npm test                   # 전체 테스트

# 크롤러
cd crawler
source venv/bin/activate
pytest tests/ -v                    # Unit 테스트
pytest test_*.py -v --ignore=tests/ # E2E 테스트
pytest --cov=. --cov-report=html    # 커버리지
```
