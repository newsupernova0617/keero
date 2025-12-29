#!/usr/bin/env python3
"""
사이트별 selector 검증 스크립트

각 사이트의 목록 페이지와 개별 게시글 페이지에서
selector가 올바르게 작동하는지 확인합니다.
"""

import sys
import requests
from bs4 import BeautifulSoup
from core.config import Config

def test_site_selectors(site_key):
    """특정 사이트의 selector 테스트"""
    if site_key not in Config.TARGET_SITES:
        print(f"❌ Site '{site_key}' not found in config")
        return False
    
    site_config = Config.TARGET_SITES[site_key]
    
    if not site_config.get("enabled", True):
        print(f"⚠️  Site '{site_key}' is disabled")
        return False
    
    print(f"\n{'='*80}")
    print(f"Testing: {site_key}")
    print(f"{'='*80}")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    # 1. 목록 페이지 테스트
    print(f"\n📋 List Page: {site_config['list_url']}")
    print("-" * 80)
    
    try:
        response = requests.get(site_config['list_url'], headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 게시글 목록 찾기
        post_items = soup.select(site_config['selectors']['post_list'])
        print(f"✓ Found {len(post_items)} post items with selector: {site_config['selectors']['post_list']}")
        
        # 첫 3개 게시글 링크 추출
        urls = []
        for i, item in enumerate(post_items[:5]):
            link = item.select_one(site_config['selectors']['post_link'])
            if link and link.get('href'):
                from urllib.parse import urljoin
                url = urljoin(site_config['base_url'], link['href'])
                title_preview = link.get_text(strip=True)[:50]
                urls.append(url)
                print(f"  {i+1}. {title_preview}")
            else:
                print(f"  {i+1}. ❌ No link found")
        
        if not urls:
            print("❌ No valid URLs found in list page")
            return False
        
        # 2. 개별 게시글 페이지 테스트 (첫 번째 게시글만)
        print(f"\n📄 Individual Post Page:")
        print("-" * 80)
        print(f"URL: {urls[0][:80]}...")
        
        response = requests.get(urls[0], headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 제목 추출
        title_elem = soup.select_one(site_config['selectors']['title'])
        if title_elem:
            title = title_elem.get_text(strip=True)
            print(f"✓ Title: {title[:60]}")
            
            # 중요: 같은 selector로 여러 개가 매칭되는지 확인
            all_titles = soup.select(site_config['selectors']['title'])
            if len(all_titles) > 1:
                print(f"⚠️  WARNING: Title selector matches {len(all_titles)} elements!")
                print(f"   This may cause all posts to have the same title.")
                print(f"   First 3 matches:")
                for i, elem in enumerate(all_titles[:3]):
                    print(f"     {i+1}. {elem.get_text(strip=True)[:50]}")
        else:
            print(f"❌ Title not found with selector: {site_config['selectors']['title']}")
        
        # 본문 추출
        content_elem = soup.select_one(site_config['selectors']['content'])
        if content_elem:
            content = content_elem.get_text(strip=True)
            print(f"✓ Content: {len(content)} chars, preview: {content[:60]}...")
        else:
            print(f"❌ Content not found with selector: {site_config['selectors']['content']}")
        
        # 이미지 추출
        images = soup.select(site_config['selectors']['images'])
        print(f"✓ Images: {len(images)} found")
        
        print(f"\n{'='*80}")
        print(f"✅ {site_key} selector test completed")
        print(f"{'='*80}\n")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing {site_key}: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # 특정 사이트만 테스트
        site_key = sys.argv[1]
        test_site_selectors(site_key)
    else:
        # 모든 활성화된 사이트 테스트
        print("Testing all enabled sites...")
        for site_key, site_config in Config.TARGET_SITES.items():
            if site_config.get("enabled", True) and not site_config.get("use_playwright", False):
                test_site_selectors(site_key)
                print("\n" + "="*80 + "\n")
