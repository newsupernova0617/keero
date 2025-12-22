"""
크롤러 엔트리포인트 및 스케줄러

역할:
- 크롤링 작업 스케줄링 및 실행 관리
- 설정 파일 로드 및 초기화
- 크롤링 주기 제어
- 에러 핸들링 및 로깅
"""

import logging
import random
import time

from config import Config
from logging_db import setup_logging
from scraper import ParseError

# 로깅 설정 (SQLite + 콘솔)
logger = setup_logging(
    db_path=Config.LOGGING["db_path"],
    level=logging.INFO,
    console=True,
)
logger = logging.getLogger(__name__)


def crawl_site(site_key: str, site_config: dict, db, scraper_class):
    """
    단일 사이트 크롤링 (Early Stop 지원)

    Note: 이 함수는 한 번에 하나의 사이트만 처리하는 헬퍼 함수입니다.
          다중 사이트 크롤링은 run_crawler()에서 이 함수를 반복 호출하여 구현됩니다.

    Args:
        site_key: 사이트 식별자
        site_config: 사이트 설정
        db: DatabaseManager 인스턴스
        scraper_class: Scraper 클래스

    Returns:
        dict: 크롤링 결과 통계
    """
    from config import Config

    logger.info(f"=== Crawling {site_key} ===")

    # User-Agent 랜덤 선택 (봇 차단 방지)
    user_agent = random.choice(Config.USER_AGENTS)
    logger.debug(f"Using User-Agent: {user_agent[:50]}...")

    # Scraper 초기화 (사이트별 선택자 사용)
    scraper = scraper_class(
        base_url=site_config["base_url"],
        list_url=site_config["list_url"],
        selectors=site_config["selectors"],
        user_agent=user_agent,
    )

    stats = {
        "new_posts": 0,
        "duplicates": 0,
        "images_saved": 0,
        "failed": 0,  # 파싱 실패 게시글 수
        "early_stopped": False,
    }

    consecutive_duplicates = 0
    early_stop_config = Config.CRAWL_CONFIG["early_stop"]

    # 페이지별 크롤링
    for page_num in range(1, Config.CRAWL_CONFIG["max_pages"] + 1):
        logger.info(f"📄 Page {page_num}/{Config.CRAWL_CONFIG['max_pages']}")

        post_urls = scraper.get_post_list(page_num)
        if not post_urls:
            logger.warning(f"⚠️  No posts found on page {page_num}")
            break
        
        logger.info(f"   Found {len(post_urls)} posts on page {page_num}")

        page_duplicates = 0
        page_total = len(post_urls)

        for url in post_urls:
            # 게시글 파싱 (Config의 max_retries 사용)
            try:
                post_data = scraper.parse_post(url, Config.CRAWL_CONFIG["max_retries"])
            except ParseError as e:
                logger.warning(f"❌ Failed to parse: {e}")
                stats["failed"] += 1
                continue

            if not post_data:
                logger.warning(f"❌ Failed to parse (returned None): {url}")
                stats["failed"] += 1
                continue
            
            # 게시물 제목 로그
            logger.debug(f"   Processing: {post_data['title'][:50]}...")

            # 사이트 이름 추가
            post_data["site_name"] = site_config["site_name"]

            # 게시글 저장 (HTML 포함 - 이미지 URL 자동 치환)
            post_id = db.save_post_with_html(post_data, post_data["images"])

            if not post_id:
                # 중복 게시글
                stats["duplicates"] += 1
                page_duplicates += 1
                consecutive_duplicates += 1
                logger.debug(f"   ⏭️  Duplicate: {post_data['title'][:40]}...")

                # Early Stop: 연속 중복 체크
                if (
                    early_stop_config["enabled"]
                    and consecutive_duplicates >= early_stop_config["consecutive_duplicates"]
                ):
                    logger.info(
                        f"Early Stop: {consecutive_duplicates} consecutive duplicates found"
                    )
                    stats["early_stopped"] = True
                    return stats
            else:
                # 새 게시글
                stats["new_posts"] += 1
                consecutive_duplicates = 0  # 리셋
                
                image_count = len(post_data["images"])
                logger.info(f"   ✅ New: {post_data['title'][:40]}... ({image_count} images)")
                
                # 이미지는 save_post_with_html에서 자동으로 저장됨
                stats["images_saved"] += image_count

            # 요청 간 딜레이
            time.sleep(Config.CRAWL_CONFIG["delay_between_requests"])
        
        # 페이지 요약
        page_new = stats["new_posts"] - (stats.get("prev_new", 0))
        stats["prev_new"] = stats["new_posts"]
        logger.info(f"   📊 Page {page_num} summary: {page_new} new, {page_duplicates} duplicates")

        # Early Stop: 페이지 중복 비율 체크
        if page_total > 0:
            duplicate_ratio = page_duplicates / page_total
            if (
                early_stop_config["enabled"]
                and duplicate_ratio >= early_stop_config["page_duplicate_ratio"]
            ):
                logger.info(f"🛑 Early Stop: Page {page_num} has {duplicate_ratio:.0%} duplicates")
                stats["early_stopped"] = True
                return stats

    return stats


def run_crawler():
    """
    크롤러 실행 메인 로직 (다중 사이트 지원)

    Config.TARGET_SITES에 정의된 모든 활성화된 사이트를 순회하며
    각 사이트마다 crawl_site()를 호출하여 크롤링을 수행합니다.
    """
    logger.info("Crawler started")

    try:
        from config import Config
        from scraper import Scraper
        from storage import DatabaseManager

        # Storage 초기화 (R2 설정 포함)
        db = DatabaseManager(
            db_path=Config.DATABASE["path"],
            r2_config=Config.R2_CONFIG,
        )

        total_stats = {
            "sites": 0,
            "new_posts": 0,
            "duplicates": 0,
            "images_saved": 0,
            "failed": 0,
        }

        # 활성화된 모든 사이트 크롤링
        for site_key, site_config in Config.TARGET_SITES.items():
            if not site_config.get("enabled", True):
                logger.info(f"Skipping disabled site: {site_key}")
                continue

            stats = crawl_site(site_key, site_config, db, Scraper)

            total_stats["sites"] += 1
            total_stats["new_posts"] += stats["new_posts"]
            total_stats["duplicates"] += stats["duplicates"]
            total_stats["images_saved"] += stats["images_saved"]
            total_stats["failed"] += stats["failed"]

            logger.info(
                f"Site {site_key} completed: "
                f"{stats['new_posts']} new, {stats['duplicates']} duplicates, "
                f"{stats['failed']} failed, {stats['images_saved']} images"
                + (" (early stopped)" if stats["early_stopped"] else "")
            )

        logger.info(
            f"Crawler completed: {total_stats['sites']} sites, "
            f"{total_stats['new_posts']} new posts, "
            f"{total_stats['duplicates']} duplicates, "
            f"{total_stats['failed']} failed, "
            f"{total_stats['images_saved']} images saved"
        )
    except Exception as e:
        logger.error(f"Crawler failed: {e}")
        raise


def main():
    """메인 함수"""
    run_crawler()

    # TODO: 스케줄러 설정 (선택사항)
    # from apscheduler.schedulers.blocking import BlockingScheduler
    # scheduler = BlockingScheduler()
    # scheduler.add_job(run_crawler, 'interval', hours=2)
    # logger.info("Scheduler started. Press Ctrl+C to exit.")
    # scheduler.start()


if __name__ == "__main__":
    main()
