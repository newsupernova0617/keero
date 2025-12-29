"""
SvelteKit Crawler API 클라이언트

역할:
- SvelteKit API 엔드포인트와 통신
- 게시글 및 로그 데이터 전송
- 재시도 로직 및 에러 처리
"""

import logging
import time
from typing import Dict, List, Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)


class CrawlerAPIClient:
    """SvelteKit Crawler API 클라이언트"""

    def __init__(self, api_url: str, api_key: str, timeout: int = 60):
        """
        Args:
            api_url: SvelteKit API URL (예: https://your-app.railway.app)
            api_key: API 인증 키
            timeout: 요청 타임아웃 (초)
        """
        self.api_url = api_url.rstrip('/')
        self.api_key = api_key
        self.timeout = timeout
        
        # 세션 설정 (연결 재사용)
        self.session = requests.Session()
        self.session.headers.update({
            'X-API-Key': api_key,
            'Content-Type': 'application/json',
            'User-Agent': 'Crawler/1.0'
        })
        
        # 재시도 전략 설정
        retry_strategy = Retry(
            total=3,  # 최대 3번 재시도
            backoff_factor=1,  # 1초, 2초, 4초 대기
            status_forcelist=[429, 500, 502, 503, 504],  # 재시도할 HTTP 상태 코드
            allowed_methods=["POST"]  # POST 요청만 재시도
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def save_post(
        self, 
        post_data: Dict, 
        image_urls: List[str]
    ) -> Optional[Dict]:
        """
        게시글 + 이미지 저장
        
        Args:
            post_data: 게시글 데이터
                {
                    "site_name": str,
                    "title": str,
                    "content": str,
                    "content_html": str,
                    "source_url": str,
                    "created_at": str (ISO format)
                }
            image_urls: 이미지 URL 리스트
        
        Returns:
            API 응답 딕셔너리 또는 None (실패 시)
            {
                "success": bool,
                "post_id": int,
                "images_saved": int
            }
        """
        try:
            # 요청 페이로드 구성
            payload = {
                "post": post_data,
                "images": [
                    {"url": url, "order_index": idx}
                    for idx, url in enumerate(image_urls)
                ]
            }
            
            # API 호출
            response = self.session.post(
                f"{self.api_url}/api/crawler/posts",
                json=payload,
                timeout=self.timeout
            )
            
            # 응답 처리
            if response.status_code == 200:
                result = response.json()
                
                # 중복 게시글
                if result.get('duplicate'):
                    logger.debug(f"Duplicate post: {post_data['source_url']}")
                    return None
                
                # 성공
                if result.get('success'):
                    logger.info(
                        f"✅ Post saved via API: {post_data['title'][:50]} "
                        f"(ID: {result.get('post_id')}, Images: {result.get('images_saved')})"
                    )
                    return result
                
                logger.warning(f"API returned success=false: {result}")
                return None
            
            elif response.status_code == 401:
                logger.error("❌ API authentication failed! Check CRAWLER_API_KEY")
                return None
            
            else:
                logger.error(
                    f"❌ API error {response.status_code}: {response.text[:200]}"
                )
                return None
                
        except requests.Timeout:
            logger.error(f"⏱️ API timeout after {self.timeout}s: {post_data['source_url']}")
            return None
        
        except requests.ConnectionError as e:
            logger.error(f"🔌 API connection error: {e}")
            return None
        
        except Exception as e:
            logger.error(f"❌ Unexpected error in save_post: {e}", exc_info=True)
            return None

    def save_logs(self, logs: List[Dict]) -> bool:
        """
        로그 배치 저장
        
        Args:
            logs: 로그 데이터 리스트
                [
                    {
                        "timestamp": str (ISO format),
                        "level": str,
                        "level_no": int,
                        "logger": str,
                        "message": str,
                        "function": str,
                        "line_number": int,
                        "exception": str | None,
                        "extra_data": str | None
                    }
                ]
        
        Returns:
            성공 여부
        """
        if not logs:
            return True
        
        try:
            # 요청 페이로드 구성
            payload = {"logs": logs}
            
            # API 호출
            response = self.session.post(
                f"{self.api_url}/api/crawler/logs",
                json=payload,
                timeout=30  # 로그는 짧은 타임아웃
            )
            
            # 응답 처리
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    logger.debug(f"📝 {result.get('logs_saved')} logs saved via API")
                    return True
                
                logger.warning(f"API returned success=false: {result}")
                return False
            
            elif response.status_code == 401:
                logger.error("❌ API authentication failed! Check CRAWLER_API_KEY")
                return False
            
            else:
                logger.error(
                    f"❌ Logs API error {response.status_code}: {response.text[:200]}"
                )
                return False
                
        except Exception as e:
            logger.error(f"❌ Error saving logs via API: {e}")
            # 로그 저장 실패는 치명적이지 않으므로 True 반환 (계속 진행)
            return True

    def close(self):
        """세션 종료"""
        self.session.close()
