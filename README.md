# 🎭 AAGAG Clone

> 한국 커뮤니티 사이트의 유머 게시글을 수집하고 공유하는 플랫폼

[![Deploy Status](https://img.shields.io/badge/deploy-Railway-blue)](https://railway.app)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

---

## 📋 프로젝트 개요

AAGAG Clone은 루리웹, 펨코, 오유, 웃긴대학, 개드립, 뽐뿌 등 6개 한국 커뮤니티 사이트에서 유머 게시글을 자동으로 수집하여 한 곳에서 볼 수 있게 해주는 웹 애플리케이션입니다.

### ✨ 주요 기능

- 🕷️ **자동 크롤링**: 6개 사이트의 유머 게시글 실시간 수집
- 🖼️ **이미지 최적화**: WebP 변환 및 Cloudflare R2 저장
- 🎬 **동영상 지원**: MP4/WebM 자동 변환
- 🔍 **전문 검색**: 제목/내용 전체 검색 (FTS)
- 💬 **댓글 시스템**: 계층형 댓글 및 답글
- ❤️ **좋아요/북마크**: 게시글 및 댓글 좋아요
- 🚨 **신고 시스템**: 커뮤니티 관리 기능
- 🌙 **다크 모드**: 눈에 편한 UI
- 📱 **반응형 디자인**: 모바일/태블릿 지원

---

## 🏗️ 아키텍처

```
┌─────────────────┐
│   SvelteKit     │  ← 웹 애플리케이션
│   (Webapp)      │  ← Supabase Auth
└────────┬────────┘
         │
    ┌────▼─────────────────┐
    │  SQLite Database     │  ← 게시글, 댓글, 사용자
    │  (data/posts.db)     │
    └────▲─────────────────┘
         │
┌────────┴────────┐
│   Crawler       │  ← Python 크롤러
│   (Scheduler)   │  ← 10분마다 실행
└────────┬────────┘
         │
    ┌────▼─────────────────┐
    │  Cloudflare R2       │  ← 이미지/동영상 저장
    └──────────────────────┘
```

---

## 📁 프로젝트 구조

```
aagag_clone/
├── 📁 crawler/              # Python 크롤러
│   ├── core/                # 핵심 모듈 (8개)
│   ├── utils/               # 유틸리티 (13개)
│   ├── tests/               # 테스트 (24개)
│   └── docs/                # 크롤러 문서
│
├── 📁 webapp/               # SvelteKit 웹앱
│   ├── src/routes/          # 페이지 라우트
│   ├── src/lib/             # 컴포넌트/유틸
│   └── src/lib/server/      # 서버 사이드
│
├── 📁 data/                 # 데이터베이스
│   ├── posts.db             # 게시글 DB
│   └── logs.db              # 로그 DB
│
├── 📁 docs/                 # 프로젝트 문서
│   ├── guides/              # 가이드
│   ├── testing/             # 테스트 문서
│   ├── issues/              # 이슈 분석
│   └── planning/            # 계획 문서
│
└── 📁 scripts/              # 유틸리티 스크립트
    ├── test_api.py          # API 테스트
    └── check_*.py           # 진단 도구
```

---

## 🚀 빠른 시작

### 1️⃣ 사전 요구사항

- **Node.js** 18+ (SvelteKit)
- **Python** 3.10+ (Crawler)
- **Supabase** 계정 (인증)
- **Cloudflare R2** 계정 (이미지 저장)

### 2️⃣ 설치

```bash
# 저장소 클론
git clone https://github.com/newsupernova0617/aagag_clone.git
cd aagag_clone

# Webapp 설치
cd webapp
npm install

# Crawler 설치
cd ../crawler
pip install -r requirements.txt
```

### 3️⃣ 환경 변수 설정

**Webapp (/.env)**

```bash
PUBLIC_SUPABASE_URL=your-supabase-url
PUBLIC_SUPABASE_ANON_KEY=your-anon-key
DATABASE_URL=file:../data/posts.db
CRAWLER_API_KEY=your-api-key
```

**Crawler (/crawler/.env.local)**

```bash
# R2 설정
R2_ACCOUNT_ID=your-account-id
R2_ACCESS_KEY_ID=your-access-key
R2_SECRET_ACCESS_KEY=your-secret-key
R2_BUCKET_NAME=your-bucket-name
R2_PUBLIC_URL=your-r2-public-url

# API 모드 (선택)
USE_API=false
API_URL=http://localhost:5173
CRAWLER_API_KEY=your-api-key
```

### 4️⃣ 실행

```bash
# Webapp 실행
cd webapp
npm run dev

# Crawler 실행 (별도 터미널)
cd crawler
python3 run.py
```

---

## 📖 문서

### 가이드

- [API 모드 가이드](docs/guides/API_MODE_GUIDE.md)
- [Railway 배포 가이드](docs/guides/RAILWAY_API_DEPLOY.md)

### 개발

- [테스트 계획](docs/testing/TEST_PLAN.md)
- [Webapp 계획](docs/planning/webapp_plan.md)

### 전체 문서

모든 문서는 [`docs/`](docs/) 폴더에 있습니다.

---

## 🧪 테스트

### Webapp 테스트

```bash
cd webapp
npm run test
```

### Crawler 테스트

```bash
cd crawler
pytest tests/unit/
```

### API 테스트

```bash
# SvelteKit 서버 실행 후
python3 scripts/test_api.py
```

---

## 🚂 배포

### Railway 배포

1. **Webapp 배포**

   - 저장소 연결
   - 환경변수 설정
   - `/data` 볼륨 마운트

2. **Crawler 배포**
   - 저장소 연결
   - 환경변수 설정
   - `run_scheduler.py` 실행

자세한 내용은 [Railway 배포 가이드](docs/guides/RAILWAY_API_DEPLOY.md)를 참조하세요.

---

## 🛠️ 기술 스택

### Frontend

- **SvelteKit** - 웹 프레임워크
- **TypeScript** - 타입 안정성
- **TailwindCSS** - 스타일링
- **Supabase Auth** - 사용자 인증

### Backend

- **Python 3.10** - 크롤러
- **SQLite** - 데이터베이스
- **SQLAlchemy** - ORM
- **BeautifulSoup4** - HTML 파싱
- **Playwright** - 동적 페이지 크롤링

### Infrastructure

- **Railway** - 배포 플랫폼
- **Cloudflare R2** - 객체 스토리지
- **APScheduler** - 크롤링 스케줄러

---

## 📊 데이터베이스 스키마

### Posts (게시글)

```sql
CREATE TABLE posts (
    id INTEGER PRIMARY KEY,
    site_name TEXT NOT NULL,
    title TEXT NOT NULL,
    content TEXT,
    content_html TEXT,
    source_url TEXT UNIQUE,
    created_at DATETIME,
    crawled_at DATETIME,
    content_hash TEXT UNIQUE
);
```

### Images (이미지/동영상)

```sql
CREATE TABLE images (
    id INTEGER PRIMARY KEY,
    post_id INTEGER,
    media_type TEXT,
    original_url TEXT,
    r2_url TEXT,
    optimized_format TEXT,
    width INTEGER,
    height INTEGER,
    file_size INTEGER
);
```

전체 스키마는 [`webapp/src/lib/server/schema.ts`](webapp/src/lib/server/schema.ts)를 참조하세요.

---

## 🤝 기여

기여는 언제나 환영합니다!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 있습니다.

---

## 🙏 감사합니다

- [Ruliweb](https://bbs.ruliweb.com), [FMKorea](https://www.fmkorea.com), [Todayhumor](https://www.todayhumor.co.kr)
- [Humoruniv](https://www.humoruniv.com), [Dogdrip](https://www.dogdrip.net), [Ppomppu](https://www.ppomppu.co.kr)
- 모든 오픈소스 기여자들

---

**Made with ❤️ by [newsupernova0617](https://github.com/newsupernova0617)**
