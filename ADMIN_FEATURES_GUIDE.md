# 🎛️ SvelteKit Admin 페이지 기능 설명

> `/admin` 경로의 모든 관리자 기능 종합 가이드

---

## 📊 Admin 대시보드 (`/admin`)

### 주요 기능

- **통계 카드** (3개)

  - 📄 전체 게시글 수
  - 💬 전체 댓글 수
  - 👥 전체 사용자 수

- **최근 활동**

  - 최근 게시글 5개 (사이트명, 날짜 표시)
  - 최근 댓글 5개 (작성자, 내용, 날짜)

- **빠른 액션** (5개 버튼)
  - 📄 게시글 관리
  - 💬 댓글 관리
  - 👥 사용자 관리
  - 💾 DB 관리
  - 📈 통계 보기

---

## 1️⃣ 게시글 관리 (`/admin/posts`)

### 기능

- **게시글 목록 조회**

  - 전체 게시글 리스트
  - 사이트별 필터링
  - 페이지네이션

- **게시글 상세 정보**

  - 제목, 내용, 작성일
  - 출처 사이트
  - 크롤링 시간

- **게시글 작업**
  - 개별 게시글 삭제
  - 게시글 상세 보기 링크

---

## 2️⃣ 댓글 관리 (`/admin/comments`)

### 기능

- **댓글 목록 조회**

  - 전체 댓글 리스트
  - 작성자, 내용, 날짜 표시
  - 연결된 게시글 정보

- **댓글 작업**
  - 개별 댓글 삭제
  - 부적절한 댓글 관리
  - 해당 게시글로 이동

---

## 3️⃣ 사용자 관리 (`/admin/users`)

### 기능

- **사용자 목록 조회**

  - 전체 사용자 리스트
  - 이메일, 표시 이름
  - 가입일, 최종 로그인

- **사용자 정보**

  - 사용자 프로필 확인
  - 활동 내역 (댓글, 좋아요 등)

- **사용자 작업**
  - 사용자 계정 관리
  - 권한 확인

---

## 4️⃣ 데이터베이스 관리 (`/admin/database`)

### 📊 통계 정보

- **테이블별 통계**

  - 전체 게시글 수
  - 크롤링된 사이트 수
  - 전체 댓글 수
  - 전체 사용자 수

- **사이트별 게시글 수**

  - 각 사이트별 게시글 통계
  - 내림차순 정렬

- **최근 게시글 20개**
  - 제목, 사이트명
  - 작성일, 크롤링 시간

### 🛠️ 데이터 관리 작업

#### 1. 개별 게시글 삭제

```typescript
Action: deletePost
- 특정 게시글 ID로 삭제
- 연관된 댓글, 이미지도 함께 삭제 (CASCADE)
```

#### 2. 개별 댓글 삭제

```typescript
Action: deleteComment
- 특정 댓글 ID로 삭제
```

#### 3. 오래된 게시글 정리

```typescript
Action: cleanOldPosts
- 30일 이상 된 게시글 자동 삭제
- 대량 정리 기능
```

---

## 5️⃣ 통계 (`/admin/stats`)

### 기능

- **전체 통계**

  - 게시글, 댓글, 사용자 수
  - 시간별 트렌드

- **사이트별 통계**

  - 각 사이트별 게시글 수
  - 크롤링 성공률

- **사용자 활동 통계**
  - 활성 사용자 수
  - 댓글 작성 통계

---

## 6️⃣ 신고 관리 (`/admin/reports`)

### 기능

- **신고 목록 조회**

  - 미처리 신고
  - 처리 완료 신고

- **신고 처리**
  - 신고 내용 확인
  - 승인/거부 처리
  - 해당 게시글/댓글 조치

---

## 🔐 권한 관리

### Admin 접근 제어

```typescript
requireAdmin(event);
```

- **인증 확인**: Supabase Auth
- **권한 확인**: Admin 역할 필요
- **미인증 시**: 로그인 페이지로 리다이렉트
- **권한 없음**: 403 Forbidden

---

## 📋 데이터베이스 스키마

### 주요 테이블

