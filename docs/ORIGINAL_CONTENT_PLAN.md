# 🎯 원본 콘텐츠 확보 프로젝트 기획서

> **목표**: Google AdSense 승인 가능성 90% → 95%+로 향상  
> **작성일**: 2026년 1월 12일  
> **작성자**: KEERO 개발팀

---

## 📌 프로젝트 개요

### 배경 및 문제점

**현재 상황:**

- KEERO는 외부 커뮤니티 콘텐츠 집계(aggregation) 사이트
- 모든 게시글은 외부에서 크롤링한 콘텐츠
- Google AdSense는 "원본 콘텐츠"를 중요하게 평가

**Google AdSense 정책:**

> "사이트에서 독창적이고 관련성 높은 콘텐츠를 제공해야 합니다. 콘텐츠를 다른 사이트에서 복사하거나
> 최소한의 부가가치만 제공하는 경우 승인이 거부될 수 있습니다."

**목표:**

- 원본 콘텐츠 비중 30% 이상 확보
- 사용자 참여 활성화
- 커뮤니티 가치 증대

---

## 🎨 핵심 전략

### 3단계 접근법

```
Phase 1: 즉시 구현 (1-2일)
└─ 주간 하이라이트 페이지
└─ 베스트 댓글 모음 페이지

Phase 2: 단기 구현 (1주일)
└─ 트렌드 리포트 페이지
└─ 에디터 Pick 시스템

Phase 3: 중장기 구현 (2-4주)
└─ 사용자 큐레이션 시스템
└─ 커뮤니티 블로그
```

---

## 📋 Phase 1: 즉시 구현 기능

### 1. 주간 하이라이트 페이지

#### 개요

- **URL**: `/highlights/weekly`
- **목적**: 주간 인기 게시글에 대한 에디터 코멘트와 커뮤니티 반응 종합
- **업데이트**: 매주 월요일 자동 생성

#### 주요 기능

```
📊 주간 하이라이트 구성:
├─ 헤더: "이번 주 유머 하이라이트 (YYYY년 MM월 DD일 - DD일)"
├─ 통계 요약
│  ├─ 총 게시글 수
│  ├─ 총 댓글 수
│  ├─ 총 좋아요 수
│  └─ 가장 활발한 사이트
├─ TOP 10 게시글
│  ├─ 순위 (🥇🥈🥉 + 4-10위)
│  ├─ 게시글 정보 (제목, 출처, 날짜)
│  ├─ 📝 에디터 코멘트 (50-100자)
│  ├─ 💬 베스트 댓글 3개
│  │  ├─ 댓글 내용
│  │  ├─ 작성자
│  │  └─ 좋아요 수
│  └─ 📈 반응 통계
│     ├─ 좋아요 수
│     ├─ 댓글 수
│     └─ 조회수 (추후 추가)
└─ 푸터: 이전 주차 아카이브 링크
```

#### 데이터베이스 스키마

**신규 테이블: `highlights`**

```sql
CREATE TABLE highlights (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    week_start DATE NOT NULL,              -- 주 시작일 (월요일)
    week_end DATE NOT NULL,                -- 주 종료일 (일요일)
    post_id INTEGER NOT NULL,              -- 게시글 ID
    rank INTEGER NOT NULL,                 -- 순위 (1-10)
    editor_comment TEXT,                   -- 에디터 코멘트
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (post_id) REFERENCES posts(id),
    UNIQUE(week_start, post_id)
);

CREATE INDEX idx_highlights_week ON highlights(week_start);
```

#### UI 설계

**레이아웃:**

```
┌─────────────────────────────────────┐
│  📅 이번 주 유머 하이라이트          │
│  2026년 1월 6일 - 1월 12일          │
├─────────────────────────────────────┤
│  📊 이번 주 통계                     │
│  게시글 234개 | 댓글 1,234개 | ...  │
├─────────────────────────────────────┤
│  🥇 1위: [게시글 제목]             │
│  ┌───────────────────────────────┐  │
│  │ 📝 에디터: "이번 주 최고!"    │  │
│  │ 💬 베스트 댓글:               │  │
│  │   "ㅋㅋㅋ 진짜 웃겨" (45👍)   │  │
│  │ 📈 좋아요 234 · 댓글 89       │  │
│  └───────────────────────────────┘  │
├─────────────────────────────────────┤
│  🥈 2위: [게시글 제목]             │
│  ...                                 │
└─────────────────────────────────────┘
```

#### 구현 상세

**파일 구조:**

```
webapp/src/routes/highlights/
├── weekly/
│   ├── +page.server.ts          # 데이터 로드
│   ├── +page.svelte             # UI
│   └── [weekId]/
│       ├── +page.server.ts      # 특정 주차 데이터
│       └── +page.svelte         # 아카이브 페이지
└── +page.svelte                 # 리다이렉트 (최신 주차로)
```

**+page.server.ts 로직:**

