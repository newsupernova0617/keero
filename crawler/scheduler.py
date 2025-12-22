"""
Railway용 크롤러 스케줄러

15분 간격으로 8개 사이트를 로테이션하며 크롤링합니다.
- 각 사이트는 2시간마다 크롤링됨
- 사용자는 15분마다 새 글을 볼 수 있음
"""

import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime

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
    
    scheduler = BlockingScheduler()
    
    # 8개 사이트 스케줄 정의
    # (사이트명, 시작 시간(분), 시작 시간(시))
    sites_schedule = [
        ("ruliweb", 0, "0,2,4,6,8,10,12,14,16,18,20,22"),      # 매 짝수 시간 00분
        ("todayhumor", 15, "0,2,4,6,8,10,12,14,16,18,20,22"),  # 매 짝수 시간 15분
        ("ppomppu", 30, "0,2,4,6,8,10,12,14,16,18,20,22"),     # 매 짝수 시간 30분
        ("fmkorea", 45, "0,2,4,6,8,10,12,14,16,18,20,22"),     # 매 짝수 시간 45분
        ("mlbpark", 0, "1,3,5,7,9,11,13,15,17,19,21,23"),      # 매 홀수 시간 00분
        ("clien", 15, "1,3,5,7,9,11,13,15,17,19,21,23"),       # 매 홀수 시간 15분
        ("humoruniv", 30, "1,3,5,7,9,11,13,15,17,19,21,23"),   # 매 홀수 시간 30분
        ("dogdrip", 45, "1,3,5,7,9,11,13,15,17,19,21,23"),     # 매 홀수 시간 45분
    ]
    
    # 스케줄 등록
    for site_name, minute, hours in sites_schedule:
        trigger = CronTrigger(
            hour=hours,
            minute=minute,
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
        
        logger.info(f"📅 Scheduled: {site_name} at minute={minute}, hours={hours}")
    
    # 등록된 작업 출력
    logger.info("=" * 80)
    logger.info("📋 Scheduled Jobs:")
    for job in scheduler.get_jobs():
        logger.info(f"  - {job.name}")
    
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
