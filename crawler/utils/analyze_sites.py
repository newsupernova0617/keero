"""
Test multiple community sites structure
"""
import requests
from bs4 import BeautifulSoup
import time

sites = {
    "fmkorea": "https://www.fmkorea.com/best",
    "mlbpark": "https://www.mlbpark.com/park",
    "clien": "https://www.clien.net/service/board/humor",
    "humoruniv": "https://www.humoruniv.com",
    "dogdrip": "https://www.dogdrip.net",
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

for site_name, url in sites.items():
    print(f"\n{'='*80}")
    print(f"Testing: {site_name.upper()} - {url}")
    print('='*80)
    
    try:
        r = requests.get(url, headers=headers, timeout=10)
        print(f"Status: {r.status_code}")
        
        if r.status_code != 200:
            print(f"  ⚠️ Failed to fetch")
            continue
        
        soup = BeautifulSoup(r.content, 'lxml')
        print(f"Title: {soup.title.string if soup.title else 'No title'}")
        
        # Try common selectors
        selectors_to_try = [
            ('article', 'article'),
            ('li.li', 'li.li'),
            ('tr.table_body', 'tr.table_body'),
            ('div.post', 'div.post'),
            ('div.list_content', 'div.list_content'),
            ('table.board_list tbody tr', 'table rows'),
        ]
        
        for selector, desc in selectors_to_try:
            elements = soup.select(selector)
            if elements and len(elements) > 5:  # At least 5 posts
                print(f"  ✓ Found {len(elements)} items with: {selector}")
                
                # Find links in first element
                first = elements[0]
                links = first.select('a')
                if links:
                    href = links[0].get('href', '')
                    text = links[0].get_text(strip=True)[:40]
                    print(f"    First link: {href}")
                    print(f"    First text: {text}...")
                break
        
        time.sleep(1)  # Be nice to servers
        
    except Exception as e:
        print(f"  ❌ Error: {str(e)[:100]}")

print("\n" + "="*80)
print("Analysis complete!")