```typescript
export const load: PageServerLoad = async () => {
    // 1. 이번 주 시작일/종료일 계산 (월-일)
    const weekStart = getMonday(new Date())
    const weekEnd = getSunday(new Date())

    // 2. 주간 TOP 10 게시글 조회
    const weeklyTop10 = await db
        .select(...)
        .where(between(posts.crawled_at, weekStart, weekEnd))
        .orderBy(desc(like_count))
        .limit(10)

    // 3. 각 게시글의 베스트 댓글 3개 조회
    for (const post of weeklyTop10) {
        post.bestComments = await db
            .select(...)
            .where(eq(comments.post_id, post.id))
            .orderBy(desc(comment_likes))
            .limit(3)
    }

    // 4. 에디터 코멘트 조회 (DB 또는 기본값)
    const highlights = await db
        .select(...)
        .where(eq(highlights.week_start, weekStart))

    // 5. 주간 통계
    const weekStats = {
        totalPosts: ...,
        totalComments: ...,
        totalLikes: ...,
        topSite: ...
    }

    return {
        weekStart,
        weekEnd,
        weeklyTop10,
        highlights,
        weekStats
    }
}
```

**에디터 코멘트 관리:**

- **초기 방안**: 하드코딩 또는 기본 템플릿
  ```typescript
  const defaultComments = {
    1: "이번 주 가장 많은 사랑을 받은 게시글!",
    2: "댓글 반응이 뜨거웠던 게시글!",
    3: "조용히 인기를 끌고 있는 숨은 보석!",
  };
  ```
- **추후 개선**: Admin 페이지에서 직접 작성

#### SEO 최적화

```html
<!-- 메타 태그 -->
<title>이번 주 유머 하이라이트 - KEERO</title>
<meta
  name="description"
  content="2026년 1월 6일-12일 주간 베스트 유머 게시글 TOP 10과 인기 댓글"
/>
<meta property="og:type" content="article" />
<meta property="article:published_time" content="{weekStart}" />

<!-- 구조화 데이터 (JSON-LD) -->
{ "@context": "https://schema.org", "@type": "Article", "headline": "이번 주
유머 하이라이트", "datePublished": "{weekStart}", "author": { "@type":
"Organization", "name": "KEERO" } }
```

---

### 2. 베스트 댓글 모음 페이지

#### 개요

- **URL**: `/best-comments`
- **목적**: 재치있고 인기 있는 댓글을 모아서 보여줌
- **업데이트**: 실시간 (좋아요 수 기반)

#### 주요 기능

```
💬 베스트 댓글 구성:
├─ 헤더: "커뮤니티 베스트 댓글"
├─ 필터
│  ├─ 기간: 전체 / 이번 주 / 이번 달
│  └─ 사이트: 전체 / 뽐뿌 / FM코리아 / ...
├─ 댓글 리스트 (페이지네이션)
│  ├─ 댓글 내용
│  ├─ 작성자 (닉네임)
│  ├─ 원본 게시글 링크
│  ├─ 좋아요 수
│  └─ 작성 시간
└─ 페이지네이션 (20개씩)
```

#### 데이터베이스 쿼리

```typescript
// 기존 테이블 활용, 추가 스키마 불필요
const bestComments = await db
  .select({
    id: comments.id,
    content: comments.content,
    author: users.display_name,
    post_title: posts.title,
    post_id: posts.id,
    likes: sql`(SELECT COUNT(*) FROM comment_likes WHERE comment_id = comments.id)`,
    created_at: comments.created_at,
  })
  .from(comments)
  .leftJoin(users, eq(comments.user_id, users.id))
  .leftJoin(posts, eq(comments.post_id, posts.id))
  .where(eq(comments.is_deleted, 0))
  .orderBy(desc(sql`likes`))
  .limit(100);
```

#### UI 설계

**카드 형태:**

```
┌─────────────────────────────────────┐
│ 💬 ㅋㅋㅋㅋ 이거 진짜 웃기네요      │
│                                     │
│ 👤 사용자123 · 2024-01-10          │
│ 👍 45 · 원본: [게시글 제목]       │
└─────────────────────────────────────┘
```

---

## 📋 Phase 2: 단기 구현 기능

### 3. 트렌드 리포트 페이지

#### 개요

- **URL**: `/trends`
- **목적**: 주간/월간 유머 트렌드 분석
- **업데이트**: 매일 자동 업데이트

#### 주요 기능

```
📈 트렌드 리포트 구성:
├─ 핫 키워드 (워드 클라우드)
├─ 사이트별 활동 비교 (차트)
├─ 시간대별 활동 패턴 (그래프)
├─ 주제별 인기 순위
└─ 댓글 참여율 통계
```

#### 데이터 수집 (신규 작업)

**필요한 테이블:**

