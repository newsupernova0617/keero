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
    
    # ThreadPoolExecutor로 순차 실행 (e2-micro 메모리 제한: 1GB)
    # max_workers=1: OOM 방지, 안정성 우선
    executors = {
        'default': ThreadPoolExecutor(max_workers=1)  # 1개씩 순차 실행
    }
    
    scheduler = BackgroundScheduler(
        timezone='Asia/Seoul',
        executors=executors
    )
    
    # 6개 사이트를 순차 실행 (e2-micro 메모리 최적화)
    # 각 사이트 3분 간격 → 18분마다 전체 사이트 1회 업데이트
    sites = ["ruliweb", "todayhumor", "ppomppu", "fmkorea", "humoruniv", "dogdrip"]
    
    # 현재 시간
    now = datetime.now()
    
    # 각 사이트를 3분 간격으로 배치
    for i, site_name in enumerate(sites):
        # 첫 실행: 1분 후부터 시작, 3분씩 간격
        start_time = now + timedelta(minutes=1 + (i * 3))
        
        # 18분마다 반복 (6개 사이트 × 3분 = 18분)
        trigger = IntervalTrigger(
            minutes=18,  # 18분마다 반복
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
        
        logger.info(f"📅 {site_name} - First run at {start_time.strftime('%H:%M:%S')}, then every 18 minutes")
    
    # 등록된 작업 출력
    logger.info("=" * 80)
    logger.info("📋 Scheduled Jobs:")
    for job in scheduler.get_jobs():
        logger.info(f"  - {job.name}")
    
    logger.info("=" * 80)
    logger.info("✅ Scheduler is running with sequential execution (1 site at a time)")
    logger.info("💡 Sites run every 3 minutes in rotation")
    logger.info("🔄 All sites updated every 18 minutes")
    logger.info("💾 Memory-optimized for e2-micro (1GB RAM)")
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
