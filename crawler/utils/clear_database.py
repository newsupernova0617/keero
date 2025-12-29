"""
데이터베이스 초기화 스크립트 - 모든 게시물과 이미지 삭제
"""

import sqlite3
from pathlib import Path

db_path = Path(__file__).parent.parent / "data" / "posts.db"

if not db_path.exists():
    print(f"데이터베이스가 없습니다: {db_path}")
    exit(1)

conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

try:
    # 이미지 삭제
    cursor.execute("DELETE FROM images")
    images_deleted = cursor.rowcount
    
    # 게시물 삭제
    cursor.execute("DELETE FROM posts")
    posts_deleted = cursor.rowcount
    
    # FTS 테이블 초기화
    cursor.execute("DELETE FROM posts_fts")
    
    conn.commit()
    
    print(f"✅ 데이터베이스 초기화 완료!")
    print(f"   - 삭제된 게시물: {posts_deleted}개")
    print(f"   - 삭제된 이미지: {images_deleted}개")
    
except Exception as e:
    conn.rollback()
    print(f"❌ 오류 발생: {e}")
    raise
finally:
    conn.close()

print("\n이제 크롤러를 실행하여 새 데이터를 수집하세요:")
print("  cd crawler")
print("  python main.py")
