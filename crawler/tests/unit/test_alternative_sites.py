"""
Test alternative humor sites with Playwright
"""
from playwright.sync_api import sync_playwright
import time

sites = {
    "todayhumor": "http://www.todayhumor.co.kr/board/list.php?table=bestofbest",
    "ppomppu": "https://www.ppomppu.co.kr/zboard/zboard.php?id=humor",
}

def test_site(name, url):
    print(f"\n{'='*80}")
    print(f"Testing: {name.upper()}")
    print(f"URL: {url}")
    print('='*80)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_extra_http_headers({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        try:
            page.goto(url, wait_until='domcontentloaded', timeout=15000)
            print(f"✓ Page loaded")
            print(f"Title: {page.title()}\n")
            
            time.sleep(1)
            
            # Try common selectors
            selectors_to_try = [
                'table tbody tr',
                'table tr',
                'div.list tr',
                'a[href*="read"]',
                'a[href*="view"]',
                'td.subject a',
            ]
            
            for selector in selectors_to_try:
                count = page.locator(selector).count()
                if count > 5:
                    print(f"✓ Found {count} items: {selector}")
                    
                    first = page.locator(selector).first
                    if first:
                        try:
                            text = first.text_content()
                            if text and len(text.strip()) > 0:
                                print(f"  Text: {text.strip()[:60]}")
                        except:
                            pass
                    print()
            
        except Exception as e:
            print(f"❌ Error: {str(e)[:200]}")
        
        finally:
            browser.close()

for name, url in sites.items():
    test_site(name, url)
    time.sleep(2)

print("\n" + "="*80)
print("Complete!")
