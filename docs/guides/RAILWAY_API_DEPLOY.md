# Railway 배포 가이드 - API 게이트웨이 방식

## 📋 개요

Railway에서 SQLite 볼륨은 하나의 서비스에만 연결할 수 있습니다.  
따라서 Crawler와 Webapp이 API를 통해 통신하는 **API 게이트웨이 방식**을 사용합니다.

```
┌─────────────────────────────────────────┐
│  Railway                                │
│                                         │
│  ┌─────────────────┐                   │
│  │  Crawler        │                   │
│  │  (Python)       │                   │
│  │                 │  HTTP POST        │
│  │                 │──────────┐        │
│  └─────────────────┘          │        │
│                                ▼        │
│  ┌─────────────────────────────────┐   │
│  │  Webapp (SvelteKit)             │   │
│  │  ┌─────────────────────────┐    │   │
│  │  │ API Routes              │    │   │
│  │  │  /api/crawler/posts     │    │   │
│  │  │  /api/crawler/logs      │    │   │
│  │  └─────────────────────────┘    │   │
│  │  ┌─────────────────────────┐    │   │
│  │  │ SQLite (Volume)         │    │   │
│  │  │  - posts.db             │    │   │
│  │  │  - logs.db              │    │   │
│  │  └─────────────────────────┘    │   │
│  └─────────────────────────────────┘   │
└─────────────────────────────────────────┘
```

---

## 🚀 배포 단계

### 1️⃣ **Webapp 서비스 배포**

#### 환경변수 설정:

```bash
# Supabase
PUBLIC_SUPABASE_URL=https://wnamhqorcmkwjatbjlkq.supabase.co
PUBLIC_SUPABASE_ANON_KEY=sb_publishable_-iO_42Hfeig1Ceh69LbM7w_lwatqJKc

# R2
R2_PUBLIC_URL=https://pub-d633a7c3cd0cd71ea3144f17896d4e65.r2.dev

# Base URL (Railway 자동 생성 URL)
# SEO, Sitemap, Open Graph에 사용됨
PUBLIC_BASE_URL=https://your-webapp.up.railway.app

# Crawler API 인증 키 (강력한 랜덤 문자열)
CRAWLER_API_KEY=<강력한-랜덤-키-생성>
```

#### API 키 생성 방법:

```bash
# 로컬에서 실행
openssl rand -hex 32
# 출력 예: c143f4a0f471232b4c7e13fafdcdc25fbd21c3b793cd95498cfb15ea1ef2e339
```

#### 볼륨 연결:

- Railway 대시보드에서 **Volume** 생성
- Mount Path: `/data`
- Webapp 서비스에 연결

---

### 2️⃣ **Crawler 서비스 배포**

#### 환경변수 설정:

```bash
# API 모드 활성화
USE_API=true

# Webapp API URL (Railway에서 생성된 URL)
API_URL=https://your-webapp.up.railway.app

# API 인증 키 (Webapp과 동일한 키)
CRAWLER_API_KEY=<Webapp과-동일한-키>

# API 타임아웃 (초)
API_TIMEOUT=60

# Cloudflare R2 설정
R2_ACCOUNT_ID=d633a7c3cd0cd71ea3144f17896d4e65
R2_ACCESS_KEY_ID=dd8b1691a5bbe265afac725f297b2f2d
R2_SECRET_ACCESS_KEY=c2659d3e2315ab4ebdd83bdcb0036602aaaed2c066b0d6c3a1b3d2fd8311d8cf
R2_BUCKET_NAME=keero
R2_PUBLIC_URL=https://pub-d633a7c3cd0cd71ea3144f17896d4e65.r2.dev
```

---

## 🔧 로컬 개발

로컬에서는 **DB 직접 접근 방식**을 사용합니다.

### Webapp (.env)

```bash
USE_API=false  # 로컬에서는 불필요
CRAWLER_API_KEY=c143f4a0f471232b4c7e13fafdcdc25fbd21c3b793cd95498cfb15ea1ef2e339
```

### Crawler (.env.local)

```bash
USE_API=false
DB_PATH=../data/posts.db
LOG_DB_PATH=../data/logs.db
```

---

## 📊 API 엔드포인트

### 1. POST `/api/crawler/posts`

게시글 + 이미지 저장

**Request:**

