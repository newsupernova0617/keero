import sqlite3
from pathlib import Path

# 프로젝트 루트 기준 상대 경로
db_path = Path(__file__).parent.parent / "data" / "posts.db"
conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

# Check if any posts have content_html
cursor.execute("SELECT id, title, LENGTH(content_html) as html_len FROM posts WHERE content_html IS NOT NULL LIMIT 5")
posts_with_html = cursor.fetchall()

print("Posts with content_html:")
print("-" * 80)
if posts_with_html:
    for post_id, title, html_len in posts_with_html:
        print(f"ID {post_id}: {title[:50]}... (HTML length: {html_len})")
else:
    print("❌ No posts have content_html!")

print("\n" + "=" * 80 + "\n")

# Check total posts
cursor.execute("SELECT COUNT(*) FROM posts")
total_posts = cursor.fetchone()[0]
print(f"Total posts: {total_posts}")

# Check posts without content_html
cursor.execute("SELECT COUNT(*) FROM posts WHERE content_html IS NULL OR content_html = ''")
posts_without_html = cursor.fetchone()[0]
print(f"Posts without content_html: {posts_without_html}")

conn.close()
