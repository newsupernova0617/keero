# API 게이트웨이 모드 사용법

## 개요

Crawler가 SvelteKit API를 통해 데이터를 저장하는 방식입니다.  
Railway 배포 시 SQLite 볼륨 제약을 해결하기 위해 사용됩니다.

---

## 로컬 개발

### 1. SvelteKit 서버 시작

```bash
cd webapp
npm run dev
```

### 2. Crawler 환경변수 설정

```bash
# crawler/.env.local
USE_API=true
API_URL=http://localhost:5173
CRAWLER_API_KEY=c143f4a0f471232b4c7e13fafdcdc25fbd21c3b793cd95498cfb15ea1ef2e339
```

### 3. Crawler 실행

```bash
cd crawler
python3 main.py --site fmkorea --limit 3
```

---

## Railway 배포

자세한 내용은 [RAILWAY_API_DEPLOY.md](./RAILWAY_API_DEPLOY.md) 참조

### 간단 요약:

1. **Webapp 배포**

   - 환경변수: `CRAWLER_API_KEY` 설정
   - 볼륨 연결: `/data`

2. **Crawler 배포**
   - 환경변수: `USE_API=true`, `API_URL`, `CRAWLER_API_KEY`

---

## API 테스트

```bash
# SvelteKit 서버 실행 후
python3 test_api.py
```

---

## 모드 전환

### API 모드 → 로컬 DB 모드

```bash
# crawler/.env.local
USE_API=false
```

### 로컬 DB 모드 → API 모드

```bash
# crawler/.env.local
USE_API=true
API_URL=http://localhost:5173
CRAWLER_API_KEY=<your-api-key>
```

---

## 문제 해결

### Crawler가 API에 연결 안 됨

```bash
# 1. SvelteKit 서버 확인
curl http://localhost:5173

# 2. API 키 확인
echo $CRAWLER_API_KEY

# 3. API 테스트
python3 test_api.py
```

### 401 Unauthorized

- Webapp과 Crawler의 `CRAWLER_API_KEY`가 동일한지 확인

### 500 Internal Server Error

- SvelteKit 로그 확인
- DB 파일 권한 확인

---

**더 자세한 정보**: [RAILWAY_API_DEPLOY.md](./RAILWAY_API_DEPLOY.md)