```json
{
  "post": {
    "site_name": "fmkorea",
    "title": "게시글 제목",
    "content": "본문 텍스트",
    "content_html": "<div>HTML 본문</div>",
    "source_url": "https://example.com/post/123",
    "created_at": "2025-12-27T17:00:00"
  },
  "images": [
    { "url": "https://example.com/image1.jpg", "order_index": 0 },
    { "url": "https://example.com/image2.jpg", "order_index": 1 }
  ]
}
```

**Response:**

```json
{
  "success": true,
  "post_id": 123,
  "images_saved": 2
}
```

### 2. POST `/api/crawler/logs`

로그 배치 저장

**Request:**

```json
{
  "logs": [
    {
      "timestamp": "2025-12-27T17:00:00",
      "level": "INFO",
      "level_no": 20,
      "logger": "crawler.scraper",
      "message": "Crawling started",
      "function": "crawl_site",
      "line_number": 45,
      "exception": null,
      "extra_data": null
    }
  ]
}
```

**Response:**

```json
{
  "success": true,
  "logs_saved": 1
}
```

---

## 🔐 보안

### API 키 관리

- ✅ 강력한 랜덤 키 사용 (64자 hex)
- ✅ 환경변수로만 관리 (코드에 하드코딩 금지)
- ✅ Railway Secrets 사용
- ✅ 정기적으로 키 교체

### 네트워크

- ✅ HTTPS 통신 (Railway 자동 제공)
- ✅ API Key 헤더 검증
- ✅ Rate limiting (필요시 추가)

---

## 🧪 테스트

### API 테스트

```bash
# SvelteKit 서버 시작
cd webapp
npm run dev

# 다른 터미널에서 테스트
python3 test_api.py
```

### Crawler API 모드 테스트

```bash
# .env.local에서 USE_API=true 설정
cd crawler
python3 main.py --site fmkorea --limit 3
```

---

## 📈 모니터링

### Webapp 로그 확인

```bash
# Railway CLI
railway logs --service webapp
```

### Crawler 로그 확인

```bash
# Railway CLI
railway logs --service crawler

# 또는 Webapp의 logs.db 확인
sqlite3 /data/logs.db "SELECT * FROM logs ORDER BY timestamp DESC LIMIT 10"
```

---

## ⚠️ 주의사항

1. **Webapp 먼저 배포**: Crawler가 API URL을 필요로 함
2. **API 키 동기화**: Webapp과 Crawler의 `CRAWLER_API_KEY`가 동일해야 함
3. **볼륨 연결**: Webapp에만 볼륨 연결
4. **타임아웃 설정**: 큰 이미지가 많은 경우 `API_TIMEOUT` 증가

---

## 🔄 마이그레이션 (로컬 → Railway)

### 1. 로컬 DB 백업

```bash
cp data/posts.db data/posts.db.backup
cp data/logs.db data/logs.db.backup
```

### 2. Railway 볼륨에 업로드

```bash
# Railway CLI 사용
railway volume upload /data posts.db
railway volume upload /data logs.db
```

### 3. 환경변수 전환

- Crawler: `USE_API=false` → `USE_API=true`
- Webapp: `CRAWLER_API_KEY` 설정

---

## 📞 문제 해결

### Crawler가 API에 연결 안 됨

- ✅ `API_URL`이 올바른지 확인
- ✅ `CRAWLER_API_KEY`가 Webapp과 동일한지 확인
- ✅ Webapp이 실행 중인지 확인

### 401 Unauthorized 에러

- ✅ API 키가 정확히 일치하는지 확인
- ✅ 환경변수가 제대로 로드되었는지 확인

### 500 Internal Server Error

- ✅ Webapp 로그 확인: `railway logs --service webapp`
- ✅ DB 파일 권한 확인
- ✅ 볼륨이 올바르게 마운트되었는지 확인

---

## ✅ 체크리스트

배포 전 확인사항:

- [ ] Webapp 환경변수 설정 완료
- [ ] Crawler 환경변수 설정 완료
- [ ] API 키 생성 및 동기화
- [ ] 볼륨 생성 및 Webapp 연결
- [ ] 로컬에서 API 테스트 성공
- [ ] Railway에 Webapp 배포
- [ ] Railway에 Crawler 배포
- [ ] 배포 후 로그 확인

---

**작성일**: 2025-12-27  
**버전**: 1.0
