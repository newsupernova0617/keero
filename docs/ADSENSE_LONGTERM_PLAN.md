# 📋 애드센스 승인률 향상을 위한 중장기 개선 계획

> **작성일**: 2026년 1월 12일  
> **목표**: 애드센스 승인 가능성 85-90% → 95%+ 향상  
> **예상 소요 시간**: 2-3일

---

## 📊 현재 상태 분석

### 강점 ✅

- 필수 법적 페이지 완비 (개인정보처리방침, 이용약관, 문의하기)
- SEO 메타 태그 최적화 완료
- 정기적인 콘텐츠 업데이트 (10분마다 자동 크롤링)
- 반응형 디자인
- 다크 모드 지원

### 약점 ⚠️

- **원본 콘텐츠 부족**: 모든 게시글이 외부 사이트에서 수집됨
- **분석 도구 미연동**: Google Analytics/Search Console 없음
- **DMCA 정책 페이지 없음**: 저작권 정책이 About 페이지에만 간략하게 명시

### Google의 콘텐츠 평가 기준

1. **원본성 (Originality)**: 자체 생성 콘텐츠 존재 여부
2. **가치 추가 (Value-Add)**: 단순 수집이 아닌 부가가치 제공
3. **사용자 경험 (UX)**: 사이트 구조, 탐색 편의성
4. **신뢰성 (Trust)**: 운영 정보, 연락처, 법적 페이지

---

## 🎯 개선 목표

| 영역            | 현재 | 목표                 |
| --------------- | ---- | -------------------- |
| 원본 콘텐츠     | 0%   | 10-20% (주요 페이지) |
| 통계/분석       | 없음 | GA + Search Console  |
| 법적 페이지     | 3개  | 4개 (DMCA 추가)      |
| 부가가치 콘텐츠 | 없음 | 랭킹, 통계, 에디터픽 |

---

## 📁 개선 항목별 상세 계획

---

## 1️⃣ 원본 콘텐츠 섹션 추가

### 1.1 주간/월간 베스트 통계 페이지 (`/stats`)

**목적**: 자체 분석 콘텐츠로 원본성 확보

**페이지 구성**:

```
/stats
├── 주간 베스트 게시글 TOP 10 (좋아요 기준)
├── 월간 베스트 게시글 TOP 10
├── 사이트별 인기 순위
├── 트렌드 그래프 (선택)
└── 댓글 활발도 순위
```

**구현 계획**:

```typescript
// webapp/src/routes/stats/+page.server.ts
export async function load() {
  // 주간 베스트 (최근 7일 좋아요 순)
  const weeklyBest = await db
    .select()
    .from(posts)
    .where(sql`crawled_at > datetime('now', '-7 days')`)
    .orderBy(desc(posts.like_count))
    .limit(10);

  // 월간 베스트
  const monthlyBest = await db
    .select()
    .from(posts)
    .where(sql`crawled_at > datetime('now', '-30 days')`)
    .orderBy(desc(posts.like_count))
    .limit(10);

  // 사이트별 통계
  const siteStats = await db
    .select({
      site_name: posts.site_name,
      count: count(),
    })
    .from(posts)
    .groupBy(posts.site_name);

  return { weeklyBest, monthlyBest, siteStats };
}
```

**UI 디자인 요소**:

- 카드 그리드로 순위 표시
- 순위 변동 표시 (↑↓)
- 사이트별 색상 구분
- 공유 버튼

**예상 작업 시간**: 2-3시간

---

### 1.2 에디터 Pick 섹션 (메인 페이지 또는 `/picks`)

**목적**: 편집자의 선별이라는 부가가치 제공

**구현 방식**:

**옵션 A: 자동 선별 (추천)**

```typescript
// 조건: 좋아요 10개 이상 + 댓글 5개 이상
// 라벨링: "에디터 Pick" 배지 표시

// 게시글 조회 시 조건 추가
const editorPicks = await db
  .select()
  .from(posts)
  .where(and(gte(posts.like_count, 10), gte(posts.comment_count, 5)))
  .orderBy(desc(posts.crawled_at))
  .limit(5);
```

**옵션 B: 관리자 수동 선별**

```sql
-- posts 테이블에 컬럼 추가
ALTER TABLE posts ADD COLUMN is_editor_pick BOOLEAN DEFAULT FALSE;
ALTER TABLE posts ADD COLUMN editor_comment TEXT;
```

**UI 표시**:

- 메인 페이지 상단에 "오늘의 Pick" 섹션
- 특별한 배지 또는 테두리 스타일
- 선별 이유 코멘트 (옵션 B)

