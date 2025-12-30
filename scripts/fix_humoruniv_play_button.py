#!/usr/bin/env python3
"""
웃긴대학 게시글의 play_trans.png 제거 스크립트
"""

import sqlite3
from bs4 import BeautifulSoup

def clean_humoruniv_html(html: str) -> str:
    """웃긴대학 HTML에서 플레이 버튼 제거"""
    if not html:
        return html
    
    soup = BeautifulSoup(html, 'lxml')
    
    # 플레이 버튼 이미지 제거
    for img in soup.find_all('img'):
        src = img.get('src', '')
        if '/images/play_trans.png' in src or 'play_trans.png' in src:
            parent = img.parent
            if parent and parent.name == 'div':
                parent.decompose()
            else:
                img.decompose()
    
    # "MP4" 텍스트만 있는 div 제거
    for div in soup.find_all('div'):
        if div.get_text(strip=True) == 'MP4':
            div.decompose()
    
    return str(soup)

def main():
    db_path = '../data/posts.db'
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 웃긴대학 게시글 조회
    cursor.execute("""
        SELECT id, title, content_html 
        FROM posts 
        WHERE site_name = 'humoruniv' 
        AND content_html LIKE '%play_trans.png%'
    """)
    
    posts = cursor.fetchall()
    
    print(f"Found {len(posts)} humoruniv posts with play_trans.png")
    
    updated = 0
    for post_id, title, content_html in posts:
        cleaned_html = clean_humoruniv_html(content_html)
        
        cursor.execute("""
            UPDATE posts 
            SET content_html = ? 
            WHERE id = ?
        """, (cleaned_html, post_id))
        
        updated += 1
        print(f"Updated: {title[:50]}...")
    
    conn.commit()
    conn.close()
    
    print(f"\n✅ Updated {updated} posts")

if __name__ == "__main__":
    main()
