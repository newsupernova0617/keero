"""
HTML 파싱 및 데이터 추출 모듈

역할:
- 타겟 사이트 HTML 다운로드
- BeautifulSoup을 이용한 HTML 파싱
- 게시글 제목, 본문, 이미지 URL 추출
- 데이터 정규화 및 검증
"""

import logging
import random
import time
from datetime import datetime
from typing import Dict, List, Optional
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from dateutil import parser as dateutil_parser

logger = logging.getLogger(__name__)


class FetchError(Exception):
    """HTTP 요청 실패 시 발생하는 예외"""

    pass


class ParseError(Exception):
    """HTML 파싱 실패 시 발생하는 예외"""

    pass


class Scraper:
    """웹 크롤러 클래스"""

    def __init__(self, base_url: str, selectors: Dict[str, str], list_url: Optional[str] = None, user_agent: Optional[str] = None):
        """
        Args:
            base_url: 타겟 사이트 기본 URL
            selectors: CSS 선택자 딕셔너리
            list_url: 게시글 목록 URL (None이면 base_url/list 사용)
            user_agent: User-Agent 문자열 (None이면 기본값 사용)
        """
        self.base_url = base_url
        self.list_url = list_url or f"{base_url}/list"
        self.selectors = selectors
        self.session = requests.Session()
        
        # User-Agent 설정 (외부에서 주입 가능)
        ua = user_agent or "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        self.session.headers.update({"User-Agent": ua})

    def fetch_page(self, url: str) -> BeautifulSoup:
        """
        페이지 HTML 가져오기

        Args:
            url: 페이지 URL

        Returns:
            BeautifulSoup 객체

        Raises:
            FetchError: HTTP 요청 실패 시
        """
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return BeautifulSoup(response.text, "lxml")
        except requests.HTTPError as e:
            if e.response.status_code == 404:
                raise FetchError(f"404 Not Found: {url}") from e
            elif e.response.status_code == 403:
                raise FetchError(f"403 Forbidden: {url}") from e
            raise FetchError(f"HTTP Error {e.response.status_code}: {url}") from e
        except requests.Timeout as e:
            raise FetchError(f"Timeout: {url}") from e
        except requests.RequestException as e:
            raise FetchError(f"Network Error: {url} - {e}") from e

    def fetch_page_with_retry(
        self, url: str, max_retries: int = 3
    ) -> Optional[BeautifulSoup]:
        """
        재시도 로직을 포함한 페이지 가져오기

        Args:
            url: 페이지 URL
            max_retries: 최대 재시도 횟수

        Returns:
            BeautifulSoup 객체 또는 None (최종 실패 시)
        """
        for attempt in range(max_retries):
            try:
                return self.fetch_page(url)
            except FetchError as e:
                if attempt == max_retries - 1:
                    logger.error(f"Failed after {max_retries} attempts: {e}")
                    return None
                wait_time = 2**attempt  # 지수 백오프: 1초, 2초, 4초
                logger.warning(f"Retry {attempt+1}/{max_retries} after {wait_time}s: {e}")
                time.sleep(wait_time)
        return None

    def get_post_list(self, page_num: int = 1) -> List[str]:
        """
        게시글 목록에서 URL 추출

        Args:
            page_num: 페이지 번호

        Returns:
            게시글 URL 리스트
        """
        # list_url에 ?page= 파라미터가 있으면 사용, 없으면 추가
        if "?" in self.list_url:
            list_url = f"{self.list_url}&page={page_num}" if page_num > 1 else self.list_url
        else:
            list_url = f"{self.list_url}?page={page_num}" if page_num > 1 else self.list_url
        
        soup = self.fetch_page_with_retry(list_url)

        if not soup:
            return []

        urls = []
        post_items = soup.select(self.selectors["post_list"])

        for item in post_items:
            link = item.select_one(self.selectors["post_link"])
            if link and link.get("href"):
                url = urljoin(self.base_url, link["href"])
                urls.append(url)

        return urls

    def parse_post(self, url: str, max_retries: int = 3) -> Optional[Dict]:
        """
        개별 게시글 파싱 (재시도 로직 포함)

        Args:
            url: 게시글 URL
            max_retries: 최대 재시도 횟수

        Returns:
            게시글 데이터 딕셔너리
            {
                'title': str,
                'content': str,
                'source_url': str,
                'created_at': datetime,
                'images': List[str]  # 이미지 URL 리스트
            }
        """
        soup = self.fetch_page_with_retry(url, max_retries)

        if not soup:
            return None

        try:
            # 제목 추출
            title_elem = soup.select_one(self.selectors["title"])
            title = title_elem.get_text(strip=True) if title_elem else "제목 없음"

            # 본문 추출
            content_elem = soup.select_one(self.selectors["content"])
            content = content_elem.get_text(strip=True) if content_elem else ""
            
            # HTML 추출 및 정리 (NEW)
            content_html = ""
            if content_elem:
                content_html = str(content_elem)
                content_html = self.clean_html(content_html)

            # 이미지 추출
            images = self.extract_images(soup)

            # 날짜 추출 (선택사항)
            date_elem = soup.select_one(self.selectors.get("date", ""))
            created_at = None
            if date_elem:
                date_text = date_elem.get_text(strip=True)
                created_at = self.parse_date(date_text)

            return {
                "title": title,
                "content": content,
                "content_html": content_html,  # NEW
                "source_url": url,
                "created_at": created_at,
                "images": images,
            }
        except Exception as e:
            logger.error(f"Failed to parse post {url}: {e}")
            raise ParseError(f"Parse failed: {url} - {e}") from e

    def extract_images(self, soup: BeautifulSoup) -> List[str]:
        """
        본문에서 이미지 URL 추출

        Args:
            soup: BeautifulSoup 객체

        Returns:
            이미지 URL 리스트
        """
        images = []
        img_elements = soup.select(self.selectors["images"])

        for img in img_elements:
            src = img.get("src")
            if src:
                # 상대 경로를 절대 경로로 변환
                absolute_url = urljoin(self.base_url, src)
                images.append(absolute_url)

        return images

    def parse_date(self, date_text: str) -> Optional[datetime]:
        """
        날짜 텍스트를 datetime 객체로 파싱
        
        Args:
            date_text: 날짜 텍스트 (예: "2025-12-17", "2시간 전", "2025.12.17 14:30")
        
        Returns:
            datetime 객체 또는 None (파싱 실패 시)
        """
        try:
            # dateutil.parser를 사용한 자동 파싱
            return dateutil_parser.parse(date_text, fuzzy=True)
        except (ValueError, TypeError) as e:
            logger.warning(f"Failed to parse date '{date_text}': {e}")
            return None

    def clean_html(self, html: str) -> str:
        """
        HTML ?�리 �?보안 처리
        
        Args:
            html: ?�본 HTML
        
        Returns:
            ?�리??HTML
        """
        soup = BeautifulSoup(html, "lxml")
        
        # ?�험???�그 ?�거
        for tag in soup.find_all(['script', 'iframe', 'embed', 'object', 'style', 'link', 'meta']):
            tag.decompose()
        
        # 모든 ?�그?�서 class, style, id ?�성 ?�거 (?�자???��???
        # ?�용???�성�??�기�?모두 ?�거
        allowed_attrs = ['src', 'href', 'alt', 'title']
        for tag in soup.find_all(True):
            tag.attrs = {k: v for k, v in tag.attrs.items() if k in allowed_attrs}
        
        return str(soup)
