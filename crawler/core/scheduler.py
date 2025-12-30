"""
Railway용 크롤러 스케줄러

20분 간격으로 6개 사이트를 2그룹으로 나눠 병렬 크롤링합니다.
- 그룹 1 (00분): 루리웹, 오유, 뽐뿌 (3개 동시)
- 그룹 2 (10분): 펨코, 웃대, 개드립 (3개 동시)
- 20분마다 전체 사이트 업데이트
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
        from core.main import run_crawler
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
    
    # 6개 사이트를 2그룹으로 분할
    group1 = ["ruliweb", "todayhumor", "ppomppu"]      # 그룹 1: 1분 후
    group2 = ["fmkorea", "humoruniv", "dogdrip"]       # 그룹 2: 11분 후 (그룹1 + 10분)
    
    # 현재 시간
    now = datetime.now()
    
    # 그룹 1: 1분 후 시작, 20분마다 반복
    start_time_group1 = now + timedelta(minutes=1)
    for site_name in group1:
        trigger = IntervalTrigger(
            minutes=20,  # 20분마다
            start_date=start_time_group1,
            timezone='Asia/Seoul'
        )
        
        scheduler.add_job(
            crawl_site_job,
            trigger=trigger,
            args=[site_name],
            id=f'crawler_{site_name}',
            name=f'Crawl {site_name} (Group 1)',
            max_instances=1,  # 같은 사이트 동시 실행 방지
            coalesce=True,    # 누락된 작업 병합
            misfire_grace_time=300  # 5분 이내 누락 허용
        )
        
        logger.info(f"📅 Group 1: {site_name} - First run at {start_time_group1.strftime('%H:%M:%S')}, then every 20 minutes")
    
    # 그룹 2: 11분 후 시작 (그룹1 + 10분), 20분마다 반복
    start_time_group2 = now + timedelta(minutes=11)
    for site_name in group2:
        trigger = IntervalTrigger(
            minutes=20,  # 20분마다
            start_date=start_time_group2,
            timezone='Asia/Seoul'
        )
        
        scheduler.add_job(
            crawl_site_job,
            trigger=trigger,
            args=[site_name],
            id=f'crawler_{site_name}',
            name=f'Crawl {site_name} (Group 2)',
            max_instances=1,
            coalesce=True,
            misfire_grace_time=300
        )
        
        logger.info(f"📅 Group 2: {site_name} - First run at {start_time_group2.strftime('%H:%M:%S')}, then every 20 minutes")
    
    # 등록된 작업 출력
    logger.info("=" * 80)
    logger.info("📋 Scheduled Jobs:")
    for job in scheduler.get_jobs():
        logger.info(f"  - {job.name}")
    
    logger.info("=" * 80)
    logger.info("✅ Scheduler is running with 3 concurrent workers...")
    logger.info("💡 Group 1 starts in 1 minute, Group 2 starts in 11 minutes (10 min gap)")
    logger.info("🔄 All sites updated every 20 minutes")
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
