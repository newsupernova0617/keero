"""
이미지 URL 추출 디버깅 스크립트
"""

import requests
from bs4 import BeautifulSoup

# 문제의 게시물 URL
url = "https://www.fmkorea.com/best/9310676594"

# HTML 다운로드
response = requests.get(url, headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
})
soup = BeautifulSoup(response.text, "lxml")

# 본문 영역 찾기
content_elem = soup.select_one("div.rd_body.clear")

if content_elem:
    print("=" * 80)
    print("본문 영역에서 이미지 태그 찾기")
    print("=" * 80)
    
    images = content_elem.find_all('img')
    print(f"\n총 {len(images)}개의 이미지 태그 발견\n")
    
    for idx, img in enumerate(images, 1):
        src = img.get('src', '')
        data_original = img.get('data-original', '')
        
        print(f"[이미지 {idx}]")
        print(f"  src: {src}")
        print(f"  data-original: {data_original}")
        
        # 현재 로직에서 어떤 URL을 선택하는지
        selected = data_original or src
        print(f"  → 선택된 URL: {selected}")
        
        # transparent.gif 체크
        if 'transparent.gif' in selected:
            print(f"  ⚠️  WARNING: transparent.gif가 선택됨!")
        
        print()