**예상 작업 시간**: 1-2시간

---

### 1.3 카테고리/태그 분류 시스템 강화

**현재 상태**: 사이트명으로만 구분 (ppomppu, fmkorea 등)

**개선안**:

```sql
-- 카테고리 테이블 추가
CREATE TABLE categories (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,      -- '웃긴짤', '유머', '움짤', '이슈' 등
    slug TEXT UNIQUE,
    icon TEXT
);

-- posts 테이블에 카테고리 연결
ALTER TABLE posts ADD COLUMN category_id INTEGER REFERENCES categories(id);
```

**자동 분류 로직**:

```typescript
// 제목/내용 기반 자동 태깅
const categories = {
  움짤: ["gif", "움짤", "GIF"],
  유머: ["ㅋㅋ", "ㅎㅎ", "웃긴", "레전드"],
  이슈: ["속보", "논란", "충격"],
  일상: ["일상", "오늘", "어제"],
};
```

**예상 작업 시간**: 2-3시간

---

## 2️⃣ Google Analytics & Search Console 연동

### 2.1 Google Analytics 4 (GA4) 연동

**파일**: `webapp/src/app.html`

**추가할 코드**:

```html
<head>
  <!-- 기존 코드 -->

  <!-- Google Analytics 4 -->
  <script
    async
    src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"
  ></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag() {
      dataLayer.push(arguments);
    }
    gtag("js", new Date());
    gtag("config", "G-XXXXXXXXXX");
  </script>
</head>
```

**환경 변수 사용 (권장)**:

```html
<!-- webapp/src/app.html -->
%sveltekit.head%

<!-- 또는 별도 컴포넌트로 분리 -->
```

**별도 컴포넌트 생성**:

```svelte
<!-- webapp/src/lib/components/GoogleAnalytics.svelte -->
<script lang="ts">
    import { env } from '$env/dynamic/public'

    const gaId = env.PUBLIC_GA_MEASUREMENT_ID
</script>

{#if gaId}
    <svelte:head>
        <script async src="https://www.googletagmanager.com/gtag/js?id={gaId}"></script>
        <script>
            window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            gtag('js', new Date());
            gtag('config', '{gaId}');
        </script>
    </svelte:head>
{/if}
```

**환경 변수**:

```bash
# .env
PUBLIC_GA_MEASUREMENT_ID=G-XXXXXXXXXX
```

**예상 작업 시간**: 30분

---

### 2.2 Google Search Console 등록

**1단계: 소유권 확인 (HTML 태그 방식)**

**파일**: `webapp/src/app.html`

```html
<head>
  <!-- Google Search Console 확인 -->
  <meta name="google-site-verification" content="YOUR_VERIFICATION_CODE" />
</head>
```

**2단계: Sitemap 제출**

- Search Console에서 `/sitemap.xml` URL 제출
- 이미 동적 생성되어 있음 ✅

**3단계: 인덱싱 요청**

- 주요 페이지 URL 개별 인덱싱 요청

**예상 작업 시간**: 15분 (설정만)

---

## 3️⃣ DMCA 정책 페이지 생성

### 3.1 DMCA 페이지 (`/dmca`)

**목적**: 저작권 침해 신고 절차 명확화

**페이지 구조**:

```markdown
# DMCA 정책

## 저작권 보호 정책

KEERO는 저작권을 존중합니다...

## 저작권 침해 신고 절차

1. 이메일 제출: keero1356@gmail.com
2. 필수 정보:
   - 저작물 URL (원본)
   - 침해 콘텐츠 URL (KEERO)
   - 본인 확인 정보
   - 저작권 소유 증명

## 처리 절차

1. 신고 접수: 24시간 이내 확인
2. 검토: 48시간 이내
3. 조치: 확인 시 즉시 삭제

## 반복 침해자 정책

반복적인 저작권 침해 콘텐츠는 영구 차단됩니다.

## 면책 조항

...
```

**구현 파일**:

- `webapp/src/routes/dmca/+page.svelte`

**Footer에 추가**:

```svelte
<li>
    <a href="/dmca" class="text-muted-foreground transition hover:text-foreground">
        저작권 정책 (DMCA)
    </a>
</li>
```

**Sitemap에 추가**:

```xml
<url>
    <loc>${baseUrl}/dmca</loc>
    <changefreq>yearly</changefreq>
    <priority>0.5</priority>
</url>
```

**예상 작업 시간**: 1시간

---

