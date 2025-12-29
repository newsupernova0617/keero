"""
Playwright로 Clien, Dogdrip, Humoruniv의 정확한 셀렉터 찾기
"""
from playwright.sync_api import sync_playwright
import time

sites = {
    "clien": {
        "url": "https://www.clien.net/service/board/park",
        "note": "humor 대신 park(자유게시판) 시도"
    },
    "dogdrip": {
        "url": "https://www.dogdrip.net/index.php?mid=dogdrip",
        "note": "개드립 일반 게시판"
    },
    "humoruniv": {
        "url": "https://web.humoruniv.com/board/humor/list.html?table=pds",
        "note": "웃긴대학 일반 게시판"
    },
}

def analyze_site(name, config):
    print(f"\n{'='*80}")
    print(f"🔍 Analyzing: {name.upper()}")
    print(f"URL: {config['url']}")
    print(f"Note: {config['note']}")
    print('='*80)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        page = context.new_page()
        
        try:
            print("⏳ Loading page...")
            page.goto(config['url'], wait_until='domcontentloaded', timeout=30000)
            time.sleep(3)  # Wait for dynamic content
            
            print(f"✓ Page loaded: {page.title()}\n")
            
            # Try to find post list
            selectors_to_try = [
                ('article', 'article tags'),
                ('div.list_item', 'list_item divs'),
                ('div.post_item', 'post_item divs'),
                ('tr', 'table rows'),
                ('li.item', 'list items'),
                ('div[class*="item"]', 'any item divs'),
                ('div[class*="post"]', 'any post divs'),
            ]
            
            best_selector = None
            best_count = 0
            
            for selector, desc in selectors_to_try:
                try:
                    count = page.locator(selector).count()
                    if count > 10:  # Need at least 10 items
                        print(f"✓ {desc}: {selector} -> {count} items")
                        
                        if count > best_count:
                            best_count = count
                            best_selector = selector
                            
                            # Get sample
                            first = page.locator(selector).first
                            text = first.text_content()
                            if text:
                                print(f"  Sample: {text.strip()[:80]}")
                except:
                    pass
            
            if best_selector:
                print(f"\n🎯 Best selector: {best_selector} ({best_count} items)")
                
                # Try to find links in the best selector
                try:
                    first_item = page.locator(best_selector).first
                    links = first_item.locator('a').all()
                    
                    if links:
                        print(f"   Links found in item: {len(links)}")
                        for i, link in enumerate(links[:3]):
                            href = link.get_attribute('href')
                            text = link.text_content()
                            if href and text:
                                print(f"   Link {i+1}: {text.strip()[:40]} -> {href[:60]}")
                except:
                    pass
                
                # Suggest selectors
                print(f"\n📝 Suggested config:")
                print(f'   "post_list": "{best_selector}",')
                
                # Try to find the best link selector
                try:
                    sample_link = page.locator(f'{best_selector} a').first
                    if sample_link:
                        link_class = sample_link.get_attribute('class')
                        if link_class:
                            print(f'   "post_link": "a.{link_class.split()[0]}",')
                        else:
                            print(f'   "post_link": "a",')
                except:
                    print(f'   "post_link": "a",')
            else:
                print("\n❌ No suitable selector found")
                print("   Trying to capture page structure...")
                
                # Get body HTML to analyze
                body_html = page.locator('body').inner_html()[:2000]
                print(f"\n   First 2000 chars of body:")
                for line in body_html.split('\n')[:30]:
                    if line.strip():
                        print(f"   {line.strip()[:100]}")
            
        except Exception as e:
            print(f"❌ Error: {str(e)[:200]}")
        
        finally:
            browser.close()
            time.sleep(2)

# Analyze each site
for name, config in sites.items():
    analyze_site(name, config)

print("\n" + "="*80)
print("✅ Analysis complete!")
