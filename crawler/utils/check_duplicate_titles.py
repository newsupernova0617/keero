#!/usr/bin/env python3
"""
데이터베이스에서 사이트별 중복 제목 체크

각 사이트에서 크롤링된 게시글들의 제목이 중복되는지 확인하여
selector 문제를 감지합니다.
"""

import sqlite3
import sys
from collections import Counter

def check_duplicate_titles(db_path="../data/posts.db", site_name=None):
    """사이트별 중복 제목 확인"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    if site_name:
        # 특정 사이트만 확인
        sites = [site_name]
    else:
        # 모든 사이트 확인
        cursor.execute("SELECT DISTINCT site_name FROM posts")
        sites = [row[0] for row in cursor.fetchall()]
    
    print("="*80)
    print("Checking for duplicate titles (potential selector issues)")
    print("="*80)
    
    for site in sites:
        cursor.execute("""
            SELECT title, COUNT(*) as count
            FROM posts
            WHERE site_name = ?
            GROUP BY title
            ORDER BY count DESC
            LIMIT 10
        """, (site,))
        
        results = cursor.fetchall()
        
        if not results:
            print(f"\n{site}: No posts found")
            continue
        
        # 전체 게시글 수
        cursor.execute("SELECT COUNT(*) FROM posts WHERE site_name = ?", (site,))
        total_posts = cursor.fetchone()[0]
        
        print(f"\n{site}: {total_posts} total posts")
        print("-" * 80)
        
        # 중복이 많은 제목 확인
        has_issue = False
        for title, count in results:
            if count > 5:  # 같은 제목이 5개 이상이면 문제
                print(f"  ⚠️  '{title[:50]}...' appears {count} times")
                has_issue = True
            elif count > 1:
                print(f"  ℹ️  '{title[:50]}...' appears {count} times")
        
        if not has_issue and results[0][1] == 1:
            print(f"  ✅ All titles are unique - selectors look good!")
        
        # 최근 5개 게시글 제목 확인
        cursor.execute("""
            SELECT id, title
            FROM posts
            WHERE site_name = ?
            ORDER BY crawled_at DESC
            LIMIT 5
        """, (site,))
        
        recent_posts = cursor.fetchall()
        print(f"\n  Recent posts:")
        for post_id, title in recent_posts:
            print(f"    {post_id}. {title[:60]}")
    
    conn.close()
    print("\n" + "="*80)

if __name__ == "__main__":
    site = sys.argv[1] if len(sys.argv) > 1 else None
    check_duplicate_titles(site_name=site)
