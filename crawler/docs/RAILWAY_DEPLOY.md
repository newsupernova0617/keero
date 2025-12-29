# Railway 배포 가이드

## 📋 개요

Railway에서 크롤러를 백그라운드 서비스로 실행합니다.
- APScheduler로 15분 간격 자동 스케줄링
- 24/7 자동 실행
- 각 사이트는 2시간마다 크롤링

---

## 🚀 Railway 배포 방법

### 1️⃣ Railway 프로젝트 생성

1. [Railway](https://railway.app) 로그인
2. **New Project** 클릭
3. **Deploy from GitHub repo** 선택
4. 이 저장소 선택

---

### 2️⃣ 크롤러 서비스 추가

1. 프로젝트에서 **+ New** 클릭
2. **GitHub Repo** 선택
3. **Root Directory** 설정:
   ```
   /crawler
   ```
4. **Service Name**: `crawler` 또는 원하는 이름

---

### 3️⃣ 환경 변수 설정

Railway 대시보드에서 **Variables** 탭:

```env
# 데이터베이스 (Railway PostgreSQL 사용 권장)
DATABASE_URL=postgresql://...

# 또는 SQLite 사용 (비권장)
DB_PATH=/app/data/posts.db

# Cloudflare R2
R2_ACCOUNT_ID=your_account_id
R2_ACCESS_KEY_ID=your_access_key
R2_SECRET_ACCESS_KEY=your_secret_key
R2_BUCKET_NAME=your_bucket_name
R2_PUBLIC_URL=https://pub-xxx.r2.dev

# 로깅
LOG_DB_PATH=/app/data/crawler_logs.db
```

---

### 4️⃣ 빌드 설정

Railway는 자동으로 `railway.json`을 감지합니다.

**수동 설정이 필요한 경우:**

1. **Settings** → **Build**
2. Build Command:
   ```bash
   pip install -r requirements.txt && playwright install chromium
   ```
3. Start Command:
   ```bash
   python scheduler.py
   ```

---

### 5️⃣ 배포

1. **Deploy** 버튼 클릭
2. 로그 확인:
   ```
   🤖 Crawler Scheduler Starting...
   📅 Scheduled: ruliweb at minute=0, hours=0,2,4,6,8,10,12,14,16,18,20,22
   📅 Scheduled: todayhumor at minute=15, hours=0,2,4,6,8,10,12,14,16,18,20,22
   ...
   ✅ Scheduler is running...
   ```

---

## 📊 스케줄 확인

### 타임라인

| 시간 | 사이트 | 다음 실행 |
|------|--------|----------|
| 00:00 | Ruliweb | 02:00 |
| 00:15 | TodayHumor | 02:15 |
| 00:30 | Ppomppu | 02:30 |
| 00:45 | FMKorea | 02:45 |
| 01:00 | MLBPark | 03:00 |
| 01:15 | Clien | 03:15 |
| 01:30 | Humoruniv | 03:30 |
| 01:45 | Dogdrip | 03:45 |

**결과:**
- 15분마다 새 글
- 각 사이트는 2시간마다
- 24/7 자동 실행

---

## 🔍 모니터링

### Railway 로그 확인

1. Railway 대시보드 → **Deployments**
2. 최신 배포 클릭
3. **Logs** 탭에서 실시간 로그 확인

### 로그 예시
```
2024-12-22 00:00:00 - 🚀 Starting crawl job for: ruliweb
2024-12-22 00:00:05 - === Crawling ruliweb ===
2024-12-22 00:00:10 - ✅ New: 재미있는 글... (3 images)
2024-12-22 00:02:30 - ✅ Completed crawl job for: ruliweb
```

---

## ⚙️ 고급 설정

### PostgreSQL 사용 (권장)

SQLite 대신 Railway PostgreSQL 사용:

1. **+ New** → **Database** → **PostgreSQL**
2. 자동으로 `DATABASE_URL` 환경 변수 생성됨
3. `storage.py`에서 PostgreSQL 지원 추가 필요

### 리소스 제한

Railway 무료 플랜:
- 메모리: 512MB
- CPU: 공유
- 실행 시간: 월 500시간

**최적화:**
- Playwright는 메모리 많이 사용 (~300MB)
- 필요시 유료 플랜 고려

---

## 🐛 문제 해결

### Playwright 설치 실패

빌드 커맨드에 시스템 의존성 추가:
```bash
apt-get update && apt-get install -y libnss3 libatk1.0-0 libatk-bridge2.0-0 && pip install -r requirements.txt && playwright install chromium
```

### 메모리 부족

1. Playwright 사이트 수 줄이기
2. 또는 Railway Pro 플랜 사용

### 타임존 문제

스케줄러는 `Asia/Seoul` 타임존 사용.
Railway 서버는 UTC이지만 스케줄러가 자동 변환함.

---

## 📝 로컬 테스트

배포 전 로컬에서 테스트:

```bash
cd crawler
python scheduler.py
```

Ctrl+C로 중지.

---

## 🎯 체크리스트

배포 전 확인:

- [ ] `.env` 파일 설정 (로컬 테스트용)
- [ ] Railway 환경 변수 설정
- [ ] `requirements.txt` 확인
- [ ] `railway.json` 확인
- [ ] 로컬 테스트 성공
- [ ] Railway 배포
- [ ] 로그 확인
- [ ] 첫 크롤링 성공 확인

---

## 🚀 배포 완료!

성공하면:
- ✅ 15분마다 새 글 자동 수집
- ✅ 24/7 자동 실행
- ✅ Railway에서 자동 관리

문제가 있으면 Railway 로그를 확인하세요!
