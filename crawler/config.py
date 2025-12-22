"""
크롤러 설정 파일

역할:
- 타겟 사이트 설정 (다중 사이트 지원)
- 크롤링 옵션 설정
- 데이터베이스 설정
- R2 설정
"""

import os

from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()


class Config:
    """크롤러 설정 클래스"""

    # User-Agent 목록 (랜덤 선택으로 차단 방지)
    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
    ]

    # 다중 사이트    # 크롤링 대상 사이트
    TARGET_SITES = {
        "example": {
            "base_url": "https://example.com",
            "list_url": "https://example.com/posts",
            "site_name": "example",
            "enabled": False,  # 예제 사이트 비활성화
            "selectors": {
                "post_list": "div.post-list article",
                "post_link": "h2.title a",
                "title": "h2.title",
                "content": "div.post-content",
                "images": "div.post-content img",
                "date": "span.date",
            },
            # 날짜 파싱 설정
            "date_format": "auto",  # "auto" = dateutil 자동 파싱, 또는 strptime 형식
        },
        # 실제 사이트: FMKorea
        "fmkorea": {
            "base_url": "https://www.fmkorea.com",
            "list_url": "https://www.fmkorea.com/best",
            "site_name": "fmkorea",
            "enabled": True,  # 활성화 (Playwright로 시도)
            "use_playwright": True,  # Playwright 사용
            "selectors": {
                "post_list": "div.fm_best_widget > ul li",
                "post_link": "h3.title a",
                "title": "h3.title a",
                "content": "div.rd_body.clear",
                "images": "div.rd_body img",
                "date": "span.date.m_no",
            },
            "date_format": "auto",  # 2025.12.21 17:00 형식 자동 파싱
        },
        # 실제 사이트: 루리웹 유머 베스트
        "ruliweb": {
            "base_url": "https://bbs.ruliweb.com",
            "list_url": "https://bbs.ruliweb.com/best/humor",
            "site_name": "ruliweb",
            "enabled": True,  # 활성화
            "use_playwright": False,  # requests 사용
            "selectors": {
                "post_list": "table.board_list_table tbody tr",
                "post_link": "a.subject_link",
                "title": "a.subject_link",
                "content": "div.view_content",
                "images": "div.view_content img",
                "date": "td.time",
            },
            "date_format": "auto",  # HH:MM 또는 YYYY.MM.DD 형식 자동 파싱
        },
        # 엠엘비파크 (MLBPark)
        "mlbpark": {
            "base_url": "https://mlbpark.donga.com",
            "list_url": "https://mlbpark.donga.com/mp/b.php?b=bullpen",
            "site_name": "mlbpark",
            "enabled": True,  # 활성화 (올바른 도메인으로 수정)
            "use_playwright": True,  # Playwright 사용
            "selectors": {
                "post_list": "div.talk_list table tbody tr",
                "post_link": "a.txt",
                "title": "a.txt",
                "content": "div.ar_txt",
                "images": "div.ar_txt img",
                "date": "td:nth-child(4)",
            },
            "date_format": "auto",
        },
        # 클리앙 (Clien)
        "clien": {
            "base_url": "https://www.clien.net",
            "list_url": "https://www.clien.net/service/board/park",  # 자유게시판 (모두의공원)
            "site_name": "clien",
            "enabled": True,  # 비활성화 (테스트 후 활성화)
            "use_playwright": True,  # Cloudflare 우회 필요
            "selectors": {
                "post_list": "div.list_item",
                "post_link": "a.list_subject",
                "title": "a.list_subject",
                "content": "div.post_article",
                "images": "div.post_article img",
                "date": "span.time",
            },
            "date_format": "auto",
        },
        # 웃긴대학 (Humoruniv)
        "humoruniv": {
            "base_url": "https://web.humoruniv.com",
            "list_url": "https://web.humoruniv.com/board/humor/list.html?table=pds",
            "site_name": "humoruniv",
            "enabled": True,  # 비활성화 (테스트 후 활성화)
            "use_playwright": True,  # JavaScript 렌더링 필요
            "selectors": {
                "post_list": "table tr",
                "post_link": "a[href*='read']",
                "title": "a[href*='read']",
                "content": "div.board_body",
                "images": "div.board_body img",
                "date": "td.datetime",
            },
            "date_format": "auto",
        },
        # 개드립 (Dogdrip)
        "dogdrip": {
            "base_url": "https://www.dogdrip.net",
            "list_url": "https://www.dogdrip.net/index.php?mid=dogdrip",
            "site_name": "dogdrip",
            "enabled": True,  # 비활성화 (테스트 후 활성화)
            "use_playwright": True,  # JavaScript 렌더링 필요
            "selectors": {
                "post_list": "li.ed",
                "post_link": "a",
                "title": "a",
                "content": "div.xe_content",
                "images": "div.xe_content img",
                "date": "span.time",
            },
            "date_format": "auto",
        },
        # 오늘의유머 (TodayHumor)
        "todayhumor": {
            "base_url": "http://www.todayhumor.co.kr",
            "list_url": "http://www.todayhumor.co.kr/board/list.php?table=bestofbest",
            "site_name": "todayhumor",
            "enabled": True,  # 비활성화 (테스트 후 활성화)
            "use_playwright": False,  # requests로 충분
            "selectors": {
                "post_list": "table.table_list tbody tr",
                "post_link": "td.subject a",
                "title": "td.subject a",
                "content": "div.viewbody",
                "images": "div.viewbody img",
                "date": "td.date",
            },
            "date_format": "auto",
        },
        # 뽐뿌 (Ppomppu)
        "ppomppu": {
            "base_url": "https://www.ppomppu.co.kr",
            "list_url": "https://www.ppomppu.co.kr/zboard/zboard.php?id=humor",
            "site_name": "ppomppu",
            "enabled": True,  # 비활성화 (테스트 후 활성화)
            "use_playwright": False,  # requests로 충분
            "selectors": {
                "post_list": "table tbody tr",
                "post_link": "td.list_title a",
                "title": "td.list_title a",  
                "content": "div.board-contents",
                "images": "div.board-contents img",
                "date": "td.list_time",
            },
            "date_format": "auto",
        },
    }

    # 크롤링 옵션
    CRAWL_CONFIG = {
        "max_pages": 3,
        "delay_between_requests": 3.0,
        "max_retries": 3,
        "timeout": 30,
        # Early Stop: 중복 감지 시 조기 중단
        "early_stop": {
            "enabled": True,
            "consecutive_duplicates": 5,  # 연속 N개 중복 시 중단
            "page_duplicate_ratio": 0.8,  # 페이지의 N% 중복 시 중단
        },
        # Batch Commit: DB 잠금 최소화
        "batch_commit": {
            "enabled": True,
            "chunk_size": 20,  # N개 게시글마다 커밋 (권장: 10~50)
            "max_time_seconds": 5,  # N초마다 커밋 (권장: 3~10)
        },
    }

    # 데이터베이스
    DATABASE = {
        "path": os.getenv("DB_PATH", "../data/posts.db"),
        "wal_mode": True,
    }

    # R2 설정
    R2_CONFIG = {
        "account_id": os.getenv("R2_ACCOUNT_ID"),
        "access_key_id": os.getenv("R2_ACCESS_KEY_ID"),
        "secret_access_key": os.getenv("R2_SECRET_ACCESS_KEY"),
        "bucket_name": os.getenv("R2_BUCKET_NAME", "humor-posts"),
        # 공개 URL (R2 Public Bucket URL 또는 Custom Domain)
        # 예: https://pub-xxxxx.r2.dev 또는 https://cdn.yourdomain.com
        "public_url": os.getenv("R2_PUBLIC_URL", ""),
    }

    # 로깅 설정
    LOGGING = {
        "db_path": os.getenv("LOGS_DB_PATH", "../data/logs.db"),
        "retention_days": int(os.getenv("LOGS_RETENTION_DAYS", "30")),
    }
