"""
데이터베이스 마이그레이션: content_html 컬럼 추가

이 스크립트는 posts.db의 posts 테이블에 content_html 컬럼을 추가합니다.
"""
import sqlite3

def migrate_add_content_html():
    # posts.db 경로로 변경
    db_path = r"c:\Users\yj437\OneDrive\Desktop\coding_windows\aagag_clone\data\posts.db"
    
    print("Connecting to posts.db...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if column already exists
        cursor.execute("PRAGMA table_info(posts)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'content_html' in columns:
            print("✅ content_html column already exists!")
            return
        
        print("Adding content_html column to posts table...")
        cursor.execute("ALTER TABLE posts ADD COLUMN content_html TEXT")
        conn.commit()
        
        print("✅ Successfully added content_html column!")
        
        # Verify the change
        cursor.execute("PRAGMA table_info(posts)")
        columns_after = cursor.fetchall()
        print("\nUpdated posts table schema:")
        print("-" * 80)
        for col in columns_after:
            print(f"{col[1]:20s} {col[2]:15s}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_add_content_html()
