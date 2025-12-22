# 프로젝트 전체 작업 목록

---

## 🤖 Part 1: Crawler 작업

### 🔴 긴급 (즉시 해결 필요)

- [x] **의존성 설치 확인**
  - ✅ venv 패키지 설치 완료
  - ✅ BeautifulSoup4, requests, lxml 등 모두 설치됨
  - ✅ pytest 7.4.3 설치 확인

- [x] **실제 커뮤니티 URL 및 CSS Selector 설정**
  - ✅ FMKorea 추가 및 활성화
  - ✅ HTML 구조 분석 완료 (브라우저 DevTools)
  - ✅ CSS 선택자 매핑 완료 (모든 필수 선택자)
  - ✅ robots.txt 확인 (/best 크롤링 허용)

- [x] **실제 크롤링 테스트 실행**
  - ✅ FMKorea 25개 게시글 크롤링 성공
  - ✅ 데이터 추출 검증 (제목, 날짜, 사이트명 정상)
  - ✅ R2 업로드 테스트 성공 (Mock 이미지)
  - ✅ `posts.db` 데이터 확인 완료
  - ⚠️ Rate Limiting 발생 (HTTP 430)

### 🟡 중요 (설정 및 구성)

- [x] **환경 변수 설정**
  - `.env` 파일 존재 확인됨
  - R2 credentials 설정 완료
  - 데이터베이스 경로 확인

- [x] **데이터베이스 초기화**
  - ✅ `posts.db` 생성 완료
  - ✅ 테이블 스키마 확인 (posts, images 등)

### 🟢 개선 사항 (코드 품질)

- [ ] **테스트 커버리지 개선**
  - scraper.py: 26% → 80%
  - storage.py: 62% → 80%
  - main.py: 12% → 70%

- [ ] **Ruff 린트 이슈 해결**

### 🚀 신규 기능: 미디어 최적화 및 GIF/동영상 지원

- [ ] **이미지 최적화 (R2 비용 절감)**
  - JPG/PNG → WebP 변환 (용량 30-50% 절감)
  - 해상도 제한 (최대 1920px)
  - Pillow 라이브러리 활용

- [ ] **GIF 최적화**
  - GIF → WebP 애니메이션 변환 (용량 50-70% 절감)
  - 또는 GIF → MP4 변환 (용량 80-90% 절감)
  - 프레임 수 제한 옵션 (너무 긴 GIF 제외)

- [ ] **동영상 최적화**
  - `ffmpeg` 연동 (Python: `ffmpeg-python`)
  - 해상도 제한 (최대 720p)
  - 비트레이트 조절, 길이 제한 (최대 60초)
  - 코덱: H.264 (호환성) 또는 VP9/AV1 (용량)

- [ ] **미디어 타입 확장**
  - 현재: 이미지 (jpg, png, webp)만 지원
  - 추가: GIF, 동영상 (mp4, webm) 지원
  - `scraper.py`에 미디어 타입 감지 로직 추가

- [ ] **R2 스토리지 전략**
  - ⚡ **최적화된 버전만 R2에 저장** (비용 절감)
  - 원본 용량은 메타데이터로만 기록 (`original_size_bytes`)
  - 미디어 타입별 R2 폴더 분리 (`images/`, `gifs/`, `videos/`)

- [x] **데이터베이스 스키마 확장** ✅ 완료
  - `storage.py`의 Image 모델에 추가 컬럼 반영됨
  - `media_type`, `duration_seconds`, `frame_count`
  - `original_size_bytes`, `optimized_size_bytes`
  - `original_format`, `optimized_format`

- [ ] **의존성 추가**
  ```
  # requirements.txt 추가
  ffmpeg-python==0.2.0
  imageio==2.31.1
  imageio-ffmpeg==0.4.8
  ```

---

## 🌐 Part 2: SvelteKit 웹앱 구현

### 🔴 Phase 1: 프로젝트 초기화

- [x] **SvelteKit 프로젝트 생성**
  - ✅ `npx sv create webapp` 실행 완료
  - ✅ TypeScript 설정 완료

- [x] **UI 프레임워크 설정**
  - ✅ Tailwind CSS 4.1.17 설치 완료
  - ✅ shadcn-svelte 설치 완료 (components.json 확인)
  - ✅ 기본 테마 구성 (Slate)
  - ✅ 개발 서버 정상 실행 (localhost:5173)

- [ ] **Supabase 연동**
  - Supabase 프로젝트 생성
  - 환경 변수 설정 (SUPABASE_URL, SUPABASE_ANON_KEY)
  - `@supabase/supabase-js` 설치
  - `@supabase/auth-helpers-sveltekit` 설치

### 🟡 Phase 2: 인증 시스템

- [ ] **OAuth 설정 (Supabase Auth)**
  - 카카오 OAuth 설정
  - 구글 OAuth 설정
  - ~~페이스북 OAuth~~ (제외)
  - ~~애플 OAuth~~ (제외)

