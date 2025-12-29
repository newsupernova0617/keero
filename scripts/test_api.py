#!/usr/bin/env python3
"""
SvelteKit Crawler API 테스트 스크립트
"""

import requests
import json
from datetime import datetime

# API 설정
API_URL = "http://localhost:5173"
API_KEY = "5d34f78b560d862c8875bd0a67709c13ff1c24275dd664e3767f288da29ff081"

def test_posts_api():
    """게시글 저장 API 테스트"""
    print("🧪 Testing POST /api/crawler/posts...")
    
    # 테스트 데이터
    payload = {
        "post": {
            "site_name": "test_site",
            "title": "API 테스트 게시글",
            "content": "이것은 API를 통해 저장된 테스트 게시글입니다.",
            "content_html": "<div><p>이것은 API를 통해 저장된 테스트 게시글입니다.</p></div>",
            "source_url": f"https://test.com/post/{datetime.now().timestamp()}",
            "created_at": datetime.now().isoformat()
        },
        "images": [
            {"url": "https://example.com/image1.jpg", "order_index": 0},
            {"url": "https://example.com/image2.jpg", "order_index": 1}
        ]
    }
    
    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(
            f"{API_URL}/api/crawler/posts",
            json=payload,
            headers=headers,
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        if response.status_code == 200:
            print("✅ 게시글 API 테스트 성공!")
            return True
        else:
            print("❌ 게시글 API 테스트 실패!")
            return False
            
    except Exception as e:
        print(f"❌ 에러 발생: {e}")
        return False

def test_logs_api():
    """로그 저장 API 테스트"""
    print("\n🧪 Testing POST /api/crawler/logs...")
    
    # 테스트 데이터
    payload = {
        "logs": [
            {
                "timestamp": datetime.now().isoformat(),
                "level": "INFO",
                "level_no": 20,
                "logger": "test.api",
                "message": "API 테스트 로그 메시지 1",
                "function": "test_logs_api",
                "line_number": 65,
                "exception": None,
                "extra_data": None
            },
            {
                "timestamp": datetime.now().isoformat(),
                "level": "WARNING",
                "level_no": 30,
                "logger": "test.api",
                "message": "API 테스트 경고 메시지",
                "function": "test_logs_api",
                "line_number": 75,
                "exception": None,
                "extra_data": json.dumps({"test": "data"})
            }
        ]
    }
    
    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(
            f"{API_URL}/api/crawler/logs",
            json=payload,
            headers=headers,
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        if response.status_code == 200:
            print("✅ 로그 API 테스트 성공!")
            return True
        else:
            print("❌ 로그 API 테스트 실패!")
            return False
            
    except Exception as e:
        print(f"❌ 에러 발생: {e}")
        return False

def test_unauthorized():
    """인증 실패 테스트"""
    print("\n🧪 Testing unauthorized access...")
    
    payload = {"post": {"site_name": "test", "title": "test", "source_url": "https://test.com"}}
    headers = {
        "X-API-Key": "wrong-key",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(
            f"{API_URL}/api/crawler/posts",
            json=payload,
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 401:
            print("✅ 인증 실패 테스트 성공! (401 Unauthorized)")
            return True
        else:
            print(f"❌ 예상과 다른 응답: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 에러 발생: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 SvelteKit Crawler API 테스트 시작")
    print("=" * 60)
    
    results = []
    
    # 1. 게시글 API 테스트
    results.append(test_posts_api())
    
    # 2. 로그 API 테스트
    results.append(test_logs_api())
    
    # 3. 인증 실패 테스트
    results.append(test_unauthorized())
    
    print("\n" + "=" * 60)
    print(f"📊 테스트 결과: {sum(results)}/{len(results)} 성공")
    print("=" * 60)
    
    if all(results):
        print("🎉 모든 테스트 통과!")
        exit(0)
    else:
        print("⚠️ 일부 테스트 실패")
        exit(1)
