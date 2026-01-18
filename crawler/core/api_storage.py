"""
API 모드 Storage Wrapper (R2 직접 업로드 지원)
"""

import logging
from typing import Dict, List, Optional
from core.api_client import CrawlerAPIClient
from core.storage import DatabaseManager, replace_image_urls_in_html

logger = logging.getLogger(__name__)

class APIStorageManager:
    """API 모드 Storage (R2 업로드 로직 포함)"""

    def __init__(self, api_url: str, api_key: str, r2_config: Optional[Dict] = None, timeout: int = 60):
        self.api_client = CrawlerAPIClient(api_url, api_key, timeout)
        
        # R2 업로드 및 이미지 최적화 로직 재사용을 위해 더미 DB 매니저 생성
        # (로컬 파일 대신 메모리 DB 사용으로 속도 향상 및 파일 생성 방지)
        self.internal_db = DatabaseManager(":memory:", r2_config=r2_config)
        self.session = self.internal_db.session

    def flush(self):
        pass

    def save_post_with_html(self, post_data: Dict, image_urls: List[str]) -> Optional[int]:
        """
        1. 이미지 R2 업로드 (GCP에서 직접 실행하여 차단 우회)
        2. HTML 내 URL 치환
        3. 서버 API로 최종 데이터 전송
        """
        # 이미지 업로드 및 URL 매핑 생성 (DatabaseManager 로직 재사용)
        image_mapping = {}
        images_metadata = []
        
        if image_urls:
            for idx, img_url in enumerate(image_urls):
                try:
                    # save_image_smart는 이미지 다운로드, 최적화, R2 업로드를 수행함
                    # 메모리 DB에 임시로 저장됨
                    image_obj = self.internal_db.save_image_smart(0, img_url, idx)
                    image_mapping[img_url] = image_obj.r2_url
                    images_metadata.append({
                        "url": image_obj.r2_url,
                        "r2_key": image_obj.r2_key,
                        "original_url": img_url,
                        "order_index": idx
                    })
                except Exception as e:
                    logger.warning(f"Media processing failed for {img_url}: {e}")
                    continue

        # HTML 내 URL 치환
        content_html = post_data.get("content_html", "")
        if content_html and image_mapping:
            content_html = replace_image_urls_in_html(content_html, image_mapping)

        # API 요청 데이터 구성
        api_post_data = {
            "site_name": post_data["site_name"],
            "title": post_data["title"],
            "content": post_data["content"],
            "content_html": content_html,
            "source_url": post_data["source_url"],
            "created_at": (
                post_data["created_at"].isoformat()
                if post_data.get("created_at") and hasattr(post_data["created_at"], 'isoformat')
                else str(post_data.get("created_at"))
            ),
        }

        # API 호출
        result = self.api_client.save_post(api_post_data, images_metadata)

        if not result:
            return None

        return result.get("post_id")