- [ ] **인증 페이지 구현**
  - 로그인 페이지 (`/auth/login`)
  - OAuth 콜백 처리 (`/auth/callback`)
  - 로그아웃 처리 (`/auth/logout`)
  - 세션 관리 (layout.server.ts)

- [ ] **권한 시스템 구현**
  - Guest (레벨 0): 읽기만
  - User (레벨 1): 댓글 작성
  - Admin (레벨 99): 전체 권한
  - 권한 체크 미들웨어

### 🟡 Phase 3: 핵심 페이지 구현

- [ ] **게시글 목록 페이지** (`/`)
  - PostCard 컴포넌트
  - 페이지네이션
  - 검색 기능 (FTS)

- [ ] **게시글 상세 페이지** (`/post/[id]`)
  - 본문 표시
  - 이미지 갤러리
  - 좋아요 기능
  - 댓글 섹션

### 🟡 Phase 4: 댓글 시스템

- [ ] **댓글 기본 기능**
  - 댓글 목록 표시
  - 댓글 작성 (로그인 필요)
  - 댓글 수정/삭제 (본인만)

- [ ] **댓글 확장 기능**
  - 대댓글 (Reply) 기능
  - 댓글 좋아요 기능

### 🟡 Phase 5: 좋아요 & 검색

- [ ] **게시글 좋아요**
  - 좋아요 버튼 UI
  - 좋아요 수 표시
  - 중복 방지 (user_id + post_id unique)

- [ ] **검색 기능**
  - 검색바 UI
  - SQLite FTS5 활용
  - 검색 결과 페이지

### 🔴 Phase 6: 관리자 기능

- [ ] **관리자 레이아웃**
  - `/admin` 권한 체크
  - 관리자 사이드바/네비게이션

- [ ] **게시글 관리** (`/admin/posts`)
  - 게시글 목록 (전체)
  - 게시글 삭제/숨김 처리

- [ ] **댓글 관리** (`/admin/comments`)
  - 댓글 목록 (전체)
  - 댓글 삭제

- [ ] **사용자 관리** (`/admin/users`)
  - 사용자 목록
  - 사용자 차단

- [ ] **크롤링 관리** (`/admin/crawler`)
  - 크롤링 상태 확인
  - 수동 크롤링 실행
  - 설정 변경

- [ ] **신고 관리** (`/admin/reports`)
  - 신고 내역 확인
  - 신고 처리

- [ ] **통계 대시보드** (`/admin`)
  - 방문자 통계
  - 인기 게시글
  - 크롤링 통계

---

## 🚀 Part 3: 배포 (Railway)

### 서비스 구성

```
Railway Project
├── webapp (SvelteKit)  ──┐
│   └── Node.js           ├── 공유 볼륨: /data/app.db
└── crawler (Python)   ───┘
    └── Railway Cron: 2시간마다
```

### webapp (SvelteKit)

- [ ] **Railway 서비스 생성**
  - GitHub 저장소 연동
  - Root Directory: `/` (또는 `src/` 위치에 따라)
  - Build Command: `npm run build`
  - Start Command: `node build`

- [ ] **환경 변수 설정**
  ```
  SUPABASE_URL=
  SUPABASE_ANON_KEY=
  DATABASE_PATH=/data/app.db
  ```

- [ ] **도메인 연결**
  - Railway 제공 도메인 또는 커스텀 도메인

### crawler (Python)

- [ ] **Railway 서비스 생성**
  - GitHub 저장소 연동
  - Root Directory: `/crawler`
  - Build Command: `pip install -r requirements.txt`
  - Start Command: `python main.py`

- [ ] **Railway Cron 스케줄 설정**
  ```json
  {
    "schedule": "0 */2 * * *"
  }
  ```
  (2시간마다 실행)

- [ ] **환경 변수 설정**
  ```
  R2_ACCOUNT_ID=
  R2_ACCESS_KEY_ID=
  R2_SECRET_ACCESS_KEY=
  R2_BUCKET_NAME=
  DB_PATH=/data/app.db
  ```

### 공유 볼륨 설정

- [ ] **Railway Volume 생성**
  - Volume Name: `data`
  - 두 서비스에 모두 마운트: `/data`

- [ ] **SQLite 파일 공유 확인**
  - webapp과 crawler가 같은 `/data/app.db` 접근

### R2 이미지 서빙 (Custom Domain)

- [ ] **Cloudflare R2 설정**
  - R2 버킷 → Settings → Custom Domains
  - 서브도메인 연결: `images.your-domain.com`
  - 자동 CDN 캐싱 적용

- [ ] **이미지 URL 형식**
  ```
  https://images.your-domain.com/images/{md5_hash}.webp
  ```

---

## 📊 진행 상황 요약

