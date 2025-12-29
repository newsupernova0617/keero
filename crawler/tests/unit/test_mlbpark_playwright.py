"""
MLBPark Playwright 테스트
"""
from playwright.sync_api import sync_playwright
import time

url = "https://www.mlbpark.com/park"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.set_extra_http_headers({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    
    print(f"Testing MLBPark: {url}\n")
    
    try:
        page.goto(url, wait_until='domcontentloaded', timeout=30000)
        time.sleep(3)  # 추가 대기
        
        print(f"✓ Page loaded")
        print(f"Title: {page.title()}\n")
        
        # Test selectors
        selectors = {
            'table tbody tr': 'table rows',
            'table tr': 'all table rows',
            'div.article-list tr': 'article-list rows',
            'a.txt': 'txt links',
            'a[href*="view"]': 'view links',
        }
        
        for selector, desc in selectors.items():
            count = page.locator(selector).count()
            if count > 5:
                print(f"✓ {desc}: {selector} -> {count} items")
                first = page.locator(selector).first
                text = first.text_content()
                if text and len(text.strip()) > 0:
                    print(f"  Sample: {text.strip()[:60]}\n")
        
        browser.close()
        print("✅ Done!")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        browser.close()
