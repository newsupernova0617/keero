"""
Check Ruliweb /best/humor page structure
"""
import requests
from bs4 import BeautifulSoup

url = 'https://bbs.ruliweb.com/best/humor'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

print(f"Fetching {url}...")
r = requests.get(url, headers=headers, timeout=10)
print(f"Status: {r.status_code}")

soup = BeautifulSoup(r.content, 'lxml')
print(f"Title: {soup.title.string if soup.title else 'No title'}")

# Find post list container
print("\n=== Looking for post list ===")
post_containers = [
    'div.best_body',
    'div.best_list',
    'table.board_list_table',
    'div.list_best',
    'ul.list_best',
    'div.board_main'
]

for selector in post_containers:
    elements = soup.select(selector)
    if elements:
        print(f"✓ Found: {selector} ({len(elements)} elements)")
    else:
        print(f"✗ Not found: {selector}")

# Find post links
print("\n=== Looking for post links ===")
link_selectors = [
    'a.subject_link',
    'a.deco',
    'a.subject',
    'div.subject a',
    'td.subject a',
    'a[href*="read"]'
]

for selector in link_selectors:
    links = soup.select(selector)
    if links:
        print(f"✓ Found: {selector} ({len(links)} links)")
        if links:
            print(f"  First link: {links[0].get('href', 'No href')[:80]}")
            print(f"  First text: {links[0].get_text(strip=True)[:50]}")
    else:
        print(f"✗ Not found: {selector}")

# Check structure
print("\n=== Page structure sample ===")
main_content = soup.select_one('div.best_body, div.board_main, body')
if main_content:
    # Get first few elements
    for i, child in enumerate(list(main_content.children)[:10]):
        if hasattr(child, 'name') and child.name:
            classes = child.get('class', [])
            print(f"{i}: <{child.name}> class={classes}")
