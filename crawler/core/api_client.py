"""
SvelteKit Crawler API 클라이언트 (R2 지원 버전)
"""

import logging
from typing import Dict, List, Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)


class CrawlerAPIClient:
    """SvelteKit Crawler API 클라이언트"""

    def __init__(self, api_url: str, api_key: str, timeout: int = 60):
        self.api_url = api_url.rstrip('/')
        self.api_key = api_key
        self.timeout = timeout
        
        self.session = requests.Session()
        self.session.headers.update({
            'X-API-Key': api_key,
            'Content-Type': 'application/json',
            'User-Agent': 'Crawler/1.0'
        })
        
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["POST"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def save_post(
        self, 
        post_data: Dict, 
        images_metadata: List[Dict]
    ) -> Optional[Dict]:
        """
        게시글 + 이미지 메타데이터 저장
        
        Args:
            post_data: 게시글 데이터
            images_metadata: 업로드된 이미지 정보 리스트
                [
                    {
                        "url": "R2 URL",
                        "r2_key": "R2 Key",
                        "original_url": "원본 URL",
                        "order_index": 0
                    }, ...
                ]
        """
        try:
            payload = {
                "post": post_data,
                "images": images_metadata
            }
            
            response = self.session.post(
                f"{self.api_url}/api/crawler/posts",
                json=payload,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('duplicate'):
                    return None
                if result.get('success'):
                    logger.info(f"✅ Post saved via API: {post_data['title'][:40]}... (ID: {result.get('post_id')})")
                    return result
                return None
            else:
                logger.error(f"❌ API error {response.status_code}: {response.text[:200]}")
                return None
        except Exception as e:
            logger.error(f"❌ Unexpected error in save_post: {e}")
            return None

    def save_logs(self, logs: List[Dict]) -> bool:
        if not logs: return True
        try:
            response = self.session.post(
                f"{self.api_url}/api/crawler/logs",
                json={"logs": logs},
                timeout=30
            )
            return response.status_code == 200
        except Exception as e:
            return True

    def close(self):
        self.session.close()
