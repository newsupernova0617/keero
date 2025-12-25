"""
크롤러 엔트리포인트 및 스케줄러

역할:
- 크롤링 작업 스케줄링 및 실행 관리
- 설정 파일 로드 및 초기화
- 크롤링 주기 제어
- 에러 핸들링 및 로깅
"""

import sys
import argparse
import logging
import random
import time

# 출력 버퍼링 비활성화 (실시간 로그 출력)
sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

from config import Config
from logging_db import setup_logging
from scraper import ParseError
from storage import Image

# 로깅 설정 (SQLite + 콘솔)
logger = setup_logging(
    db_path=Config.LOGGING["db_path"],
    level=logging.INFO,
    console=True,
)
logger = logging.getLogger(__name__)


def crawl_site(site_key: str, site_config: dict, db, scraper_class, limit: int = None):
    """
    단일 사이트 크롤링 (Early Stop + Batch Commit 지원)

    Note: 이 함수는 한 번에 하나의 사이트만 처리하는 헬퍼 함수입니다.
          다중 사이트 크롤링은 run_crawler()에서 이 함수를 반복 호출하여 구현됩니다.

    Args:
        site_key: 사이트 식별자
        site_config: 사이트 설정
        db: DatabaseManager 인스턴스
        scraper_class: Scraper 클래스
        limit: 크롤링할 최대 게시글 수 (미니테스트용, None이면 제한 없음)

    Returns:
        dict: 크롤링 결과 통계
    """
    import time as time_module
    from config import Config

    logger.info(f"=== Crawling {site_key} ===" + (f" (limit: {limit} posts)" if limit else ""))

    # User-Agent 랜덤 선택 (봇 차단 방지)
    user_agent = random.choice(Config.USER_AGENTS)
    logger.debug(f"Using User-Agent: {user_agent[:50]}...")

    # Scraper 초기화 (사이트별 선택자 사용)
    scraper = scraper_class(
        base_url=site_config["base_url"],
        list_url=site_config["list_url"],
        selectors=site_config["selectors"],
        user_agent=user_agent,
        use_playwright=site_config.get("use_playwright", False),  # Playwright 사용 여부
    )

    stats = {
        "new_posts": 0,
        "duplicates": 0,
        "images_saved": 0,
        "failed": 0,  # 파싱 실패 게시글 수
        "early_stopped": False,
        "commits": 0,  # 커밋 횟수 추적
    }

    consecutive_duplicates = 0
    early_stop_config = Config.CRAWL_CONFIG["early_stop"]
    batch_config = Config.CRAWL_CONFIG["batch_commit"]
    
    # 배치 커밋 설정
    batch_enabled = batch_config.get("enabled", False)
    chunk_size = batch_config.get("chunk_size", 20)
    max_time_seconds = batch_config.get("max_time_seconds", 5)
    
    if batch_enabled:
        logger.info(f"📦 Batch mode: commit every {chunk_size} posts or {max_time_seconds}s")
    
    # 배치 처리 상태
    posts_since_commit = 0
    last_commit_time = time_module.time()
    total_processed = 0  # 미니테스트용 카운터

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
            # 미니테스트 limit 체크
            if limit and total_processed >= limit:
                logger.info(f"🎯 Limit reached: {limit} posts processed")
                stats["early_stopped"] = True
                
                # 마지막 커밋 (배치 모드)
                if batch_enabled and posts_since_commit > 0:
                    commit_start = time_module.time()
                    db.flush()
                    commit_time = time_module.time() - commit_start
                    
                    stats["commits"] += 1
                    logger.info(f"   💾 Final commit: {posts_since_commit} posts ({commit_time*1000:.0f}ms DB)")
                
                return stats
            
            total_processed += 1
            
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
                        f"⏹️  Early Stop: {consecutive_duplicates} consecutive duplicates found"
                    )
                    stats["early_stopped"] = True
                    
                    # 마지막 커밋 (배치 모드)
                    if batch_enabled and posts_since_commit > 0:
                        commit_start = time_module.time()
                        db.flush()
                        commit_time = time_module.time() - commit_start
                        
                        stats["commits"] += 1
                        logger.info(f"   💾 Final commit: {posts_since_commit} posts ({commit_time*1000:.0f}ms DB)")
                    
                    return stats
            else:
                # 새 게시글
                stats["new_posts"] += 1
                consecutive_duplicates = 0  # 리셋
                posts_since_commit += 1
                
                # 미디어 타입별 개수 확인 (DB에서 조회)
                media_count = len(post_data["images"])
                
                # 저장 후 실제 미디어 타입 확인
                try:
                    # 방금 저장된 게시글의 이미지 정보 조회
                    saved_images = db.session.query(Image).filter_by(post_id=post_id).all()
                    
                    # 타입별로 분류
                    webp_count = sum(1 for img in saved_images if img.optimized_format == 'webp')
                    webm_count = sum(1 for img in saved_images if img.optimized_format == 'webm')
                    gif_count = sum(1 for img in saved_images if img.optimized_format == 'gif')
                    
                    # 로그 메시지 구성
                    media_parts = []
                    if webp_count > 0:
                        media_parts.append(f"{webp_count} images")
                    if webm_count > 0:
                        media_parts.append(f"{webm_count} videos/GIFs")
                    if gif_count > 0:
                        media_parts.append(f"{gif_count} static GIFs")
                    
                    media_str = ", ".join(media_parts) if media_parts else f"{media_count} media"
                    logger.info(f"   ✅ New: {post_data['title'][:40]}... ({media_str})")
                except:
                    # fallback
                    logger.info(f"   ✅ New: {post_data['title'][:40]}... ({media_count} media)")
                
                # 이미지는 save_post_with_html에서 자동으로 저장됨
                stats["images_saved"] += media_count
                
                # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                # 배치 커밋 로직
                # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                if batch_enabled:
                    current_time = time_module.time()
                    time_elapsed = current_time - last_commit_time
                    
                    # 1. 청크 크기 도달 또는 2. 시간 초과
                    if posts_since_commit >= chunk_size or time_elapsed >= max_time_seconds:
                        # SQLite 커밋 시간 측정
                        commit_start = time_module.time()
                        db.flush()
                        commit_time = time_module.time() - commit_start
                        
                        stats["commits"] += 1
                        logger.info(f"   💾 Batch commit: {posts_since_commit} posts ({time_elapsed:.1f}s total, {commit_time*1000:.0f}ms DB)")
                        posts_since_commit = 0
                        last_commit_time = current_time

            # 요청 간 딜레이
            time.sleep(Config.CRAWL_CONFIG["delay_between_requests"])
        
        # 페이지 요약
        page_new = stats["new_posts"] - (stats.get("prev_new", 0))
        stats["prev_new"] = stats["new_posts"]
        logger.info(
            f"   Page {page_num} summary: {page_new} new, {page_duplicates} duplicates"
        )

        # Early Stop: 페이지 중복률 체크
        if (
            early_stop_config["enabled"]
            and page_total > 0
            and (page_duplicates / page_total) >= early_stop_config["page_duplicate_ratio"]
        ):
            logger.info(
                f"⏹️  Early Stop: Page duplicate ratio {page_duplicates}/{page_total} "
                f"= {page_duplicates/page_total:.1%}"
            )
            stats["early_stopped"] = True
            break

    # 최종 커밋 (배치 모드에서 남은 데이터)
    if batch_enabled and posts_since_commit > 0:
        commit_start = time_module.time()
        db.flush()
        commit_time = time_module.time() - commit_start
        
        stats["commits"] += 1
        logger.info(f"   💾 Final commit: {posts_since_commit} posts ({commit_time*1000:.0f}ms DB)")

    return stats


