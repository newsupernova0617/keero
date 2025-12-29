"""
Test MLBPark structure
"""
import requests
from bs4 import BeautifulSoup

url = 'https://www.mlbpark.com/park/list.php?m=search&p=1&b=bullpen&select=stt&query=1'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

print(f"Testing: MLBPark")
print(f"URL: {url}\n")

try:
    r = requests.get(url, headers=headers, timeout=10)
    print(f"Status: {r.status_code}")
    
    soup = BeautifulSoup(r.content, 'lxml')
    print(f"Title: {soup.title.string if soup.title else 'No title'}\n")
    
    # Test selectors
    selectors = [
        ('table.tbl_type01 tbody tr', 'Original selector'),
        ('table tbody tr', 'Simple table rows'),
        ('div.ar_lst tbody tr', 'ar_lst table'),
        ('article', 'Article tags'),
    ]
    
    for selector, desc in selectors:
        elements = soup.select(selector)
        if elements:
            print(f"✓ {desc}: {selector}")
            print(f"  Found: {len(elements)} items")
            
            if elements:
                first = elements[0]
                # Try to find link
                link = first.select_one('a')
                if link:
                    print(f"  First link: {link.get('href', 'No href')[:80]}")
                    print(f"  First text: {link.get_text(strip=True)[:50]}")
                print()
        else:
            print(f"✗ {desc}: Not found\n")
    
    # Show page structure
    print("=== Page structure sample ===")
    main = soup.select_one('body')
    if main:
        for i, child in enumerate(list(main.children)[:15]):
            if hasattr(child, 'name') and child.name:
                classes = ' '.join(child.get('class', []))
                print(f"{i}: <{child.name}> class='{classes}'")

except Exception as e:
    print(f"❌ Error: {str(e)}")
