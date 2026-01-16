# ✅ 원본 콘텐츠 확보 - 구현 체크리스트

> **목표**: AdSense 승인 가능성 95%+ 달성  
> **기간**: 2-3일 (Phase 1만 구현 시)

---

## 📋 Phase 1: 즉시 구현 (필수)

### 1️⃣ 데이터베이스 준비

- [ ] `webapp/src/lib/server/schema.ts`에 `highlights` 테이블 추가
- [ ] `drizzle.config.ts` 확인
- [ ] `npm run db:push` 실행하여 스키마 적용
- [ ] 데이터베이스 마이그레이션 확인

### 2️⃣ 주간 하이라이트 페이지 `/highlights/weekly`

**백엔드 (Server):**

- [ ] `webapp/src/routes/highlights/weekly/+page.server.ts` 생성
- [ ] 이번 주 시작일/종료일 계산 함수 구현
- [ ] 주간 TOP 10 게시글 조회 쿼리 작성
- [ ] 각 게시글의 베스트 댓글 3개 조회 로직 추가
- [ ] 에디터 코멘트 기본 템플릿 구현
- [ ] 주간 통계 데이터 조회 (총 게시글, 댓글, 좋아요)
- [ ] 데이터 리턴 구조 완성

**프론트엔드 (UI):**

- [ ] `webapp/src/routes/highlights/weekly/+page.svelte` 생성
- [ ] 페이지 헤더 구현 (제목, 날짜 범위)
- [ ] 주간 통계 카드 UI 구현
- [ ] TOP 10 게시글 카드 레이아웃 디자인
- [ ] 순위 아이콘 추가 (🥇🥈🥉 + 4-10위)
- [ ] 에디터 코멘트 섹션 스타일링
- [ ] 베스트 댓글 3개 표시 UI
- [ ] 반응 통계 (좋아요, 댓글 수) 표시
- [ ] 원본 게시글 링크 추가
- [ ] 모바일 반응형 디자인 확인

**SEO 최적화:**

- [ ] `<title>` 태그 추가
- [ ] `<meta name="description">` 추가
- [ ] Open Graph 메타 태그 추가 (og:title, og:description, og:type, og:image)
- [ ] Twitter Card 메타 태그 추가
- [ ] Canonical URL 추가
- [ ] JSON-LD 구조화 데이터 추가 (Article 타입)

### 3️⃣ 베스트 댓글 페이지 `/best-comments`

**백엔드 (Server):**

- [ ] `webapp/src/routes/best-comments/+page.server.ts` 생성
- [ ] 좋아요 많은 댓글 TOP 100 조회 쿼리 작성
- [ ] 사용자 정보 JOIN
- [ ] 원본 게시글 정보 JOIN
- [ ] 댓글 좋아요 수 집계
- [ ] 페이지네이션 로직 추가 (선택)
- [ ] 기간 필터 로직 추가 (선택)

**프론트엔드 (UI):**

- [ ] `webapp/src/routes/best-comments/+page.svelte` 생성
- [ ] 페이지 헤더 구현
- [ ] 댓글 카드 컴포넌트 디자인
- [ ] 댓글 내용 표시
- [ ] 작성자 정보 표시 (닉네임, 아바타)
- [ ] 원본 게시글 링크 버튼
- [ ] 좋아요 수 표시
- [ ] 작성 시간 표시 (상대 시간)
- [ ] 빈 상태 UI (댓글 없을 때)
- [ ] 페이지네이션 UI (선택)

**SEO 최적화:**

- [ ] `<title>` 태그 추가
- [ ] `<meta name="description">` 추가
- [ ] Open Graph 메타 태그 추가
- [ ] Twitter Card 메타 태그 추가
- [ ] Canonical URL 추가

### 4️⃣ 네비게이션 및 링크 추가

**Footer 업데이트:**

- [ ] `webapp/src/lib/components/Footer.svelte` 수정
- [ ] "주간 하이라이트" 링크 추가 (`/highlights/weekly`)
- [ ] "베스트 댓글" 링크 추가 (`/best-comments`)
- [ ] 링크 카테고리 정리 (커뮤니티 섹션?)

**Sitemap 업데이트:**

- [ ] `webapp/src/routes/sitemap.xml/+server.ts` 수정
- [ ] `/highlights/weekly` URL 추가 (priority: 0.8)
- [ ] `/best-comments` URL 추가 (priority: 0.7)

**메인 페이지 링크 (선택):**

- [ ] 홈페이지에 "주간 하이라이트" 배너 추가
- [ ] 사이드바에 "베스트 댓글" 위젯 추가

### 5️⃣ 테스트

**기능 테스트:**

