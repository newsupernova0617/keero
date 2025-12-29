"""
특정 게시물 재크롤링 스크립트
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from core.config import Config
from core.scraper import Scraper
from core.storage import DatabaseManager
from sqlalchemy import create_engine, text

def recrawl_post(post_id: int):
    """특정 게시물 재크롤링"""
    
    # DB 연결
    engine = create_engine(f"sqlite:///{Config.DATABASE['path']}")
    
    with engine.connect() as conn:
        # 게시물 정보 조회
        result = conn.execute(text("""
            SELECT source_url, site_name, title
            FROM posts
            WHERE id = :post_id
        """), {"post_id": post_id})
        
        row = result.fetchone()
        if not row:
            print(f"게시물 ID {post_id}를 찾을 수 없습니다.")
            return
        
        source_url, site_name, title = row
        print(f"게시물: {title}")
        print(f"URL: {source_url}")
        print(f"사이트: {site_name}")
        
        # 기존 이미지 삭제
        result = conn.execute(text("""
            DELETE FROM images WHERE post_id = :post_id
        """), {"post_id": post_id})
        deleted_count = result.rowcount
        conn.commit()
        print(f"\n기존 이미지 {deleted_count}개 삭제")
        
        # 게시물 삭제 (재크롤링을 위해)
        conn.execute(text("""
            DELETE FROM posts WHERE id = :post_id
        """), {"post_id": post_id})
        conn.commit()
        print(f"게시물 삭제 완료")
    
    # 재크롤링
    print(f"\n재크롤링 시작...")
    
    # Storage 초기화
    db = DatabaseManager(
        db_path=Config.DATABASE["path"],
        r2_config=Config.R2_CONFIG,
        auto_commit=True,
    )
    
    # 사이트 설정 찾기
    site_config = None
    for key, config in Config.TARGET_SITES.items():
        if config["site_name"] == site_name:
            site_config = config
            break
    
    if not site_config:
        print(f"사이트 설정을 찾을 수 없습니다: {site_name}")
        return
    
    # Scraper 초기화
    scraper = Scraper(
        base_url=site_config["base_url"],
        list_url=site_config["list_url"],
        selectors=site_config["selectors"],
        user_agent=Config.USER_AGENTS[0],
        use_playwright=site_config.get("use_playwright", False),
    )
    
    # 게시글 파싱
    try:
        post_data = scraper.parse_post(source_url, max_retries=3)
        if not post_data:
            print("게시글 파싱 실패")
            return
        
        print(f"\n이미지 {len(post_data['images'])}개 추출:")
        for idx, img_url in enumerate(post_data['images'], 1):
            print(f"  {idx}. {img_url[:80]}...")
        
        # 사이트 이름 추가
        post_data["site_name"] = site_name
        
        # 게시글 저장
        new_post_id = db.save_post_with_html(post_data, post_data["images"])
        
        if new_post_id:
            print(f"\n✅ 재크롤링 완료! 새 게시물 ID: {new_post_id}")
            
            # 저장된 이미지 확인
            with engine.connect() as conn:
                result = conn.execute(text("""
                    SELECT COUNT(*) as cnt
                    FROM images
                    WHERE post_id = :post_id
                """), {"post_id": new_post_id})
                image_count = result.fetchone()[0]
                print(f"저장된 이미지: {image_count}개")
        else:
            print("게시글 저장 실패 (중복?)")
    
    except Exception as e:
        print(f"오류 발생: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        post_id = int(sys.argv[1])
    else:
        post_id = 3  # 기본값
    
    recrawl_post(post_id)
