"""
실제 크롤러 로직 시뮬레이션
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# 문제의 게시물 URL
url = "https://www.fmkorea.com/best/9310676594"
base_url = "https://www.fmkorea.com"

# HTML 다운로드
response = requests.get(url, headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
})
soup = BeautifulSoup(response.text, "lxml")

# 본문 영역 찾기
content_elem = soup.select_one("div.rd_body.clear")

print("=" * 80)
print("extract_images() 시뮬레이션 (원본 soup 사용)")
print("=" * 80)

# extract_images 로직
images_selector = "div.rd_body.clear img"
img_elements = soup.select(images_selector)

print(f"총 {len(img_elements)}개의 이미지 태그 발견\n")

extracted_urls = []
for idx, img in enumerate(img_elements, 1):
    # Lazy loading 이미지 처리: data-original 우선 확인
    src = img.get("data-original") or img.get("src")
    if src:
        # 상대 경로를 절대 경로로 변환
        absolute_url = urljoin(base_url, src)
        
        # UI 버튼/아이콘 이미지 필터링
        if '/images/' in absolute_url:
            print(f"  [{idx}] SKIP (/images/): {absolute_url}")
            continue
        
        # Lazy loading placeholder 제외
        if 'transparent.gif' in absolute_url or 'placeholder' in absolute_url.lower():
            print(f"  [{idx}] SKIP (placeholder): {absolute_url}")
            continue
        
        print(f"  [{idx}] ✅ EXTRACTED: {absolute_url}")
        extracted_urls.append(absolute_url)

print(f"\n최종 추출된 이미지: {len(extracted_urls)}개")
