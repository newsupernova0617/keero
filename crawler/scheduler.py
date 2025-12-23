"""
Railway용 크롤러 스케줄러

4분 간격으로 8개 사이트를 병렬 크롤링합니다.
- 각 사이트는 32분마다 크롤링됨 (8 × 4분 = 32분)
- 사용자는 4분마다 새 글을 볼 수 있음
- BackgroundScheduler + ThreadPoolExecutor로 독립 실행
"""

import logging
import time
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime, timedelta

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def crawl_site_job(site_name):
    """단일 사이트 크롤링 작업"""
    try:
        logger.info(f"🚀 Starting crawl job for: {site_name}")
        from main import run_crawler
        run_crawler(site_filter=site_name)
        logger.info(f"✅ Completed crawl job for: {site_name}")
    except Exception as e:
        logger.error(f"❌ Failed crawl job for {site_name}: {e}")


def main():
    """메인 스케줄러"""
    logger.info("=" * 80)
    logger.info("🤖 Crawler Scheduler Starting...")
    logger.info("=" * 80)
    
    # ThreadPoolExecutor로 병렬 실행 (최대 3개 동시)
    executors = {
        'default': ThreadPoolExecutor(max_workers=3)
    }
    
    scheduler = BackgroundScheduler(
        timezone='Asia/Seoul',
        executors=executors
    )
    
    # 8개 사이트 목록 (순서대로 크롤링)
    sites = [
        "ruliweb",
        "todayhumor",
        "ppomppu",
        "fmkorea",
        "mlbpark",
        "clien",
        "humoruniv",
        "dogdrip"
    ]
    
    # 현재 시간
    now = datetime.now()
    
    # 각 사이트를 4분 간격으로 스케줄링
    for index, site_name in enumerate(sites):
        # 시작 시간: 현재 시간 + (인덱스 × 4분)
        start_time = now + timedelta(seconds=index * 240)  # 240초 = 4분
        
        # 32분(1920초) 간격으로 반복
        trigger = IntervalTrigger(
            seconds=1920,  # 32분 = 1920초 (8 × 4분)
            start_date=start_time,
            timezone='Asia/Seoul'
        )
        
        scheduler.add_job(
            crawl_site_job,
            trigger=trigger,
            args=[site_name],
            id=f'crawler_{site_name}',
            name=f'Crawl {site_name}',
            max_instances=1,  # 같은 사이트 동시 실행 방지
            coalesce=True,    # 누락된 작업 병합
            misfire_grace_time=300  # 5분 이내 누락 허용
        )
        
        logger.info(f"📅 Scheduled: {site_name} - First run at {start_time.strftime('%H:%M:%S')}, then every 32 minutes")
    
    # 등록된 작업 출력
    logger.info("=" * 80)
    logger.info("📋 Scheduled Jobs:")
    for job in scheduler.get_jobs():
        logger.info(f"  - {job.name}")
    
    logger.info("=" * 80)
    logger.info("✅ Scheduler is running with 3 concurrent workers...")
    logger.info("💡 Each site runs independently - delays won't affect others")
    logger.info("=" * 80)
    
    # 스케줄러 시작 (백그라운드)
    try:
        scheduler.start()
        
        # BackgroundScheduler는 non-blocking이므로 무한 루프 필요
        while True:
            time.sleep(60)  # 1분마다 체크
            
    except (KeyboardInterrupt, SystemExit):
        logger.info("🛑 Scheduler stopped")
        scheduler.shutdown()


if __name__ == "__main__":
    main()
