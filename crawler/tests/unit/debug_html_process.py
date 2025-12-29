"""
HTML 처리 과정 디버깅 스크립트
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

print("=" * 80)
print("1단계: 원본 HTML에서 이미지 추출 (scraper.py의 extract_images)")
print("=" * 80)

images_from_extract = []
for img in content_elem.find_all('img'):
    src = img.get("data-original") or img.get("src")
    if src:
        # /images/ 필터링
        if '/images/' in src:
            continue
        # transparent.gif 필터링
        if 'transparent.gif' in src or 'placeholder' in src.lower():
            continue
        images_from_extract.append(src)

print(f"추출된 이미지 URL: {len(images_from_extract)}개")
for idx, url in enumerate(images_from_extract, 1):
    print(f"  {idx}. {url}")

print("\n" + "=" * 80)
print("2단계: clean_html() 후 HTML 상태")
print("=" * 80)

# clean_html 시뮬레이션
html_str = str(content_elem)
soup2 = BeautifulSoup(html_str, "lxml")

# Lazy loading 처리 (data-original -> src 복사)
for img in soup2.find_all('img'):
    data_original = img.get('data-original')
    src = img.get('src', '')
    if data_original and ('transparent.gif' in src or 'placeholder' in src.lower() or not src):
        img['src'] = data_original

# 속성 정리
allowed_attrs = ['src', 'href', 'alt', 'title', 'controls', 'autoplay', 'loop', 'muted', 'playsinline']
for tag in soup2.find_all(True):
    tag.attrs = {k: v for k, v in tag.attrs.items() if k in allowed_attrs}

print("clean_html() 후 이미지 태그:")
for idx, img in enumerate(soup2.find_all('img'), 1):
    src = img.get('src', '')
    data_original = img.get('data-original', '')
    print(f"  [{idx}] src={src[:80]}... data-original={data_original}")

print("\n" + "=" * 80)
print("3단계: replace_image_urls_in_html()에서 매핑 시도")
print("=" * 80)

# 이미지 매핑 생성 (가상)
image_mapping = {}
for img_url in images_from_extract:
    # 정규화
    normalized = img_url.replace('https://', '').replace('http://', '').replace('//', '')
    image_mapping[normalized] = f"https://r2.dev/images/{hash(img_url)}.webp"

print(f"매핑 테이블: {len(image_mapping)}개")

# replace_image_urls_in_html 시뮬레이션
def normalize_url(url):
    if url.startswith('//'):
        url = 'https:' + url
    return url.replace('https://', '').replace('http://', '')

# 정규화된 매핑
normalized_mapping = {}
for original_url, r2_url in image_mapping.items():
    normalized_key = normalize_url(original_url)
    normalized_mapping[normalized_key] = r2_url

matched = 0
unmatched = 0

for img in soup2.find_all('img'):
    # 여기가 문제! data-original이 이미 삭제됨
    original_src = img.get('data-original') or img.get('src')
    if original_src:
        normalized_src = normalize_url(original_src)
        if normalized_src in normalized_mapping:
            matched += 1
            print(f"  ✅ 매칭: {original_src[:60]}...")
        else:
            unmatched += 1
            print(f"  ❌ 미매칭: {original_src[:60]}...")

print(f"\n매칭 결과: {matched}개 성공, {unmatched}개 실패")
