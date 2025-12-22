# config.py

## 개요

크롤러의 설정값을 관리하는 파일 (다중 사이트 지원)

## 주요 설정

### User-Agent 목록 (봇 차단 방지)

```python
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
]
```

- 크롤링 시 랜덤으로 선택되어 사용
- 다양한 브라우저 User-Agent를 순환하여 차단 방지

### 다중 사이트 설정 (사이트별 선택자 포함)

```python
TARGET_SITES = {
    "dcinside": {
        "base_url": "https://gall.dcinside.com",
        "list_url": "https://gall.dcinside.com/board/lists?id=dcbest",
        "site_name": "dcinside",
        "enabled": True,
        "selectors": {  # 사이트별 선택자
            "post_list": "tr.ub-content",
            "post_link": "td.gall_tit a",
            "title": "div.view_content_wrap h3",
            "content": "div.writing_view_box",
            "images": "div.writing_view_box img",
            "date": "span.gall_date",
        },
        "date_format": "auto",  # "auto" = dateutil 자동 파싱
    },
    "clien": {
        "base_url": "https://www.clien.net",
        "site_name": "clien",
        "enabled": True,
        "selectors": {  # 다른 선택자
            "post_list": "div.list_item",
            "post_link": "a.list_subject",
            ...
        },
        "date_format": "auto",
    }
}
```

### 크롤링 옵션 (Early Stop 포함)

```python
CRAWL_CONFIG = {
    "max_pages": 10,                    # 최대 크롤링 페이지 수
    "delay_between_requests": 1.0,      # 요청 간 딜레이 (초)
    "max_retries": 3,                   # HTTP 요청 실패 시 재시도 횟수
    "timeout": 30,                      # HTTP 요청 타임아웃 (초)

    # Early Stop: 중복 감지 시 조기 중단
    "early_stop": {
        "enabled": True,
        "consecutive_duplicates": 5,    # 연속 5개 중복 시 중단
        "page_duplicate_ratio": 0.8     # 페이지 80% 중복 시 중단
    }
}
```

### 데이터베이스

```python
DATABASE = {
    "path": os.getenv("DB_PATH", "../data/posts.db"),
    "wal_mode": True
}
```

### R2 설정

```python
R2_CONFIG = {
    "account_id": os.getenv("R2_ACCOUNT_ID"),
    "access_key_id": os.getenv("R2_ACCESS_KEY_ID"),
    "secret_access_key": os.getenv("R2_SECRET_ACCESS_KEY"),
    "bucket_name": os.getenv("R2_BUCKET_NAME")
}
```

### 로깅 설정

```python
LOGGING = {
    "db_path": os.getenv("LOGS_DB_PATH", "../data/logs.db"),
    "retention_days": int(os.getenv("LOGS_RETENTION_DAYS", "30"))
}
```

## 환경 변수 (.env)

```bash
R2_ACCOUNT_ID=your_account_id
R2_ACCESS_KEY_ID=your_access_key
R2_SECRET_ACCESS_KEY=your_secret_key
R2_BUCKET_NAME=humor-posts
DB_PATH=../data/posts.db
```

## 보안 주의사항

> [!CAUTION]
>
> - API 키를 코드에 하드코딩 금지
> - `.env` 파일을 Git에 커밋 금지
> - `.gitignore`에 `.env` 추가 필수
