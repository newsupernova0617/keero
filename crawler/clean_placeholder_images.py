"""
DB에서 transparent.gif 및 placeholder 이미지 레코드 정리

이 스크립트는:
1. transparent.gif를 original_url로 가진 이미지 레코드를 찾아서 삭제
2. /images/ 경로를 가진 UI 아이콘 이미지 레코드 삭제
3. 영향받은 게시물의 content_html을 재생성 (필요시)
"""

import sys
from pathlib import Path

# 프로젝트 루트 디렉토리를 Python 경로에 추가
sys.path.insert(0, str(Path(__file__).parent))

from config import Config
from storage import DatabaseManager
from sqlalchemy import create_engine, text

def clean_placeholder_images():
    """DB에서 placeholder 이미지 정리"""
    
    # DB 연결
    engine = create_engine(f"sqlite:///{Config.DATABASE['path']}")
    
    with engine.connect() as conn:
        # 1. transparent.gif 및 placeholder 이미지 찾기
        result = conn.execute(text("""
            SELECT COUNT(*) as cnt, original_url 
            FROM images 
            WHERE original_url LIKE '%transparent.gif%' 
               OR original_url LIKE '%placeholder%'
               OR original_url LIKE '%/images/%'
            GROUP BY original_url
        """))
        
        print("=" * 80)
        print("삭제 대상 이미지:")
        print("=" * 80)
        
        total_to_delete = 0
        for row in result:
            cnt, url = row
            print(f"  {cnt}개: {url}")
            total_to_delete += cnt
        
        if total_to_delete == 0:
            print("\n삭제할 이미지가 없습니다! ✅")
            return
        
        print(f"\n총 {total_to_delete}개의 레코드를 삭제합니다.")
        
        # 사용자 확인
        response = input("\n계속하시겠습니까? (y/N): ")
        if response.lower() != 'y':
            print("취소되었습니다.")
            return
        
        # 2. 삭제 실행
        result = conn.execute(text("""
            DELETE FROM images 
            WHERE original_url LIKE '%transparent.gif%' 
               OR original_url LIKE '%placeholder%'
               OR original_url LIKE '%/images/%'
        """))
        
        deleted_count = result.rowcount
        conn.commit()
        
        print(f"\n✅ {deleted_count}개의 레코드를 삭제했습니다!")
        
        # 3. 영향받은 게시물 확인
        result = conn.execute(text("""
            SELECT COUNT(DISTINCT post_id) as post_count
            FROM images
            WHERE post_id IN (
                SELECT DISTINCT p.id 
                FROM posts p
                LEFT JOIN images i ON p.id = i.post_id
                WHERE p.content_html IS NOT NULL
                GROUP BY p.id
            )
        """))
        
        post_count = result.fetchone()[0]
        print(f"\n📊 현재 {post_count}개의 게시물에 이미지가 연결되어 있습니다.")
        
        print("\n" + "=" * 80)
        print("정리 완료!")
        print("=" * 80)
        print("\n다음 크롤링부터는 transparent.gif가 업로드되지 않습니다.")
        print("기존 게시물의 HTML은 자동으로 수정되지 않으므로,")
        print("필요시 해당 게시물을 다시 크롤링하거나 수동으로 수정해주세요.")

if __name__ == "__main__":
    clean_placeholder_images()
