
import asyncio
from core.scraper import Scraper
from core.storage import DatabaseManager
from core.config import Config

# 특정 URL 테스트용 스크립트
TARGET_URL = "https://www.fmkorea.com/best/9310073329"

async def test_single_crawl():
    print(f"Testing single crawl for: {TARGET_URL}")
    
    db_manager = DatabaseManager(Config.DATABASE['path'], Config.R2_CONFIG)
    
    site_config = Config.TARGET_SITES['fmkorea']
    
    scraper = Scraper(
        base_url=site_config['base_url'],
        selectors=site_config['selectors'],
        list_url=site_config['list_url']
    )
    
    print("Scraper initialized. Fetching and parsing post...")
    
    try:
        post_data = scraper.parse_post(TARGET_URL)
        
        if post_data:
            # site_name 필드 추가
            post_data['site_name'] = 'fmkorea'
            
            print(f"Successfully parsed post: {post_data['title']}")
            print(f"Saving to DB and uploading images...")
            
            image_urls = post_data.get('images', [])
            
            db_manager.save_post_with_html(post_data, image_urls)
            print("Saved to DB.")
            
            import sqlite3
            conn = sqlite3.connect(Config.DATABASE['path'])
            cursor = conn.cursor()
            cursor.execute('SELECT content_html FROM posts WHERE source_url=?', (TARGET_URL,))
            row = cursor.fetchone()
            conn.close()
            
            if row:
                final_html = row[0]
                html_path = '/tmp/test_single_result.html'
                with open(html_path, 'w', encoding='utf-8') as f:
                    f.write(final_html.replace('><', '>\n<'))
                print(f"Full HTML saved to {html_path}")
            else:
                print("Error: Could not find saved post in DB")
            
        else:
            print("Failed to parse post (scraper returned None)")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_single_crawl())
