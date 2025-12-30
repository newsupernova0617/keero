# 🧪 Crawler 테스트 가이드

> 재구조화 후 크롤러 테스트 방법

---

## 🚀 빠른 테스트

### 1️⃣ 래퍼 스크립트 사용 (권장)

```bash
cd /home/yj437/coding/aagag_clone/crawler

# 전체 크롤링 (모든 사이트)
python3 run.py

# 특정 사이트만
python3 run.py --site fmkorea

# 3개 게시글만 테스트
python3 run.py --limit 3

# 특정 사이트 + 제한
python3 run.py --site ruliweb --limit 5
```

### 2️⃣ 모듈로 직접 실행

```bash
cd /home/yj437/coding/aagag_clone/crawler

# Python 모듈로 실행
python3 -m core.main

# 옵션 포함
python3 -m core.main --site fmkorea --limit 3
```

---

## 🧪 단위 테스트 (pytest)

### 전체 테스트 실행

```bash
cd /home/yj437/coding/aagag_clone/crawler

# 모든 테스트 실행
pytest tests/unit/

# 상세 출력
pytest tests/unit/ -v

# 특정 테스트만
pytest tests/unit/test_scraper.py

# 커버리지 포함
pytest tests/unit/ --cov=core --cov-report=html
```

### 개별 테스트

```bash
# Scraper 테스트
pytest tests/unit/test_scraper.py -v

# Storage 테스트
pytest tests/unit/test_storage.py -v

# HTML 처리 테스트
pytest tests/unit/test_html_processing.py -v
```

---

## 🔍 사이트별 빠른 테스트

### 루리웹

```bash
python3 run.py --site ruliweb --limit 3
```

### 펨코

```bash
python3 run.py --site fmkorea --limit 3
```

### 오유

```bash
python3 run.py --site todayhumor --limit 3
```

### 웃긴대학

```bash
python3 run.py --site humoruniv --limit 3
```

### 개드립

```bash
python3 run.py --site dogdrip --limit 3
```

### 뽐뿌

```bash
python3 run.py --site ppomppu --limit 3
```

---

## 🛠️ 유틸리티 스크립트 테스트

### 선택자 테스트

```bash
cd /home/yj437/coding/aagag_clone/crawler

# 모든 사이트 선택자 검증
python3 -m pytest tests/unit/test_selectors.py -v
```

### 단일 게시글 테스트

```bash
# 특정 URL 테스트
python3 tests/unit/test_single.py
```

### 미디어 처리 테스트

```bash
# 이미지/동영상 처리
python3 tests/unit/test_media.py
```

---

## 🌐 API 모드 테스트

### 1. SvelteKit 서버 시작

```bash
cd /home/yj437/coding/aagag_clone/webapp
npm run dev
```

### 2. API 테스트 스크립트

```bash
cd /home/yj437/coding/aagag_clone
python3 scripts/test_api.py
```

### 3. API 모드로 크롤러 실행

```bash
cd /home/yj437/coding/aagag_clone/crawler

# .env.local 설정
# USE_API=true
# API_URL=http://localhost:5173
# CRAWLER_API_KEY=your-key

python3 run.py --site fmkorea --limit 3
```

---

## 📊 데이터베이스 확인

### posts.db 확인

```bash
cd /home/yj437/coding/aagag_clone

# 게시글 개수
python3 scripts/check_databases.py

# content_html 확인
python3 scripts/check_content_html.py

# 스키마 확인
python3 scripts/check_db_schema.py
```

### 중복 제목 확인

```bash
cd /home/yj437/coding/aagag_clone/crawler
python3 utils/check_duplicate_titles.py
```

---

## 🔧 디버깅 모드

### 상세 로그 출력

```bash
cd /home/yj437/coding/aagag_clone/crawler

# Python 로깅 레벨 조정 (core/config.py)
# LOGGING = {
#     "level": "DEBUG",  # INFO → DEBUG
# }

python3 run.py --site fmkorea --limit 1
```

### 특정 게시글 재크롤링

```bash
cd /home/yj437/coding/aagag_clone/crawler

# 게시글 ID로 재크롤링
python3 utils/recrawl_post.py 123
```

---

## ⚡ 스케줄러 테스트

### 로컬에서 스케줄러 실행

```bash
cd /home/yj437/coding/aagag_clone/crawler

# 스케줄러 시작 (Ctrl+C로 종료)
python3 run_scheduler.py
```

### 스케줄러 동작 확인

- 즉시 실행: 그룹 1 (루리웹, 오유, 뽐뿌)
- 5분 후: 그룹 2 (펨코, 웃대, 개드립)
- 이후 10분마다 반복

---

## 🐛 문제 해결

### Import 에러

```bash
# 현재 디렉토리 확인
pwd  # /home/yj437/coding/aagag_clone/crawler 이어야 함

# Python 경로 확인
python3 -c "import sys; print(sys.path)"

# Import 테스트
python3 -c "from core.config import Config; print('✅ OK')"
```

### 의존성 에러

```bash
cd /home/yj437/coding/aagag_clone/crawler

# 의존성 설치 (가상환경 권장)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### DB 권한 에러

```bash
# DB 파일 권한 확인
ls -lh ../data/posts.db

# 권한 수정 (필요시)
chmod 664 ../data/posts.db
```

---

## 📝 테스트 체크리스트

### 기본 테스트

- [ ] `python3 run.py --limit 3` 실행
- [ ] 게시글 3개 크롤링 확인
- [ ] 로그 출력 확인
- [ ] DB에 저장 확인

### 사이트별 테스트

- [ ] 루리웹 크롤링
- [ ] 펨코 크롤링
- [ ] 오유 크롤링
- [ ] 웃대 크롤링
- [ ] 개드립 크롤링
- [ ] 뽐뿌 크롤링

### 기능 테스트

- [ ] 이미지 R2 업로드
- [ ] 중복 게시글 스킵
- [ ] Early Stop 동작
- [ ] Batch Commit 동작

### API 모드 테스트

- [ ] API 연결 확인
- [ ] 게시글 저장 확인
- [ ] 로그 전송 확인

---

## 🎯 권장 테스트 순서

1. **기본 동작 확인**

   ```bash
   python3 run.py --site fmkorea --limit 3
   ```

2. **DB 확인**

   ```bash
   python3 ../scripts/check_databases.py
   ```

3. **단위 테스트**

   ```bash
   pytest tests/unit/test_scraper.py -v
   ```

4. **전체 테스트**

   ```bash
   pytest tests/unit/ -v
   ```

5. **API 모드 테스트** (선택)
   ```bash
   python3 ../scripts/test_api.py
   ```

---

**Happy Testing! 🚀**
