# main.py

## 개요

크롤러의 엔트리포인트이자 스케줄러 역할을 담당하는 메인 파일 (다중 사이트 지원)

## 주요 책임

- 다중 사이트 크롤링 관리
- Early Stop: 중복 감지 시 조기 중단
- 크롤링 주기 제어 (Cron 또는 수동 실행)
- 에러 핸들링 및 로깅

## 핵심 기능

### 1. 다중 사이트 크롤링

```python
def run_crawler():
    """크롤러 실행 메인 로직 (다중 사이트 지원)"""
    # 활성화된 모든 사이트 크롤링
    for site_key, site_config in Config.TARGET_SITES.items():
        if site_config.get("enabled", True):
            stats = crawl_site(site_key, site_config, db, Scraper)
```

### 2. 사이트별 크롤링 (Early Stop 지원)

```python
def crawl_site(site_key, site_config, db, scraper_class):
    """단일 사이트 크롤링 (Early Stop 지원)"""

    # User-Agent 랜덤 선택 (봇 차단 방지)
    user_agent = random.choice(Config.USER_AGENTS)

    # 사이트별 선택자로 Scraper 초기화
    scraper = scraper_class(
        base_url=site_config["base_url"],
        selectors=site_config["selectors"],
        user_agent=user_agent,  # User-Agent 주입
    )

    # 통계 초기화 (실패 카운트 포함)
    stats = {
        "new_posts": 0,
        "duplicates": 0,
        "images_saved": 0,
        "failed": 0,  # 파싱 실패 게시글 수
        "early_stopped": False
    }

    # Early Stop: 연속 중복 감지
    if consecutive_duplicates >= 5:
        return stats  # 조기 중단

    # Early Stop: 페이지 중복 비율 체크
    if page_duplicate_ratio >= 0.8:
        return stats  # 조기 중단
```

### 3. DatabaseManager 초기화 (R2 설정 포함)

```python
def run_crawler():
    """크롤러 실행 메인 로직"""
    # Storage 초기화 (R2 설정 포함)
    db = DatabaseManager(
        db_path=Config.DATABASE["path"],
        r2_config=Config.R2_CONFIG,  # R2 설정 전달
    )
```

### 3. 에러 핸들링

#### 재시도 로직

- **네트워크 오류**: `max_retries` (기본 3회) 재시도
- **지수 백오프**: 1초 → 2초 → 4초 대기 후 재시도
- **최종 실패**: 통계에 `failed` 카운트 추가

#### 실패 처리

- **파싱 실패**: 로그 기록 후 다음 게시글로 continue
- **이미지 저장 실패**: 에러 로그, 다른 이미지는 계속 저장
- **실패 통계**: 크롤링 완료 후 실패 건수 리포트

## 의존성

- `scraper.py`: HTML 파싱 모듈
- `storage.py`: DB/R2 저장 모듈
- `config.py`: 설정 관리 (TARGET_SITES, CRAWL_CONFIG)
- `logging_db.py`: SQLite 로그 저장 (→ `logs.db`)
- `APScheduler`: 스케줄링 라이브러리 (선택)

## 실행 방법

### 수동 실행

```bash
cd crawler
./venv/bin/python main.py
```

### Cron 설정 (2시간마다)

```bash
0 */2 * * * cd /path/to/crawler && ./venv/bin/python main.py >> /var/log/crawler.log 2>&1
```

## 로그 출력 예시

```
[2025-12-17 14:20:00] INFO: Crawler started
[2025-12-17 14:20:01] INFO: === Crawling dcinside ===
[2025-12-17 14:20:02] INFO: Page 1/10
[2025-12-17 14:20:15] WARNING: Failed to parse: https://example.com/post/123 (404 Not Found)
[2025-12-17 14:20:20] WARNING: Retry 1/3 after 1s: Timeout
[2025-12-17 14:20:30] INFO: Site dcinside completed: 15 new, 5 duplicates, 2 failed, 45 images
[2025-12-17 14:20:31] INFO: === Crawling clien ===
[2025-12-17 14:20:35] INFO: Early Stop: 5 consecutive duplicates found
[2025-12-17 14:20:35] INFO: Site clien completed: 3 new, 17 duplicates, 0 failed, 9 images (early stopped)
[2025-12-17 14:20:36] INFO: Crawler completed: 2 sites, 18 new posts, 22 duplicates, 2 failed, 54 images saved
```