def run_crawler(site_filter=None, limit=None):
    """
    크롤러 실행 메인 로직 (다중 사이트 지원)

    Config.TARGET_SITES에 정의된 모든 활성화된 사이트를 순회하며
    각 사이트마다 crawl_site()를 호출하여 크롤링을 수행합니다.
    
    Args:
        site_filter: 특정 사이트만 크롤링 (예: 'ruliweb', 'fmkorea')
        limit: 크롤링할 최대 게시글 수 (미니테스트용, None이면 제한 없음)
    """
    logger.info(f"Crawler started{f' (site: {site_filter})' if site_filter else ''}{f' (limit: {limit})' if limit else ''}")

    try:
        from config import Config
        from scraper import Scraper
        from storage import DatabaseManager

        # 배치 커밋 설정 확인
        batch_enabled = Config.CRAWL_CONFIG["batch_commit"].get("enabled", False)
        
        # Storage 초기화 (R2 설정 + 배치 모드)
        db = DatabaseManager(
            db_path=Config.DATABASE["path"],
            r2_config=Config.R2_CONFIG,
            auto_commit=not batch_enabled,  # 배치 모드면 auto_commit=False
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
            # site_filter가 지정되었으면 해당 사이트만 크롤링
            if site_filter and site_key != site_filter:
                continue
                
            if not site_config.get("enabled", True):
                logger.info(f"Skipping disabled site: {site_key}")
                continue

            total_stats["sites"] += 1
            stats = crawl_site(site_key, site_config, db, Scraper, limit=limit)

            total_stats["new_posts"] += stats["new_posts"]
            total_stats["duplicates"] += stats["duplicates"]
            total_stats["images_saved"] += stats["images_saved"]
            total_stats["failed"] += stats["failed"]

            logger.info(
                f"Site {site_key} completed: {stats['new_posts']} new, "
                f"{stats['duplicates']} duplicates, "
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
    parser = argparse.ArgumentParser(description='Community humor crawler')
    parser.add_argument('--site', type=str, help='Crawl specific site only (e.g., ruliweb, fmkorea)')
    parser.add_argument('--limit', type=int, help='Limit number of posts to crawl (for testing, e.g., 3)')
    args = parser.parse_args()
    
    if args.site:
        # 단일 사이트 크롤링
        logger.info(f"Crawling single site: {args.site}")
        run_crawler(site_filter=args.site, limit=args.limit)
    else:
        # 모든 사이트 크롤링
        run_crawler(limit=args.limit)


if __name__ == "__main__":
    main()