```sql
-- 키워드 추출 결과 저장
CREATE TABLE trending_keywords (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    keyword TEXT NOT NULL,
    count INTEGER NOT NULL,
    date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**키워드 추출 방법:**

- 옵션 1: Python 크롤러에서 제목/내용 형태소 분석
- 옵션 2: 클라이언트 사이드 간단한 단어 빈도 분석
- 옵션 3: 수동 태깅 (초기 단계)

---

### 4. 에디터 Pick 시스템

#### 개요

- 주간 하이라이트에 에디터가 직접 코멘트 작성
- Admin 페이지에서 관리

#### Admin UI

```
/admin/highlights
├─ 이번 주 TOP 10 게시글 목록
├─ 각 게시글마다 "코멘트 작성" 버튼
└─ 코멘트 입력 폼 (50-100자 제한)
```

---

## 📋 Phase 3: 중장기 구현 기능

### 5. 사용자 큐레이션 시스템

#### 개요

- 사용자가 직접 "이주의 베스트" 투표
- 투표 이유를 댓글로 작성 (필수)

#### 주요 기능

```
🗳️ 커뮤니티 Pick:
├─ 매주 목요일 투표 시작
├─ 일요일 자정 투표 마감
├─ 월요일 결과 발표
└─ 투표 이유 베스트 댓글 선정
```

#### 데이터베이스

```sql
CREATE TABLE community_picks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    week_start DATE NOT NULL,
    post_id INTEGER NOT NULL,
    user_id TEXT NOT NULL,
    vote_reason TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (post_id) REFERENCES posts(id),
    UNIQUE(week_start, post_id, user_id)
);
```

---

### 6. 커뮤니티 블로그

#### 개요

- 사용자가 직접 유머 관련 글 작성
- 에디터 승인 후 게시

#### 주제 예시

- "이번 달 가장 웃긴 밈 분석"
- "커뮤니티별 유머 스타일 차이"
- "유머 게시글 작성 팁"

---

## 🗓️ 구현 일정

### Week 1 (즉시 시작)

**Day 1-2:**

- [ ] 데이터베이스 스키마 생성 (`highlights` 테이블)
- [ ] `/highlights/weekly` 페이지 구현
- [ ] 주간 TOP 10 데이터 로드 로직
- [ ] 베스트 댓글 3개 조회 로직

**Day 3-4:**

- [ ] 에디터 코멘트 기본 템플릿 구현
- [ ] UI 디자인 및 반응형 레이아웃
- [ ] SEO 메타 태그 추가
- [ ] `/best-comments` 페이지 구현

**Day 5-7:**

- [ ] 테스트 및 버그 수정
- [ ] 성능 최적화
- [ ] Railway 배포
- [ ] Google Analytics 확인

### Week 2 (추가 기능)

- [ ] 트렌드 리포트 페이지
- [ ] Admin에서 에디터 코멘트 작성 기능
- [ ] 아카이브 페이지 (과거 주차)

### Week 3-4 (확장)

- [ ] 사용자 큐레이션 시스템
- [ ] 커뮤니티 블로그 (선택)

---

## 📊 성과 측정

### KPI (핵심 성과 지표)

| 지표                  | 현재        | 목표 (1달 후) |
| --------------------- | ----------- | ------------- |
| 원본 콘텐츠 페이지 수 | 1개 (stats) | 10개+         |
| 주간 에디터 코멘트    | 0개         | 10개/주       |
| 베스트 댓글 조회수    | 0           | 500+/주       |
| AdSense 승인 가능성   | 90%         | 95%+          |

### Google AdSense 심사 기준 충족도

| 기준          | 개선 전 | 개선 후      |
| ------------- | ------- | ------------ |
| 원본 콘텐츠   | ⚠️ 부족 | ✅ 충분      |
| 콘텐츠 품질   | 🟡 보통 | ✅ 우수      |
| 사용자 참여   | ✅ 좋음 | ✅ 매우 좋음 |
| 정기 업데이트 | ✅ 우수 | ✅ 우수      |
| 사이트 구조   | ✅ 우수 | ✅ 우수      |

---

## 💰 예상 비용

**개발 비용:**

- Phase 1: 무료 (기존 인프라 활용)
- Phase 2: 무료 (추가 스토리지 불필요)
- Phase 3: 무료

**운영 비용:**

- 에디터 코멘트 작성 시간: 주 1시간
- 월간 운영 비용: $0 (자동화)

---

## 🎯 성공 기준

### Phase 1 완료 조건

- [x] `/highlights/weekly` 페이지 정상 작동
- [x] TOP 10 게시글 자동 선정
- [x] 베스트 댓글 3개 표시
- [x] SEO 메타 태그 완성
- [x] `/best-comments` 페이지 정상 작동

### AdSense 승인 신청 조건

- [x] 최소 4주간의 주간 하이라이트 아카이브
- [x] 에디터 코멘트 40개 이상
- [x] 베스트 댓글 페이지 트래픽 유입 확인
- [x] Google Analytics에서 원본 콘텐츠 페이지 조회수 확인

---

## 📝 참고 자료

### Google AdSense 정책

- [콘텐츠 정책](https://support.google.com/adsense/answer/9335567)
- [승인 기준](https://support.google.com/adsense/answer/9724)

### 유사 사례

- **Reddit**: 커뮤니티 큐레이션
- **Product Hunt**: 일간/주간 TOP 선정
- **Hacker News**: 사용자 투표 시스템

---

## 🔄 업데이트 이력

| 날짜       | 버전 | 변경사항  |
| ---------- | ---- | --------- |
| 2026-01-12 | v1.0 | 초안 작성 |

---

**작성자**: KEERO 개발팀  
**검토자**: -  
**승인자**: -