| 영역 | 상태 | 비고 |
|------|------|------|
| Crawler 코어 | ✅ 완료 | 코드 구현됨 |
| Crawler 설정 | 🔴 미완료 | 실제 사이트 설정 필요 |
| SvelteKit 초기화 | 🔴 미시작 | |
| UI 프레임워크 | 🔴 미시작 | Tailwind + shadcn-svelte |
| 인증 시스템 | 🔴 미시작 | Supabase Auth |
| 게시글 페이지 | 🔴 미시작 | |
| 댓글 시스템 | 🔴 미시작 | 대댓글, 좋아요 포함 |
| 관리자 기능 | 🔴 미시작 | |
| Railway 배포 | 🔴 미시작 | |

---

## 🔧 Part 4: 운영 및 모니터링

### 에러 모니터링 (Sentry)

- [ ] **Sentry 설정**
  - Sentry 계정 생성 (sentry.io)
  - SvelteKit 프로젝트 생성
  - `@sentry/sveltekit` 설치

- [ ] **통합 구현**
  ```typescript
  // src/hooks.client.ts
  import * as Sentry from '@sentry/sveltekit';

  Sentry.init({
    dsn: 'https://xxx@sentry.io/xxx',
    tracesSampleRate: 1.0,
  });

  export const handleError = Sentry.handleErrorWithSentry();
  ```

- [ ] **알림 설정**
  - 슬랙/이메일 알림 연동
  - 에러 그룹화 설정

### 분석 도구 (Cloudflare Web Analytics)

- [ ] **Cloudflare 설정**
  - Cloudflare 대시보드 → Web Analytics
  - 사이트 추가 (도메인 연결)
  - 스크립트 코드 발급

- [ ] **SvelteKit에 추가**
  ```svelte
  <!-- src/app.html -->
  <script defer src='https://static.cloudflareinsights.com/beacon.min.js' 
    data-cf-beacon='{"token": "your-token"}'></script>
  ```

- [ ] **추적 항목**
  - 페이지뷰, 방문자 수
  - 인기 게시글
  - 검색어 분석

### 백업 전략

#### 백업 구조
```
R2 Bucket
└── backups/
    ├── app_20231221_0300.db      # 일일 백업
    ├── app_20231222_0300.db
    ├── app_20231223_0300.db
    └── ... (7일간 보관)
```

#### 백업 스크립트

- [ ] **crawler/backup.py 생성**
  ```python
  import shutil
  import os
  from datetime import datetime, timedelta
  from storage import R2Uploader
  from config import Config

  def backup_database():
      """SQLite 데이터베이스를 R2에 백업"""
      db_path = Config.DB_PATH
      timestamp = datetime.now().strftime('%Y%m%d_%H%M')
      backup_name = f"app_{timestamp}.db"
      
      # 1. 로컬 복사 (WAL 체크포인트)
      import sqlite3
      conn = sqlite3.connect(db_path)
      conn.execute("PRAGMA wal_checkpoint(TRUNCATE)")
      conn.close()
      
      # 2. 백업 파일 생성
      backup_path = f"/tmp/{backup_name}"
      shutil.copy(db_path, backup_path)
      
      # 3. R2 업로드
      r2 = R2Uploader(...)
      with open(backup_path, 'rb') as f:
          r2.upload(f.read(), f"backups/{backup_name}")
      
      # 4. 오래된 백업 삭제 (7일 이상)
      cleanup_old_backups(r2)
      
      print(f"Backup completed: {backup_name}")

  def cleanup_old_backups(r2, retention_days=7):
      """7일 이상 된 백업 삭제"""
      # R2에서 backups/ 목록 조회
      # 날짜 파싱하여 오래된 것 삭제
      pass

  if __name__ == "__main__":
      backup_database()
  ```

- [ ] **Railway Cron 설정**
  - 별도 서비스 또는 기존 crawler에 통합
  - 스케줄: `0 3 * * *` (매일 새벽 3시)

- [ ] **복원 절차 문서화**
  1. R2에서 백업 파일 다운로드
  2. 현재 DB 교체
  3. 서비스 재시작

### 모바일 전략

#### 현재 계획: 웹 우선 (반응형)
- Tailwind CSS로 모바일 반응형 구현
- 페이지네이션 (무한스크롤 X)
- 이미지 lazy loading

#### 향후 확장 옵션

| 옵션 | 설명 | 복잡도 |
|------|------|:------:|
| **PWA** | 홈 화면 추가, 오프라인 캐시 | 🟡 중간 |
| **Capacitor.js** | 네이티브 앱 래핑 (앱스토어 배포) | 🟡 중간 |

- [ ] **PWA 구현 시 (향후)**
  ```typescript
  // vite.config.ts
  import { SvelteKitPWA } from '@vite-pwa/sveltekit';
  
  export default {
    plugins: [
      sveltekit(),
      SvelteKitPWA({
        strategies: 'generateSW',
        manifest: {
          name: 'AAGAG Clone',
          short_name: 'AAGAG',
          theme_color: '#ffffff',
        }
      })
    ]
  };
  ```

- [ ] **Capacitor.js 구현 시 (향후)**
  ```bash
  npx cap init
  npx cap add android
  npx cap add ios
  npm run build && npx cap sync
  ```

