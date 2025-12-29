"""
필터링 로직 테스트
"""

from urllib.parse import urljoin

base_url = "https://www.fmkorea.com"

# 테스트 URL들
test_urls = [
    "//image.fmkorea.com/files/attach/new5/20251224/9310676594_486616_1e8e59d34c2fb766a3330d8cb978c898.png",
    "//image.fmkorea.com/classes/lazy/img/transparent.gif",
]

for url in test_urls:
    absolute_url = urljoin(base_url, url)
    print(f"원본: {url}")
    print(f"절대 경로: {absolute_url}")
    
    # 필터링 체크
    if '/images/' in absolute_url:
        print("  → SKIP: /images/ 경로")
    elif 'transparent.gif' in absolute_url or 'placeholder' in absolute_url.lower():
        print("  → SKIP: placeholder")
    else:
        print("  → ✅ EXTRACTED")
    print()
