# 🚀 Railway 배포 환경 로컬 재현 가이드

> Railway의 Volume 제약사항으로 인해 Crawler가 API를 통해 SQLite에 접근하는 환경을 로컬에서 테스트하는 방법

---

## 🏗️ Railway 배포 구조 (실제)

### ⚠️ Railway 제약사항

**Railway에서는 여러 서비스가 같은 Volume을 공유할 수 없습니다!**

따라서:

- ❌ Webapp과 Crawler가 같은 SQLite 파일에 직접 접근 불가
- ✅ SQLite는 **Webapp 서비스에만** 종속
- ✅ Crawler는 **API를 통해서만** 데이터 저장

### Production (Railway)

```
┌─────────────────────────────────────────────────┐
│              Webapp Service                     │
│  ┌──────────────────────────────────────────┐   │
│  │  Volume (/data)                          │   │
│  │  ├── posts.db                            │   │
│  │  └── logs.db                             │   │
│  └──────────────────────────────────────────┘   │
│         ↑                                        │
│         │ 읽기/쓰기                              │
│  ┌──────┴────────┐                              │
│  │  SvelteKit    │                              │
│  │  + SQLite     │ ← API 엔드포인트             │
│  └───────────────┘                              │
└──────────────────────────────┬──────────────────┘
                               │
                               │ HTTP API
                               │ POST /api/crawler/posts
                               │ POST /api/crawler/logs
                               ↓
┌─────────────────────────────────────────────────┐
│              Crawler Service                    │
│  ┌──────────────────────────────────────────┐   │
│  │  Python Crawler                          │   │
│  │  (SQLite 직접 접근 불가)                  │   │
│  │                                           │   │
│  │  데이터 저장 필요 시:                      │   │
│  │  → API 요청으로 처리                      │   │
│  └──────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘
```

**핵심**:

- ✅ SQLite는 **Webapp 서비스의 Volume**에만 존재
- ✅ Crawler는 **API 호출**로만 데이터 저장
- ✅ 이것이 Railway의 제약으로 인한 **유일한 방법**

---

## 💡 왜 API 모드를 만들었나?

### 문제

```
Railway Volume = 하나의 서비스에만 마운트 가능
→ Webapp과 Crawler가 같은 SQLite 파일 공유 불가
```

### 해결책 (API 모드)

```
1. SQLite를 Webapp 서비스에 종속
2. Crawler는 HTTP API로 데이터 전송
3. Webapp의 API 엔드포인트가 SQLite에 저장
```

### 구현

- **API 엔드포인트**: `/api/crawler/posts`, `/api/crawler/logs`
- **Crawler 클라이언트**: `api_client.py` (HTTP 요청)
- **Wrapper**: `api_storage.py` (DatabaseManager 인터페이스 호환)

---

## 💻 로컬 재현 방법

### 방법 1: API 모드 (Railway와 동일) ⭐

**이것이 실제 Railway 배포 환경입니다!**

#### 1️⃣ SvelteKit 서버 시작

```bash
cd /home/yj437/coding/aagag_clone/webapp
npm run dev
# → http://localhost:5173
```

#### 2️⃣ Crawler 설정 (.env.local)

```bash
# API 모드 활성화
USE_API=true
API_URL=http://localhost:5173
CRAWLER_API_KEY=c143f4a0f471232b4c7e13fafdcdc25fbd21c3b793cd95498cfb15ea1ef2e339

# R2는 비활성화 (Railway에서도 사용 안 함)
# R2_ACCOUNT_ID=
# R2_ACCESS_KEY_ID=
# R2_SECRET_ACCESS_KEY=
```

#### 3️⃣ Crawler 실행

```bash
cd /home/yj437/coding/aagag_clone/crawler
source venv/bin/activate
python3 run.py --limit 3
```

#### 4️⃣ 데이터 흐름

```
Crawler (Python)
   ↓ HTTP POST /api/crawler/posts
SvelteKit API Handler
   ↓ SQLite INSERT
/home/yj437/coding/aagag_clone/data/posts.db
   ↑ SQLite SELECT
SvelteKit 페이지 (+page.server.ts)
   ↓ 렌더링
브라우저
```

**이것이 Railway 배포와 100% 동일한 환경입니다!**

---

### 방법 2: 로컬 DB 모드 (개발 전용)

**Railway에서는 불가능하지만, 로컬 개발 시 편리합니다.**

#### 1️⃣ Crawler 설정 (.env.local)

```bash
# API 모드 비활성화
USE_API=false

# R2 활성화 (로컬 테스트용)
R2_ACCOUNT_ID=d633a7c3cd0cd71ea3144f17896d4e65
R2_ACCESS_KEY_ID=dd8b1691a5bbe265afac725f297b2f2d
R2_SECRET_ACCESS_KEY=c2659d3e2315ab4ebdd83bdcb0036602aaaed2c066b0d6c3a1b3d2fd8311d8cf
R2_BUCKET_NAME=keero
R2_PUBLIC_URL=https://pub-d633a7c3cd0cd71ea3144f17896d4e65.r2.dev
```

#### 2️⃣ Crawler 실행

