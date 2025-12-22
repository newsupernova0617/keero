# 크롤러 설정 가이드

크롤러를 실행하기 전에 다음 3가지를 설정해야 합니다.

---

## 1️⃣ 환경 변수 설정 (.env 파일)

### 📝 파일 생성
```bash
cd crawler
copy .env.example .env
```

### ✏️ .env 파일 편집

`.env` 파일을 열어서 다음 값들을 설정하세요:

```env
# 데이터베이스 경로 (기본값 사용 가능)
DB_PATH=../data/posts.db

# Cloudflare R2 설정 (웹앱과 동일한 값 사용)
R2_ACCOUNT_ID=your_account_id
R2_ACCESS_KEY_ID=your_access_key
R2_SECRET_ACCESS_KEY=your_secret_key
R2_BUCKET_NAME=your_bucket_name
R2_PUBLIC_URL=https://pub-d633a7c3cd0cd71ea3144f17896d4e65.r2.dev

# 로깅 데이터베이스 (기본값 사용 가능)
LOG_DB_PATH=../data/crawler_logs.db
```

**💡 팁**: 웹앱의 `.env` 파일에서 R2 설정을 복사하세요!

---

## 2️⃣ 데이터 폴더 생성

크롤러가 데이터베이스를 저장할 폴더를 만듭니다.

```bash
cd ..
mkdir data
```

또는 이미 `data` 폴더가 있다면 건너뛰세요.

---

## 3️⃣ Windows 작업 스케줄러 설정

`SCHEDULER_GUIDE.md` 파일을 참고하여 Windows 작업 스케줄러에 8개 작업을 생성합니다.

### 빠른 시작

1. **작업 스케줄러 열기**
   ```
   시작 → "작업 스케줄러" 검색
   ```

2. **기본 작업 만들기** (8번 반복)
   - 이름: `Crawler - Ruliweb`
   - 트리거: 매일 00:00, 2시간마다 반복
   - 동작: `run_crawler.bat ruliweb`

3. **나머지 7개 사이트도 동일하게**
   - TodayHumor: 00:15
   - Ppomppu: 00:30
   - FMKorea: 00:45
   - MLBPark: 01:00
   - Clien: 01:15
   - Humoruniv: 01:30
   - Dogdrip: 01:45

자세한 내용은 `SCHEDULER_GUIDE.md` 참고!

---

## ✅ 설정 완료 확인

### 테스트 실행
```bash
cd crawler
python main.py --site ruliweb
```

성공하면:
```
Crawler started (site: ruliweb)
=== Crawling ruliweb ===
📄 Page 1/2
   Found 20 posts on page 1
   ✅ New: 재미있는 글... (3 images)
   ...
```

### 로그 확인
```bash
cd crawler/logs
dir
```

`crawler_ruliweb_20241222.log` 같은 파일이 생성되어야 합니다.

---

## 🔍 문제 해결

### Python을 찾을 수 없음
`run_crawler.bat` 파일을 열어서 Python 경로 수정:
```batch
set PYTHON=C:\Python311\python.exe
```

### R2 연결 실패
`.env` 파일의 R2 설정이 올바른지 확인하세요.

### 데이터베이스 오류
`data` 폴더가 있는지 확인하세요.

---

## 📊 모니터링

### 로그 파일 위치
```
crawler/logs/crawler_[사이트명]_[날짜].log
```

### 데이터베이스 확인
```bash
cd data
sqlite3 posts.db
sqlite> SELECT COUNT(*) FROM posts;
sqlite> .quit
```

---

## 🎯 다음 단계

1. ✅ .env 파일 설정
2. ✅ data 폴더 생성
3. ✅ 테스트 실행
4. ✅ Windows 작업 스케줄러 설정
5. 🚀 크롤러 자동 실행 시작!
