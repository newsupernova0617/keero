"""
Railway용 크롤러 스케줄러

7분 30초 간격으로 8개 사이트를 순차적으로 크롤링합니다.
- 각 사이트는 1시간마다 크롤링됨 (8 × 7.5분 = 60분)
- 사용자는 7분 30초마다 새 글을 볼 수 있음
"""

import logging
from apscheduler.schedulers.blocking import BlockingScheduler
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
    
    scheduler = BlockingScheduler(timezone='Asia/Seoul')
    
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
    
    # 각 사이트를 7분 30초 간격으로 스케줄링
    for index, site_name in enumerate(sites):
        # 시작 시간: 현재 시간 + (인덱스 × 7분 30초)
        start_time = now + timedelta(seconds=index * 450)  # 450초 = 7분 30초
        
        # 1시간(3600초) 간격으로 반복
        trigger = IntervalTrigger(
            seconds=3600,  # 1시간 = 3600초
            start_date=start_time,
            timezone='Asia/Seoul'
        )
        
        scheduler.add_job(
            crawl_site_job,
            trigger=trigger,
            args=[site_name],
            id=f'crawler_{site_name}',
            name=f'Crawl {site_name}',
            max_instances=1,  # 동시 실행 방지
            coalesce=True,    # 누락된 작업 병합
            misfire_grace_time=300  # 5분 이내 누락 허용
        )
        
        logger.info(f"📅 Scheduled: {site_name} - First run at {start_time.strftime('%H:%M:%S')}, then every 1 hour")
    
    # 등록된 작업 출력
    logger.info("=" * 80)
    logger.info("📋 Scheduled Jobs:")
    for job in scheduler.get_jobs():
        next_run = job.next_run_time.strftime('%H:%M:%S') if job.next_run_time else 'N/A'
        logger.info(f"  - {job.name} (Next: {next_run})")
    
    logger.info("=" * 80)
    logger.info("✅ Scheduler is running... Press Ctrl+C to exit")
    logger.info("=" * 80)
    
    # 스케줄러 시작 (블로킹)
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("🛑 Scheduler stopped")
        scheduler.shutdown()


if __name__ == "__main__":
    main()
