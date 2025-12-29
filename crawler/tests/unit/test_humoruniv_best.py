"""Test Humoruniv best board with query params"""
import requests
from bs4 import BeautifulSoup

url = 'https://humoruniv.com/board/humor/list.html?table=humorbest&st=year&year=2024'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

print(f"Testing: {url}\n")

try:
    r = requests.get(url, headers=headers, timeout=10)
    print(f"Status: {r.status_code}")
    
    soup = BeautifulSoup(r.content, 'lxml')
    print(f"Title: {soup.title.string if soup.title else 'No title'}")
    
    # Find post links
    links = soup.select('a[href*="read"]')
    print(f"Found {len(links)} post links")
    
    if links:
        print("\nFirst 3 posts:")
        for i, link in enumerate(links[:3], 1):
            print(f"  {i}. {link.get_text(strip=True)[:50]}")
            print(f"     {link.get('href', 'No href')}")
        print("\n✅ SUCCESS! This URL works!")
    else:
        print("\n⚠️ No posts found")
        
except Exception as e:
    print(f"❌ Error: {str(e)}")