## 4️⃣ 추가 권장 개선 사항

### 4.1 404 에러 페이지 개선

**현재**: 기본 404 페이지

**개선안**: 커스텀 404 페이지

```svelte
<!-- webapp/src/routes/+error.svelte -->
<script>
    import { page } from '$app/stores'
    import { Button } from '$lib/components/ui/button'
</script>

<div class="flex flex-col items-center justify-center min-h-[60vh] text-center">
    <h1 class="text-6xl font-bold text-primary mb-4">404</h1>
    <p class="text-xl text-muted-foreground mb-8">
        페이지를 찾을 수 없습니다
    </p>
    <Button href="/">홈으로 돌아가기</Button>
</div>
```

**예상 작업 시간**: 30분

---

### 4.2 로딩 상태 개선

**현재**: 페이지 로딩 시 빈 화면

**개선안**: 스켈레톤 UI 또는 로딩 스피너

- 이미 `PostCardSkeleton` 컴포넌트 있음 ✅
- 다른 페이지에도 적용

---

### 4.3 Breadcrumb 네비게이션 추가

**목적**: 사이트 구조 명확화, SEO 개선

**구현**:

```svelte
<!-- webapp/src/lib/components/Breadcrumb.svelte -->
<nav aria-label="breadcrumb">
    <ol class="flex items-center gap-2 text-sm text-muted-foreground">
        <li><a href="/">홈</a></li>
        <li>/</li>
        <li class="text-foreground">게시글</li>
    </ol>
</nav>
```

---

## 📅 구현 일정 (권장)

### Day 1: 핵심 원본 콘텐츠 (3-4시간)

| 시간  | 작업                      |
| ----- | ------------------------- |
| 1시간 | `/stats` 통계 페이지 생성 |
| 1시간 | 에디터 Pick 섹션 추가     |
| 1시간 | DMCA 정책 페이지 생성     |
| 30분  | Footer, Sitemap 업데이트  |

### Day 2: 분석 도구 & 마무리 (1-2시간)

| 시간 | 작업                  |
| ---- | --------------------- |
| 30분 | Google Analytics 연동 |
| 15분 | Search Console 등록   |
| 30분 | 404 페이지 개선       |
| 30분 | 테스트 및 배포        |

---

## 🏆 우선순위 랭킹

### 🥇 최우선 (High Impact)

1. **통계 페이지 (`/stats`)** - 원본 콘텐츠로 가장 효과적
2. **DMCA 페이지** - 저작권 신뢰성 확보

### 🥈 권장 (Medium Impact)

3. **Google Analytics** - 트래픽 분석
4. **Search Console** - 검색 인덱싱
5. **에디터 Pick** - 부가가치 제공

### 🥉 선택 (Nice to Have)

6. **404 페이지 개선** - UX 향상
7. **카테고리 시스템** - 추후 확장
8. **Breadcrumb** - SEO 미세 개선

---

## 🎯 예상 결과

### 개선 전

- **원본 콘텐츠**: 0%
- **승인 가능성**: 85-90%

### 개선 후 (Day 1 완료 시)

- **원본 콘텐츠**: ~15%
- **승인 가능성**: 92-95%

### 개선 후 (Day 2 완료 시)

- **원본 콘텐츠**: ~20%
- **분석 도구**: 연동 완료
- **승인 가능성**: 95%+

---

## ✅ 체크리스트

### Day 1

- [ ] `/stats` 통계 페이지 생성
- [ ] 에디터 Pick 섹션 (메인 또는 별도 페이지)
- [ ] `/dmca` DMCA 정책 페이지 생성
- [ ] Footer에 DMCA 링크 추가
- [ ] Sitemap에 새 페이지 추가

### Day 2

- [ ] Google Analytics 연동
- [ ] Search Console 등록 및 인증
- [ ] 404 에러 페이지 개선
- [ ] 전체 테스트
- [ ] Production 배포

---

## 📝 참고 사항

### AdSense 승인 후 주의사항

1. 콘텐츠 업데이트 유지 (현재 자동화 ✅)
2. 광고 배치 정책 준수
3. 부정 클릭 방지
4. 정기적인 성과 모니터링

### 예상 수익 (참고)

- **RPM** (1000 페이지뷰당): $1-3 (한국 기준)
- **일 방문자 1,000명 기준**: 월 $30-90 예상
- **일 방문자 10,000명 기준**: 월 $300-900 예상

---

**작성 완료**: 2026년 1월 12일  
**다음 단계**: 구현 착수 또는 현재 상태로 신청
