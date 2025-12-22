"""
기존 이미지 URL을 공개 URL로 업데이트하는 마이그레이션 스크립트

사용법:
    python migrate_image_urls.py <OLD_URL_PREFIX> <NEW_URL_PREFIX>

예시:
    python migrate_image_urls.py "https://pub-d633a7c3cd0cd71ea3144f17896d4e65.r2.dev" "https://pub-xxxxx.r2.dev"
"""

import sys
import sqlite3
from pathlib import Path


def migrate_image_urls(db_path: str, old_prefix: str, new_prefix: str):
    """이미지 URL을 업데이트"""
    
    # 슬래시 정규화
    old_prefix = old_prefix.rstrip("/")
    new_prefix = new_prefix.rstrip("/")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # 현재 이미지 개수 확인
        cursor.execute("SELECT COUNT(*) FROM images")
        total_images = cursor.fetchone()[0]
        print(f"총 {total_images}개의 이미지가 있습니다.")
        
        # 업데이트할 이미지 개수 확인
        cursor.execute(
            "SELECT COUNT(*) FROM images WHERE r2_url LIKE ?",
            (f"{old_prefix}%",)
        )
        to_update = cursor.fetchone()[0]
        print(f"업데이트할 이미지: {to_update}개")
        
        if to_update == 0:
            print("업데이트할 이미지가 없습니다.")
            return
        
        # 확인 요청
        response = input(f"\n{to_update}개의 이미지 URL을 업데이트하시겠습니까? (y/N): ")
        if response.lower() != 'y':
            print("취소되었습니다.")
            return
        
        # URL 업데이트
        cursor.execute("""
            UPDATE images 
            SET r2_url = REPLACE(r2_url, ?, ?)
            WHERE r2_url LIKE ?
        """, (old_prefix, new_prefix, f"{old_prefix}%"))
        
        conn.commit()
        updated = cursor.rowcount
        print(f"\n✅ {updated}개의 이미지 URL이 업데이트되었습니다!")
        
        # 샘플 확인
        cursor.execute("SELECT r2_url FROM images LIMIT 3")
        samples = cursor.fetchall()
        print("\n업데이트된 URL 샘플:")
        for url, in samples:
            print(f"  - {url}")
            
    except Exception as e:
        conn.rollback()
        print(f"❌ 오류 발생: {e}")
        raise
    finally:
        conn.close()


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        print("\n❌ 사용법이 올바르지 않습니다.")
        print("예시: python migrate_image_urls.py 'OLD_URL' 'NEW_URL'")
        sys.exit(1)
    
    old_prefix = sys.argv[1]
    new_prefix = sys.argv[2]
    
    # 데이터베이스 경로
    db_path = Path(__file__).parent.parent / "data" / "posts.db"
    
    if not db_path.exists():
        print(f"❌ 데이터베이스를 찾을 수 없습니다: {db_path}")
        sys.exit(1)
    
    print(f"데이터베이스: {db_path}")
    print(f"이전 URL: {old_prefix}")
    print(f"새 URL: {new_prefix}")
    print("-" * 60)
    
    migrate_image_urls(str(db_path), old_prefix, new_prefix)


if __name__ == "__main__":
    main()
