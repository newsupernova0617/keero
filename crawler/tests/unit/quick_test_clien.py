"""
간단한 Playwright 테스트 - Clien만
"""
from playwright.sync_api import sync_playwright
import time

url = "https://www.clien.net/service/board/park"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.set_extra_http_headers({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    
    print(f"Testing: {url}\n")
    page.goto(url, wait_until='domcontentloaded', timeout=15000)
    time.sleep(2)
    
    print(f"Title: {page.title()}\n")
    
    # Test selectors
    selectors = {
        'div.list_item': 'list_item divs',
        'div.list_content': 'list_content div',
        'a.list_subject': 'list_subject links',
    }
    
    for selector, desc in selectors.items():
        count = page.locator(selector).count()
        print(f"{desc}: {selector} -> {count} items")
        
        if count > 0:
            first = page.locator(selector).first
            text = first.text_content()
            if text:
                print(f"  Sample: {text.strip()[:60]}\n")
    
    browser.close()
    print("✅ Done!")
