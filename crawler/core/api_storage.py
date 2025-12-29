"""
API 모드 Storage Wrapper

역할:
- DatabaseManager와 동일한 인터페이스 제공
- 내부적으로 CrawlerAPIClient 사용
- main.py 코드 변경 없이 API 모드 지원
"""

import logging
from typing import Dict, List, Optional

from core.api_client import CrawlerAPIClient

logger = logging.getLogger(__name__)


class APIStorageManager:
    """API 모드 Storage (DatabaseManager 인터페이스 호환)"""

    def __init__(self, api_url: str, api_key: str, timeout: int = 60):
        """
        Args:
            api_url: SvelteKit API URL
            api_key: API 인증 키
            timeout: 요청 타임아웃
        """
        self.api_client = CrawlerAPIClient(api_url, api_key, timeout)
        self.session = None  # DatabaseManager 호환성 (사용 안 함)

    def flush(self):
        """배치 커밋 (API 모드에서는 불필요)"""
        pass

    def save_post_with_html(
        self, post_data: Dict, image_urls: List[str]
    ) -> Optional[int]:
        """
        게시글 저장 (DatabaseManager.save_post_with_html 호환)

        Args:
            post_data: 게시글 데이터
            image_urls: 이미지 URL 리스트

        Returns:
            post_id 또는 None (중복/실패)
        """
        # API 요청 데이터 구성
        api_post_data = {
            "site_name": post_data["site_name"],
            "title": post_data["title"],
            "content": post_data["content"],
            "content_html": post_data.get("content_html", ""),
            "source_url": post_data["source_url"],
            "created_at": (
                post_data["created_at"].isoformat()
                if post_data.get("created_at")
                else None
            ),
        }

        # API 호출
        result = self.api_client.save_post(api_post_data, image_urls)

        if not result:
            # 중복 또는 실패
            return None

        return result.get("post_id")