```sql
-- 게시글
posts (
  id, site_name, title, content, content_html,
  source_url, created_at, crawled_at, content_hash
)

-- 댓글
comments (
  id, post_id, user_id, content,
  created_at, parent_id
)

-- 사용자
users (
  id, email, display_name,
  created_at, last_login
)

-- 이미지
images (
  id, post_id, media_type, original_url, r2_url,
  width, height, file_size
)

-- 좋아요
likes (
  id, user_id, post_id, comment_id, created_at
)

-- 북마크
bookmarks (
  id, user_id, post_id, created_at
)

-- 신고
reports (
  id, user_id, post_id, comment_id,
  reason, status, created_at, resolved_at
)
```

---

## 🎯 주요 사용 시나리오

### 1. 일일 관리 루틴

```
1. /admin - 대시보드 확인
2. 최근 게시글/댓글 확인
3. 신고 처리 (/admin/reports)
4. 통계 확인 (/admin/stats)
```

### 2. 데이터 정리

```
1. /admin/database
2. 사이트별 게시글 수 확인
3. "오래된 게시글 정리" 실행
4. 통계 재확인
```

### 3. 사용자 관리

```
1. /admin/users
2. 사용자 목록 확인
3. 문제 사용자 확인
4. 필요 시 조치
```

### 4. 컨텐츠 관리

```
1. /admin/posts
2. 부적절한 게시글 확인
3. 개별 삭제 또는 신고 처리
4. /admin/comments - 댓글 관리
```

---

## 🔧 API 엔드포인트

### Crawler API (내부용)

```
POST /api/crawler/posts
- Crawler가 게시글 저장
- 인증: CRAWLER_API_KEY

POST /api/crawler/logs
- Crawler가 로그 전송
- 인증: CRAWLER_API_KEY
```

---

## 📊 통계 예시

### 대시보드 통계

```
전체 게시글: 1,234개
전체 댓글: 567개
전체 사용자: 89명
```

### 사이트별 게시글

```
fmkorea: 450개
ruliweb: 320개
todayhumor: 280개
humoruniv: 184개
dogdrip: 0개 (비활성)
ppomppu: 0개 (비활성)
```

---

## 🚨 주의사항

### 1. 게시글 삭제

```
⚠️ CASCADE 삭제
- 게시글 삭제 시 연관된 모든 데이터 삭제
  - 댓글
  - 이미지
  - 좋아요
  - 북마크
  - 신고
```

### 2. 오래된 게시글 정리

```
⚠️ 30일 기준
- created_at 기준 30일 이상 게시글 삭제
- 복구 불가능
- 실행 전 확인 필요
```

### 3. 권한 관리

```
⚠️ Admin 전용
- 모든 /admin/* 경로는 Admin 권한 필요
- 일반 사용자 접근 불가
```

---

## 🎨 UI 컴포넌트

### 사용된 주요 컴포넌트

- **Card**: 정보 카드
- **Badge**: 사이트명, 상태 표시
- **Button**: 액션 버튼
- **Table**: 데이터 테이블
- **Icons**: Lucide Icons
  - FileText (게시글)
  - MessageSquare (댓글)
  - Users (사용자)
  - Database (DB)
  - TrendingUp (통계)

---

## 🔗 페이지 네비게이션

```
/admin
├── /admin/posts        (게시글 관리)
├── /admin/comments     (댓글 관리)
├── /admin/users        (사용자 관리)
├── /admin/database     (DB 관리)
├── /admin/stats        (통계)
└── /admin/reports      (신고 관리)
```

---

## 📝 요약

### Admin 페이지의 핵심 기능

1. ✅ **대시보드**: 전체 통계 및 최근 활동 확인
2. ✅ **게시글 관리**: 크롤링된 게시글 조회/삭제
3. ✅ **댓글 관리**: 사용자 댓글 모니터링/삭제
4. ✅ **사용자 관리**: 회원 정보 확인
5. ✅ **DB 관리**: 데이터 정리 및 통계
6. ✅ **통계**: 상세 분석 데이터
7. ✅ **신고 관리**: 사용자 신고 처리

### 주요 작업

- 📊 모니터링: 실시간 통계 확인
- 🗑️ 데이터 정리: 오래된 게시글 삭제
- 🚨 컨텐츠 관리: 부적절한 게시글/댓글 삭제
- 👥 사용자 관리: 회원 활동 확인

---

**Admin 페이지는 시스템 전체를 관리하는 중앙 허브입니다!** 🎛️
