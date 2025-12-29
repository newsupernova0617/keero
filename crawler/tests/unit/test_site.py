#!/usr/bin/env python3
"""
개별 사이트 크롤링 테스트 스크립트

사용법:
    python test_site.py fmkorea
    python test_site.py ruliweb
    python test_site.py mlbpark
    python test_site.py clien
    python test_site.py humoruniv
    python test_site.py dogdrip
    python test_site.py todayhumor
    python test_site.py ppomppu
    python test_site.py all  # 모든 사이트 테스트
"""

import asyncio
import sys
from datetime import datetime

from core.config import Config
from crawler import Crawler
from db import Database
from logger import CrawlerLogger


async def test_single_site(site_key: str):
    """단일 사이트 크롤링 테스트"""
    
    # 사이트 설정 확인
    if site_key not in Config.TARGET_SITES:
        print(f"❌ 알 수 없는 사이트: {site_key}")
        print(f"사용 가능한 사이트: {', '.join(Config.TARGET_SITES.keys())}")
        return False
    
    site_config = Config.TARGET_SITES[site_key]
    
    if not site_config.get("enabled", False):
        print(f"⚠️  사이트 '{site_key}'는 비활성화되어 있습니다.")
        print(f"계속 테스트하시겠습니까? (y/n): ", end="")
        response = input().strip().lower()
        if response != 'y':
            return False
    
    print(f"\n{'='*60}")
    print(f"🧪 사이트 테스트: {site_config['site_name']}")
    print(f"{'='*60}")
    print(f"URL: {site_config['list_url']}")
    print(f"Playwright 사용: {site_config.get('use_playwright', False)}")
    print(f"시작 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")
    
    # DB 및 로거 초기화
    db = Database(Config.DATABASE["path"])
    logger = CrawlerLogger(Config.LOGGING["db_path"])
    
    # 크롤러 초기화
    crawler = Crawler(db, logger)
    
    try:
        # 크롤링 실행
        start_time = datetime.now()
        result = await crawler.crawl_site(site_key, site_config)
        end_time = datetime.now()
        
        duration = (end_time - start_time).total_seconds()
        
        # 결과 출력
        print(f"\n{'='*60}")
        print(f"✅ 크롤링 완료!")
        print(f"{'='*60}")
        print(f"소요 시간: {duration:.2f}초")
        print(f"새 게시글: {result.get('new_posts', 0)}개")
        print(f"중복 게시글: {result.get('duplicate_posts', 0)}개")
        print(f"실패한 게시글: {result.get('failed_posts', 0)}개")
        print(f"총 처리: {result.get('total_processed', 0)}개")
        
        if result.get('early_stopped', False):
            print(f"⚠️  Early Stop 발동: {result.get('early_stop_reason', 'Unknown')}")
        
        print(f"{'='*60}\n")
        
        return True
        
    except Exception as e:
        print(f"\n{'='*60}")
        print(f"❌ 크롤링 실패!")
        print(f"{'='*60}")
        print(f"에러: {str(e)}")
        print(f"{'='*60}\n")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        # 크롤러 종료
        await crawler.close()


async def test_all_sites():
    """모든 활성화된 사이트 테스트"""
    print(f"\n{'='*60}")
    print(f"🧪 전체 사이트 테스트")
    print(f"{'='*60}\n")
    
    enabled_sites = [
        key for key, config in Config.TARGET_SITES.items()
        if config.get("enabled", False)
    ]
    
    print(f"테스트할 사이트 ({len(enabled_sites)}개):")
    for site_key in enabled_sites:
        site_name = Config.TARGET_SITES[site_key]["site_name"]
        print(f"  - {site_key} ({site_name})")
    
    print(f"\n{'='*60}\n")
    
    results = {}
    
    for i, site_key in enumerate(enabled_sites, 1):
        print(f"\n[{i}/{len(enabled_sites)}] 테스트 중...\n")
        success = await test_single_site(site_key)
        results[site_key] = success
        
        # 다음 사이트로 넘어가기 전 잠시 대기
        if i < len(enabled_sites):
            print(f"⏳ 다음 사이트 테스트까지 3초 대기...\n")
            await asyncio.sleep(3)
    
    # 전체 결과 요약
    print(f"\n{'='*60}")
    print(f"📊 전체 테스트 결과")
    print(f"{'='*60}")
    
    success_count = sum(1 for success in results.values() if success)
    fail_count = len(results) - success_count
    
    for site_key, success in results.items():
        status = "✅ 성공" if success else "❌ 실패"
        site_name = Config.TARGET_SITES[site_key]["site_name"]
        print(f"{status} - {site_key} ({site_name})")
    
    print(f"\n성공: {success_count}개 | 실패: {fail_count}개")
    print(f"{'='*60}\n")


def print_usage():
    """사용법 출력"""
    print("\n사용법:")
    print("  python test_site.py <site_key>")
    print("\n사용 가능한 사이트:")
    
    for key, config in Config.TARGET_SITES.items():
        if key == "example":
            continue
        enabled = "✅" if config.get("enabled", False) else "⚠️ "
        site_name = config["site_name"]
        print(f"  {enabled} {key:15} - {site_name}")
    
    print("\n특수 명령:")
    print("  all                - 모든 활성화된 사이트 테스트")
    print("\n예시:")
    print("  python test_site.py fmkorea")
    print("  python test_site.py all")
    print()


async def main():
    """메인 함수"""
    
    # 인자 확인
    if len(sys.argv) < 2:
        print("❌ 사이트를 지정해주세요.")
        print_usage()
        sys.exit(1)
    
    site_key = sys.argv[1].lower()
    
    # 도움말
    if site_key in ["-h", "--help", "help"]:
        print_usage()
        sys.exit(0)
    
    # 전체 테스트
    if site_key == "all":
        await test_all_sites()
        sys.exit(0)
    
    # 개별 사이트 테스트
    success = await test_single_site(site_key)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  사용자에 의해 중단되었습니다.")
        sys.exit(1)
