"""
Test Ruliweb /best/humor scraping with detailed debugging
"""
import requests
from bs4 import BeautifulSoup

url = 'https://bbs.ruliweb.com/best/humor'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

print(f"Fetching {url}...")
r = requests.get(url, headers=headers, timeout=10)
print(f"Status: {r.status_code}\n")

soup = BeautifulSoup(r.content, 'lxml')

# Test selectors
print("=== Testing post_list selector ===")
selector = "table.board_list_table tbody tr"
posts = soup.select(selector)
print(f"Selector: {selector}")
print(f"Found: {len(posts)} posts")

if posts:
    print("\nFirst post structure:")
    first_post = posts[0]
    print(f"  Tag: {first_post.name}")
    print(f"  Classes: {first_post.get('class', [])}")
    
    # Find link
    link = first_post.select_one("a.subject_link")
    if link:
        print(f"  Link found: {link.get('href', 'No href')}")
        print(f"  Title: {link.get_text(strip=True)[:50]}")
    else:
        print("  ✗ No link found with a.subject_link")
        # Try other selectors
        all_links = first_post.select("a")
        print(f"  All links in post: {len(all_links)}")
        if all_links:
            print(f"    First link: {all_links[0].get('href', 'No href')}")

print("\n=== Alternative selector test ===")
# Try without tbody
selector2 = "table.board_list_table tr"
posts2 = soup.select(selector2)
print(f"Selector: {selector2}")
print(f"Found: {len(posts2)} rows")

# Filter out header rows
valid_posts = [p for p in posts2 if p.select_one("a.subject_link")]
print(f"Valid posts (with subject_link): {len(valid_posts)}")

if valid_posts:
    print("\nFirst 3 valid posts:")
    for i, post in enumerate(valid_posts[:3], 1):
        link = post.select_one("a.subject_link")
        print(f"  {i}. {link.get_text(strip=True)[:40]}...")
        print(f"     URL: {link.get('href', 'No href')}")
