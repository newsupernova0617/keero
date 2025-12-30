"""
테스트용 크롤러 스케줄러 (5분 간격, 30분 테스트)

목적:
- Railway 배포 전 스케줄러 로직 검증
- 5분 간격으로 실제 새 게시글 수집 가능
- 30분 = 12회 실행 (각 그룹 6회)

실행 타임라인:
00:00 → 그룹1 (루리웹, 오유, 뽐뿌)
02:30 → 그룹2 (펨코, 웃대, 개드립)
05:00 → 그룹1 재실행
07:30 → 그룹2 재실행
...
30:00 → 테스트 종료
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
    """테스트용 스케줄러 (5분 간격)"""
    logger.info("=" * 80)
    logger.info("🧪 TEST Crawler Scheduler Starting...")
    logger.info("⏱️  Interval: 5 minutes")
    logger.info("⏰ Test Duration: 30 minutes")
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
    group1 = ["ruliweb", "todayhumor", "ppomppu"]      # 그룹 1: 00분
    group2 = ["fmkorea", "humoruniv", "dogdrip"]       # 그룹 2: 2.5분 후
    
    # 현재 시간
    now = datetime.now()
    test_end_time = now + timedelta(minutes=30)  # 30분 후 종료
    
    logger.info(f"🕐 Test Start: {now.strftime('%H:%M:%S')}")
    logger.info(f"🕐 Test End:   {test_end_time.strftime('%H:%M:%S')}")
    logger.info("=" * 80)
    
    # 그룹 1: 즉시 1회 실행 + 5분마다 반복
    logger.info("🚀 Executing Group 1 immediately...")
    for site_name in group1:
        # 즉시 실행
        scheduler.add_job(
            crawl_site_job,
            args=[site_name],
            id=f'crawler_{site_name}_immediate',
            name=f'Crawl {site_name} (Immediate)'
        )
        
        # 5분 후부터 반복
        trigger = IntervalTrigger(
            minutes=5,
            start_date=now + timedelta(minutes=5),
            end_date=test_end_time,
            timezone='Asia/Seoul'
        )
        
        scheduler.add_job(
            crawl_site_job,
            trigger=trigger,
            args=[site_name],
            id=f'crawler_{site_name}',
            name=f'Crawl {site_name} (Group 1)',
            max_instances=1,
            coalesce=True,
            misfire_grace_time=300
        )
        
        logger.info(f"📅 Group 1: {site_name} - Immediate + every 5 minutes")
    
    # 그룹 2: 2.5분 후 시작, 5분마다 반복
    start_time_group2 = now + timedelta(minutes=2, seconds=30)
    for site_name in group2:
        trigger = IntervalTrigger(
            minutes=5,  # 5분마다
            start_date=start_time_group2,
            end_date=test_end_time,  # 30분 후 종료
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
        
        logger.info(f"📅 Group 2: {site_name} - First run at {start_time_group2.strftime('%H:%M:%S')}, then every 5 minutes")
    
    # 등록된 작업 출력
    logger.info("=" * 80)
    logger.info("📋 Scheduled Jobs:")
    for job in scheduler.get_jobs():
        logger.info(f"  - {job.name}")
    
    logger.info("=" * 80)
    logger.info("✅ Test Scheduler is running...")
    logger.info("💡 2 groups of 3 sites each, 2.5 minutes apart")
    logger.info("🔄 Each site runs every 5 minutes")
    logger.info("⏰ Test will automatically stop after 30 minutes")
    logger.info("=" * 80)
    
    # 스케줄러 시작
    try:
        scheduler.start()
        
        # 30분 대기 (자동 종료)
        logger.info("⏳ Waiting for 30 minutes...")
        time.sleep(30 * 60)  # 30분
        
        logger.info("=" * 80)
        logger.info("🎉 Test completed successfully!")
        logger.info("=" * 80)
        
        scheduler.shutdown()
        
    except (KeyboardInterrupt, SystemExit):
        logger.info("🛑 Test stopped manually")
        scheduler.shutdown()


if __name__ == "__main__":
    main()
