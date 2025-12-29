# Railway 배포 가이드

## 📦 프로젝트 구조

이 프로젝트는 **2개의 독립적인 서비스**로 구성됩니다:

1. **Crawler** (크롤러) - Python 기반 데이터 수집
2. **WebApp** (웹앱) - SvelteKit 기반 웹 애플리케이션

---

## 🚀 Railway 배포 단계

### 1️⃣ 공유 볼륨 생성

두 서비스가 같은 SQLite DB를 공유해야 하므로 **Volume**을 생성합니다.

```bash
# Railway CLI 사용
railway volume create data-volume
```

또는 Railway 대시보드에서:
- Project Settings → Volumes → New Volume
- Name: `data-volume`
- Mount Path: `/data`

---

### 2️⃣ Crawler 서비스 배포

#### Railway 대시보드에서:

1. **New Service** 클릭
2. **Deploy from GitHub repo** 선택
3. Repository 연결
4. **Settings** 탭에서:
   - **Root Directory**: `crawler`
   - **Dockerfile Path**: `crawler/Dockerfile`
   - **Service Name**: `crawler`

5. **Variables** 탭에서 환경 변수 설정:
   ```
   R2_ACCOUNT_ID=your-account-id
   R2_ACCESS_KEY_ID=your-access-key
   R2_SECRET_ACCESS_KEY=your-secret-key
   R2_BUCKET_NAME=aagag-images
   DB_PATH=/data/posts.db
   LOGS_DB_PATH=/data/logs.db
   ```

6. **Volumes** 탭에서:
   - `data-volume`을 `/data`에 마운트

7. **Settings** → **Cron Schedule** 설정:
   ```
   0 */2 * * *
   ```
   (2시간마다 실행)

---

### 3️⃣ WebApp 서비스 배포

#### Railway 대시보드에서:

1. **New Service** 클릭
2. 같은 Repository 선택
3. **Settings** 탭에서:
   - **Root Directory**: `webapp`
   - **Dockerfile Path**: `webapp/Dockerfile`
   - **Service Name**: `webapp`

4. **Variables** 탭에서 환경 변수 설정:
   ```
   DATABASE_URL=/data/posts.db
   PUBLIC_SUPABASE_URL=your-supabase-url
   PUBLIC_SUPABASE_ANON_KEY=your-supabase-key
   ORIGIN=https://your-domain.railway.app
   ```

5. **Volumes** 탭에서:
   - 같은 `data-volume`을 `/data`에 마운트

6. **Networking** 탭에서:
   - Public Domain 활성화

---

## 🔧 환경 변수 전체 목록

### Crawler 서비스
```env
# Cloudflare R2
R2_ACCOUNT_ID=
R2_ACCESS_KEY_ID=
R2_SECRET_ACCESS_KEY=
R2_BUCKET_NAME=aagag-images

# Database
DB_PATH=/data/posts.db
LOGS_DB_PATH=/data/logs.db
```

### WebApp 서비스
```env
# Database
DATABASE_URL=/data/posts.db

# Supabase
PUBLIC_SUPABASE_URL=
PUBLIC_SUPABASE_ANON_KEY=

# SvelteKit
ORIGIN=https://your-domain.railway.app
```

---

## 📊 볼륨 공유 확인

두 서비스가 같은 DB를 사용하는지 확인:

```bash
# Crawler 서비스 로그
railway logs --service crawler

# WebApp 서비스 로그
railway logs --service webapp
```

---

## 🔄 Cron 설정 (크롤러)

Railway에서 Cron Job 설정:

1. Crawler 서비스 → **Settings**
2. **Cron Schedule** 입력:
   - `0 */2 * * *` - 2시간마다
   - `0 0 * * *` - 매일 자정
   - `*/30 * * * *` - 30분마다

---

## 🐛 트러블슈팅

### 1. DB 파일이 공유되지 않음
- 두 서비스가 **같은 Volume**을 마운트했는지 확인
- Mount Path가 `/data`로 동일한지 확인

### 2. Crawler가 실행되지 않음
- Cron Schedule이 올바른지 확인
- 환경 변수가 모두 설정되었는지 확인
- Logs에서 에러 메시지 확인

### 3. WebApp이 DB를 찾지 못함
- `DATABASE_URL=/data/posts.db` 설정 확인
- Volume이 마운트되었는지 확인

---

## 📝 배포 체크리스트

- [ ] Railway 프로젝트 생성
- [ ] Volume 생성 (`data-volume`)
- [ ] Crawler 서비스 배포
  - [ ] Dockerfile 경로 설정
  - [ ] 환경 변수 설정
  - [ ] Volume 마운트
  - [ ] Cron 스케줄 설정
- [ ] WebApp 서비스 배포
  - [ ] Dockerfile 경로 설정
  - [ ] 환경 변수 설정
  - [ ] Volume 마운트 (같은 볼륨!)
  - [ ] Public Domain 활성화
- [ ] Supabase OAuth 콜백 URL 업데이트
  - `https://your-domain.railway.app/auth/callback`
- [ ] R2 CORS 설정 확인
- [ ] 배포 테스트
  - [ ] 크롤러 로그 확인
  - [ ] 웹앱 접속 확인
  - [ ] 게시글 표시 확인
  - [ ] 로그인 테스트

---

## 🎯 배포 후 확인사항

1. **크롤러 실행 확인**
   ```bash
   railway logs --service crawler
   ```

2. **웹앱 접속 확인**
   - https://your-domain.railway.app

3. **DB 공유 확인**
   - 크롤러가 저장한 게시글이 웹앱에 표시되는지 확인

4. **Supabase 로그인 테스트**
   - Google/Kakao 로그인 정상 작동 확인

---

## 📚 추가 리소스

- [Railway Docs](https://docs.railway.app/)
- [Railway Volumes](https://docs.railway.app/reference/volumes)
- [Railway Cron Jobs](https://docs.railway.app/reference/cron-jobs)