```bash
cd /home/yj437/coding/aagag_clone/crawler
source venv/bin/activate
python3 run.py --limit 3
```

#### 3️⃣ 데이터 흐름

```
Crawler (Python)
   ↓ 직접 SQLite INSERT
/home/yj437/coding/aagag_clone/data/posts.db
   ↑ SQLite SELECT
SvelteKit (나중에 실행)
```

**장점**:

- ✅ SvelteKit 없이 크롤러만 빠르게 테스트
- ✅ R2 업로드 테스트 가능
- ✅ 빠른 개발/디버깅

**단점**:

- ⚠️ **Railway 배포와 다른 방식**
- ⚠️ Railway에서는 이 방식 불가능

---

## 🎯 권장 워크플로우

### 개발 단계별 사용

#### 1. 크롤러 로직 개발 (빠른 반복)

```bash
# 로컬 DB 모드 - 빠른 테스트
USE_API=false
python3 run.py --site fmkorea --limit 3
```

#### 2. API 통합 테스트 (배포 전 필수)

```bash
# Terminal 1: SvelteKit 서버
cd webapp && npm run dev

# Terminal 2: Crawler (API 모드)
cd crawler
# .env.local에서 USE_API=true
python3 run.py --limit 3
```

#### 3. Railway 배포

```bash
# Railway 환경변수 설정
USE_API=true
API_URL=https://your-webapp.railway.app
CRAWLER_API_KEY=your-secret-key

# 자동으로 API 모드로 실행됨
```

---

## 📊 환경 비교표

| 항목               | 로컬 DB 모드 | 로컬 API 모드 | Railway 배포    |
| ------------------ | ------------ | ------------- | --------------- |
| **SvelteKit 서버** | 선택         | 필수 ✅       | 자동 실행 ✅    |
| **Crawler → DB**   | 직접 쓰기    | API 경유 ✅   | API 경유 ✅     |
| **SQLite 위치**    | 공유 폴더    | 공유 폴더     | Webapp Volume만 |
| **R2 업로드**      | ✅ 가능      | ❌ 불가       | ❌ 불가         |
| **로그 전송**      | 로컬 DB      | API ✅        | API ✅          |
| **배포 유사도**    | ❌ 낮음      | ✅ **100%**   | -               |
| **개발 속도**      | ⚡ 빠름      | 보통          | -               |

---

## 🚨 중요 사항

### 1. Railway에서는 API 모드만 가능

```
Railway 제약: Volume은 하나의 서비스에만 마운트
→ Crawler가 SQLite에 직접 접근 불가
→ API 모드가 유일한 해결책
```

### 2. R2 업로드는 API 모드에서 미지원

```
현재 구현:
- 로컬 DB 모드: Crawler가 R2 업로드 ✅
- API 모드: R2 업로드 안 함 ❌

Railway 배포 시:
- 이미지는 원본 URL 그대로 저장
- R2 업로드 기능은 사용 안 함
```

**향후 개선 방안**:

- SvelteKit API에서 이미지 다운로드 + R2 업로드 처리
- 또는 별도 이미지 처리 서비스 구축

### 3. 로컬 테스트 시 주의

```
개발: 로컬 DB 모드 (빠름)
배포 전 테스트: API 모드 (필수)
Railway 배포: API 모드 (자동)
```

---

## 🔧 실전 설정 예시

### Railway 배포 환경 재현 (API 모드)

#### Step 1: SvelteKit 서버 시작

```bash
# Terminal 1
cd /home/yj437/coding/aagag_clone/webapp
npm run dev
```

#### Step 2: .env.local 수정

```bash
# /home/yj437/coding/aagag_clone/crawler/.env.local
USE_API=true
API_URL=http://localhost:5173
CRAWLER_API_KEY=c143f4a0f471232b4c7e13fafdcdc25fbd21c3b793cd95498cfb15ea1ef2e339
```

#### Step 3: Crawler 실행

```bash
# Terminal 2
cd /home/yj437/coding/aagag_clone/crawler
source venv/bin/activate
python3 run.py --limit 3
```

#### Step 4: 로그 확인

```
[2025-12-29 21:51:29] INFO: 🌐 API Mode enabled
[2025-12-29 21:51:29] INFO:    API URL: http://localhost:5173
[2025-12-29 21:51:29] INFO: 📝 API Log Handler added
```

#### Step 5: 브라우저 확인

```
http://localhost:5173
→ 크롤링된 게시글 확인
```

---

## 🎯 최종 정리

### Railway 배포의 핵심

```
1. SQLite는 Webapp 서비스에만 존재
2. Crawler는 API로만 데이터 저장
3. 이것이 Railway Volume 제약의 해결책
```

### 로컬 테스트 방법

```
1. 개발: 로컬 DB 모드 (빠름)
2. 배포 전: API 모드 (필수)
3. 배포: Railway 자동 처리
```

### API 모드가 필수인 이유

```
Railway Volume = 서비스별 독립
→ 공유 불가능
→ API가 유일한 해결책
```

---

**이제 Railway 배포 환경을 정확히 이해하셨나요?** 🚀
