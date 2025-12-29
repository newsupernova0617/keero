"""
Humoruniv 테스트
"""
from playwright.sync_api import sync_playwright
import time

url = "https://web.humoruniv.com/board/humor/list.html?table=pds"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.set_extra_http_headers({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    
    print(f"Testing Humoruniv: {url}\n")
    page.goto(url, wait_until='domcontentloaded', timeout=15000)
    time.sleep(2)
    
    print(f"Title: {page.title()}\n")
    
    # Test selectors
    selectors = {
        'table tr': 'table rows',
        'div.board_list tr': 'board_list rows',
        'li.list': 'list items',
        'a.subject': 'subject links',
        'a[href*="read"]': 'read links',
    }
    
    for selector, desc in selectors.items():
        count = page.locator(selector).count()
        if count > 5:  # Need at least 5
            print(f"✓ {desc}: {selector} -> {count} items")
            first = page.locator(selector).first
            text = first.text_content()
            if text and len(text.strip()) > 0:
                print(f"  Sample: {text.strip()[:60]}\n")
    
    browser.close()
    print("✅ Done!")