- [ ] 로컬 개발 서버에서 `/highlights/weekly` 접속 확인
- [ ] TOP 10 게시글 정상 표시 확인
- [ ] 베스트 댓글 3개 정상 표시 확인
- [ ] 에디터 코멘트 표시 확인
- [ ] 통계 데이터 정확성 확인
- [ ] `/best-comments` 페이지 접속 확인
- [ ] 댓글 목록 정상 표시 확인
- [ ] 원본 게시글 링크 작동 확인

**UI/UX 테스트:**

- [ ] 데스크톱 화면에서 레이아웃 확인
- [ ] 태블릿 화면에서 레이아웃 확인
- [ ] 모바일 화면에서 레이아웃 확인
- [ ] 다크 모드에서 정상 표시 확인
- [ ] 로딩 상태 처리 확인
- [ ] 에러 상태 처리 확인

**SEO 테스트:**

- [ ] 브라우저 개발자 도구에서 메타 태그 확인
- [ ] Open Graph 디버거로 미리보기 확인
- [ ] JSON-LD 유효성 검사 (Google Rich Results Test)

**성능 테스트:**

- [ ] Lighthouse 점수 확인 (90+ 목표)
- [ ] 페이지 로딩 시간 확인 (3초 이내)
- [ ] 이미지 최적화 확인

### 6️⃣ 배포

**배포 전 체크:**

- [ ] 환경 변수 확인 (`PUBLIC_BASE_URL`)
- [ ] 빌드 테스트 (`npm run build`)
- [ ] 빌드 오류 없음 확인
- [ ] Git commit 및 push

**Railway 배포:**

- [ ] Railway 대시보드 접속
- [ ] 자동 배포 확인 (또는 수동 Deploy)
- [ ] 배포 로그 확인
- [ ] 배포 성공 확인

**배포 후 테스트:**

- [ ] 프로덕션 URL로 `/highlights/weekly` 접속
- [ ] 프로덕션 URL로 `/best-comments` 접속
- [ ] 모든 링크 작동 확인
- [ ] Google Analytics에서 페이지 조회 확인

---

## 📋 Phase 2: 추가 개선 (선택)

### 7️⃣ 아카이브 기능

- [ ] `/highlights/weekly/[weekId]` 동적 라우트 생성
- [ ] 과거 주차 데이터 조회 로직
- [ ] 아카이브 목록 페이지
- [ ] 주차 간 네비게이션 (이전/다음 주)

### 8️⃣ Admin 페이지 - 에디터 코멘트 관리

- [ ] `/admin/highlights` 페이지 생성
- [ ] 이번 주 TOP 10 게시글 목록 표시
- [ ] 각 게시글마다 코멘트 입력 폼
- [ ] 코멘트 저장 API
- [ ] 코멘트 수정/삭제 기능
- [ ] 저장 완료 토스트 메시지

### 9️⃣ 트렌드 리포트

- [ ] 키워드 추출 로직 구현
- [ ] `/trends` 페이지 생성
- [ ] 워드 클라우드 UI
- [ ] 사이트별 활동 차트
- [ ] 시간대별 활동 그래프

---

## 📋 Phase 3: 고급 기능 (장기)

### 🔟 사용자 큐레이션 시스템

- [ ] `community_picks` 테이블 생성
- [ ] 투표 UI 구현
- [ ] 투표 이유 입력 폼
- [ ] 주간 투표 마감 크론잡
- [ ] 결과 발표 페이지

---

## 📊 완료 기준

### Phase 1 완료 체크

최소 요구사항:

- [x] 주간 하이라이트 페이지 정상 작동
- [x] 베스트 댓글 페이지 정상 작동
- [x] SEO 메타 태그 완성
- [x] 모바일 반응형 디자인
- [x] 프로덕션 배포 완료

### AdSense 신청 준비 완료 체크

최소 운영 기간:

- [ ] 4주간 주간 하이라이트 발행 (4개 누적)
- [ ] 에디터 코멘트 40개 이상
- [ ] Google Analytics 데이터 수집 (4주)
- [ ] 원본 콘텐츠 페이지 조회수 500+ (4주 합산)

---

## 🚀 시작하기

**1. 기획서 숙지**

```bash
# 상세 기획서 읽기
cat /home/yj437/coding/aagag_clone/docs/ORIGINAL_CONTENT_PLAN.md
```

**2. 빠른 시작 가이드 확인**

```bash
# 빠른 실행 가이드 읽기
cat /home/yj437/coding/aagag_clone/docs/ORIGINAL_CONTENT_QUICKSTART.md
```

**3. 개발 시작**

```bash
# 개발 서버 실행
cd webapp
npm run dev
```

---

**최종 업데이트**: 2026-01-12  
**예상 완료일**: Phase 1 → 2-3일 내
