# 📋 원본 콘텐츠 확보 - 빠른 실행 가이드

> **빠른 요약**: 2-3일 안에 AdSense 승인 가능성을 90% → 95%+로 높이는 방법

---

## 🎯 핵심 전략

### 즉시 구현할 2가지 기능

1. **주간 하이라이트** (`/highlights/weekly`)

   - 매주 TOP 10 게시글 + 에디터 코멘트
   - 베스트 댓글 3개 표시
   - 주간 통계 요약

2. **베스트 댓글 모음** (`/best-comments`)
   - 좋아요 많은 댓글 TOP 100
   - 원본 게시글 링크
   - 실시간 업데이트

---

## ⚡ 빠른 시작

### 1단계: 데이터베이스 스키마 추가 (5분)

```sql
-- webapp/src/lib/server/schema.ts에 추가

export const highlights = sqliteTable('highlights', {
    id: integer('id').primaryKey({ autoIncrement: true }),
    weekStart: text('week_start').notNull(),
    weekEnd: text('week_end').notNull(),
    postId: integer('post_id').notNull().references(() => posts.id),
    rank: integer('rank').notNull(),
    editorComment: text('editor_comment'),
    createdAt: text('created_at').default(sql`CURRENT_TIMESTAMP`)
})
```

### 2단계: 주간 하이라이트 페이지 생성 (1-2시간)

```bash
# 파일 생성
webapp/src/routes/highlights/weekly/
├── +page.server.ts
└── +page.svelte
```

### 3단계: 베스트 댓글 페이지 생성 (30분)

```bash
# 파일 생성
webapp/src/routes/best-comments/
├── +page.server.ts
└── +page.svelte
```

### 4단계: Footer 링크 추가 (5분)

```svelte
<!-- webapp/src/lib/components/Footer.svelte -->
<li>
    <a href="/highlights/weekly">주간 하이라이트</a>
</li>
<li>
    <a href="/best-comments">베스트 댓글</a>
</li>
```

---

## 📊 예상 결과

### 원본 콘텐츠 증가

| 항목               | 추가되는 콘텐츠                                 |
| ------------------ | ----------------------------------------------- |
| 주간 하이라이트    | 주당 10개 에디터 코멘트 + 30개 베스트 댓글 분석 |
| 베스트 댓글 페이지 | 100개 큐레이션 + 설명                           |
| 4주 후 누적        | **약 300개 원본 콘텐츠 아이템**                 |

### AdSense 승인 타임라인

```
Week 1: 기능 구현 및 배포
Week 2-4: 콘텐츠 누적 (최소 4주 운영 권장)
Week 5: AdSense 신청
Week 6-7: 심사 대기
Week 8: 승인 🎉
```

---

## 🎨 UI 미리보기

### 주간 하이라이트 페이지

```
┌────────────────────────────────────────┐
│ 📅 이번 주 유머 하이라이트              │
│ 2026년 1월 6일 - 1월 12일              │
├────────────────────────────────────────┤
│ 📊 이번 주 통계                         │
│ 게시글 234 | 댓글 1,234 | 좋아요 5,678 │
├────────────────────────────────────────┤
│                                        │
│ 🥇 1위: 오늘 회사에서 있었던 일       │
│ ┌──────────────────────────────────┐  │
│ │ 📝 에디터의 한마디                │  │
│ │ "이번 주 가장 많은 웃음을 준 글!  │  │
│ │  댓글 반응도 폭발적이었습니다"    │  │
│ │                                  │  │
│ │ 💬 베스트 댓글 TOP 3             │  │
│ │ ① "ㅋㅋㅋㅋ 진짜?" (👍 45)      │  │
│ │ ② "이거 실화냐" (👍 32)         │  │
│ │ ③ "나도 비슷한..." (👍 28)      │  │
│ │                                  │  │
│ │ 📈 반응 통계                     │  │
│ │ 좋아요 234개 · 댓글 89개         │  │
│ └──────────────────────────────────┘  │
│                                        │
│ 🥈 2위: ...                           │
└────────────────────────────────────────┘
```

---

## 🚀 다음 단계

### 즉시 시작 가능한 작업

**우선순위 1: 데이터베이스 마이그레이션**

```bash
# schema.ts 수정 후
cd webapp
npm run db:push
```

**우선순위 2: 주간 하이라이트 페이지**

- [ ] +page.server.ts 작성
- [ ] +page.svelte 작성
- [ ] SEO 메타 태그 추가

**우선순위 3: 베스트 댓글 페이지**

- [ ] +page.server.ts 작성 (간단)
- [ ] +page.svelte 작성
- [ ] 페이지네이션 추가

**우선순위 4: 테스트 및 배포**

- [ ] 로컬 테스트
- [ ] Railway 배포
- [ ] Google Analytics 확인

---

## 💡 에디터 코멘트 작성 팁

### 초기 단계 (자동 생성)

```typescript
// 기본 템플릿 사용
const defaultComments = {
  1: "🏆 이번 주 가장 많은 사랑을 받은 게시글입니다!",
  2: "🔥 댓글 반응이 뜨거웠던 화제의 글!",
  3: "💎 조용히 인기를 끌고 있는 숨은 보석 같은 글",
  4: "😂 웃음이 터져나오는 재미있는 글",
  5: "👏 많은 공감을 얻은 글",
};
```

### 고도화 (Admin 페이지)

```
/admin/highlights/weekly
- 이번 주 TOP 10 목록
- 각 게시글마다 "코멘트 작성" 버튼
- 50-100자 제한 입력 폼
```

---

## 📈 성공 지표

### 1주일 후 확인사항

- [ ] 주간 하이라이트 1회 게시
- [ ] 에디터 코멘트 10개 작성
- [ ] 베스트 댓글 페이지 조회수 50+

### 4주일 후 확인사항

- [ ] 주간 하이라이트 4회 누적
- [ ] 에디터 코멘트 40개 누적
- [ ] Google Analytics에서 원본 콘텐츠 페이지 유입 확인
- [ ] AdSense 신청 준비 완료

---

## ❓ FAQ

**Q: 에디터 코멘트를 매번 작성해야 하나요?**  
A: 초기에는 템플릿을 사용하고, 여유가 생기면 직접 작성하세요.

**Q: 베스트 댓글은 어떻게 선정하나요?**  
A: 좋아요 수로 자동 선정됩니다.

**Q: 언제 AdSense를 신청하나요?**  
A: 최소 4주간 콘텐츠를 누적한 후 신청하는 것이 좋습니다.

**Q: 다른 작업은 언제 하나요?**  
A: Phase 1 완료 후 2-4주 뒤에 진행하세요.

---

**상세 기획서**: [ORIGINAL_CONTENT_PLAN.md](./ORIGINAL_CONTENT_PLAN.md)
