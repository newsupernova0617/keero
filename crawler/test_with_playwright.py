"""
Use Playwright to test site structures with JavaScript rendering
"""
from playwright.sync_api import sync_playwright
import time

sites = {
    "clien": "https://www.clien.net/service/board/humor",
    "humoruniv": "https://www.humoruniv.com/board/humor/list.html?table=pds", 
    "dogdrip": "https://www.dogdrip.net/index.php?mid=dogdrip",
}

def test_site(name, url):
    print(f"\n{'='*80}")
    print(f"Testing: {name.upper()}")
    print(f"URL: {url}")
    print('='*80)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            # Navigate and wait for network idle
            page.goto(url, wait_until='networkidle', timeout=30000)
            print(f"✓ Page loaded")
            print(f"Title: {page.title()}\n")
            
            # Wait a bit for dynamic content
            time.sleep(2)
            
            # Try common selectors
            selectors_to_try = [
                'article',
                'div.list_item',
                'div.post',
                'table tbody tr',
                'li.item',
                'div.item',
                'tr',
                'a[href*="read"]',
                'a[href*="view"]',
            ]
            
            for selector in selectors_to_try:
                count = page.locator(selector).count()
                if count > 5:  # At least 5 items
                    print(f"✓ Found {count} items: {selector}")
                    
                    # Get first item details
                    first = page.locator(selector).first
                    if first:
                        try:
                            text = first.text_content()
                            if text:
                                print(f"  First text: {text.strip()[:60]}")
                            
                            # Try to find link
                            link = first.locator('a').first
                            if link:
                                href = link.get_attribute('href')
                                link_text = link.text_content()
                                print(f"  Link: {href[:80] if href else 'No href'}")
                                print(f"  Link text: {link_text.strip()[:50] if link_text else 'No text'}")
                        except:
                            pass
                    print()
            
            # Get page structure sample
            print("=== Sample HTML structure ===")
            body = page.locator('body').first
            if body:
                html = body.inner_html()
                # Print first 1000 chars
                lines = html[:1000].split('\n')
                for line in lines[:20]:
                    if line.strip():
                        print(line.strip()[:100])
            
        except Exception as e:
            print(f"❌ Error: {str(e)[:200]}")
        
        finally:
            browser.close()

# Test each site
for name, url in sites.items():
    test_site(name, url)
    time.sleep(2)  # Be nice to servers

print("\n" + "="*80)
print("Analysis complete!")
