"""
Test Humoruniv structure
"""
import requests
from bs4 import BeautifulSoup

url = 'https://www.humoruniv.com/board/humor/list.html?table=pds'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

print(f"Testing: Humoruniv")
print(f"URL: {url}\n")

try:
    r = requests.get(url, headers=headers, timeout=10)
    print(f"Status: {r.status_code}")
    
    soup = BeautifulSoup(r.content, 'lxml')
    print(f"Title: {soup.title.string if soup.title else 'No title'}\n")
    
    # Test selectors
    selectors = [
        ('table.bd_list tbody tr', 'Original selector'),
        ('table tbody tr', 'Simple table rows'),
        ('div.listbox tbody tr', 'listbox table'),
        ('a.subject', 'subject links'),
    ]
    
    for selector, desc in selectors:
        elements = soup.select(selector)
        if elements:
            print(f"✓ {desc}: {selector}")
            print(f"  Found: {len(elements)} items")
            
            if elements:
                first = elements[0]
                link = first.select_one('a') if first.name != 'a' else first
                if link:
                    print(f"  First link: {link.get('href', 'No href')[:80]}")
                    print(f"  First text: {link.get_text(strip=True)[:50]}")
                print()
        else:
            print(f"✗ {desc}: Not found\n")

except Exception as e:
    print(f"❌ Error: {str(e)}")
