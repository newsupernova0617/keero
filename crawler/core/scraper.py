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

    def __init__(self, base_url: str, selectors: Dict[str, str], list_url: Optional[str] = None, user_agent: Optional[str] = None, use_playwright: bool = False):
        """
        Args:
            base_url: 타겟 사이트 기본 URL
            selectors: CSS 선택자 딕셔너리
            list_url: 게시글 목록 URL (None이면 base_url/list 사용)
            user_agent: User-Agent 문자열 (None이면 기본값 사용)
            use_playwright: Playwright 사용 여부 (True=Playwright, False=requests)
        """
        self.base_url = base_url
        self.list_url = list_url or f"{base_url}/list"
        self.selectors = selectors
        self.use_playwright = use_playwright
        self.session = requests.Session()
        
        # User-Agent 설정
        self.user_agent = user_agent or "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        self.session.headers.update({"User-Agent": self.user_agent})

        # Playwright 관련 변수 초기화 (지연 생성)
        self._pw = None
        self._browser = None
        self._context = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        """자원 정리 (브라우저 종료 포함)"""
        if self._context:
            self._context.close()
            self._context = None
        if self._browser:
            self._browser.close()
            self._browser = None
        if self._pw:
            self._pw.stop()
            self._pw = None
        self.session.close()

    def _init_playwright(self):
        """Playwright 브라우저 및 컨텍스트 초기화 (지연 로딩)"""
        if self._browser:
            return

        from playwright.sync_api import sync_playwright
        self._pw = sync_playwright().start()
        
        # e2-micro를 위한 극한의 최적화 플래그
        self._browser = self._pw.chromium.launch(
            headless=True,
            args=[
                '--disable-gpu',
                '--disable-dev-shm-usage',
                '--disable-setuid-sandbox',
                '--no-sandbox',
                '--single-process',          # 메모리 사용 최소화
                '--no-zygote',
                '--disable-extensions',
                '--mute-audio',
                '--no-first-run',
                '--disable-background-networking',
                '--disable-default-apps',
                '--disable-sync',
                '--js-flags="--max-old-space-size=256"', # V8 엔진 메모리 제한
            ]
        )
        self._context = self._browser.new_context(
            user_agent=self.user_agent,
            viewport={'width': 1280, 'height': 800}
        )

    def fetch_page(self, url: str) -> BeautifulSoup:
        """페이지 HTML 가져오기 (requests 또는 playwright 재사용)"""
        if self.use_playwright:
            self._init_playwright()
            page = self._context.new_page()
            try:
                # 리소스 로딩 최적화: 이미지, 폰트 등은 로드하지 않음 (메모리 ↓)
                page.route("**/*.{png,jpg,jpeg,gif,webp,svg,woff,woff2,ttf,otf,css}", lambda route: route.abort())
                
                # 60초 타임아웃, DOM 로드 시점까지만 대기
                page.goto(url, wait_until="domcontentloaded", timeout=60000)
                
                # 동적 로딩을 위한 짧은 대기 (선택적)
                # time.sleep(1) 
                
                content = page.content()
                return BeautifulSoup(content, "lxml")
            except Exception as e:
                logger.error(f"Playwright fetch error: {url} - {e}")
                raise FetchError(f"Playwright Error: {url} - {e}")
            finally:
                page.close() # 탭은 닫되 브라우저는 유지하여 재사용
        
        # requests 사용
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return BeautifulSoup(response.text, "lxml")
        except Exception as e:
            raise FetchError(f"Fetch failed: {url} - {e}")

    def fetch_page_with_retry(self, url: str, max_retries: int = 3) -> Optional[BeautifulSoup]:
        """재시도 로직을 포함한 페이지 가져오기"""
        for attempt in range(max_retries):
            try:
                return self.fetch_page(url)
            except FetchError as e:
                if attempt == max_retries - 1:
                    logger.error(f"Failed after {max_retries} attempts: {e}")
                    return None
                wait_time = 2**attempt
                logger.warning(f"Retry {attempt+1}/{max_retries} after {wait_time}s: {e}")
                time.sleep(wait_time)
        return None

    def get_post_list(self, page_num: int = 1) -> List[str]:
        """게시글 목록에서 URL 추출"""
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
            # 사이트별 특정 클래스 필터링 (광고, 인기글 등)
            if 'ruliweb.com' in self.base_url:
                if 'best' in item.get('class', []) or 'list_inner' in item.get('class', []):
                    continue
            if 'fmkorea.com' in self.base_url:
                if 'li_best2_pop1' in item.get('class', []) or 'li_best2_hotdeal1' in item.get('class', []):
                    continue
            
            link = item.select_one(self.selectors["post_link"])
            if not link and item.get("href"):
                link = item
            if link and link.get("href"):
                url = urljoin(self.base_url, link["href"])
                
                # 뽐뿌 특정 게시판 필터링
                if 'ppomppu.co.kr' in self.base_url:
                    excluded = ['id=freeboard', 'id=coupon', 'id=ppomppu', 'id=ppomppu4', 'id=event', 'id=money']
                    if any(b in url for b in excluded):
                        continue
                
                urls.append(url)
        return urls

    def parse_post(self, url: str, max_retries: int = 3) -> Optional[Dict]:
        """개별 게시글 파싱"""
        soup = self.fetch_page_with_retry(url, max_retries)
        if not soup:
            return None
        
        # 오유 시사 게시판 필터링
        if 'todayhumor.co.kr' in self.base_url:
            html_str = str(soup)
            if 'var parent_table = "sisa"' in html_str:
                return None

        try:
            # 제목
            title_elem = soup.select_one(self.selectors["title"])
            title = title_elem.get_text(strip=True) if title_elem else "제목 없음"
            
            # 사이트별 제목 정리
            if 'dogdrip.net' in self.base_url:
                title = title.split(' - DogDrip')[0].strip()
            elif 'fmkorea.com' in self.base_url:
                title = title.split(' - ')[0].strip()

            # 본문
            content_elem = soup.select_one(self.selectors["content"])
            if 'fmkorea.com' in self.base_url and content_elem:
                for doc_addr in content_elem.select('div.document_address'):
                    doc_addr.decompose()
            
            content = content_elem.get_text(strip=True) if content_elem else ""
            
            # HTML 정리
            content_html = ""
            if content_elem:
                content_html = self.clean_html(str(content_elem))

            # 이미지/동영상
            images = self.extract_images(soup)

            # 날짜
            date_elem = soup.select_one(self.selectors.get("date", ""))
            created_at = self.parse_date(date_elem.get_text(strip=True)) if date_elem else None

            return {
                "title": title,
                "content": content,
                "content_html": content_html,
                "source_url": url,
                "created_at": created_at,
                "images": images,
            }
        except Exception as e:
            logger.error(f"Failed to parse post {url}: {e}")
            raise ParseError(f"Parse failed: {url} - {e}") from e

    def extract_images(self, soup: BeautifulSoup) -> List[str]:
        """원본 이미지 및 동영상 URL 추출"""
        media_urls = []
        img_elements = soup.select(self.selectors["images"])
        for img in img_elements:
            src = img.get("data-original") or img.get("src")
            if src:
                absolute_url = urljoin(self.base_url, src)
                if '/images/' in absolute_url or 'transparent.gif' in absolute_url:
                    continue
                media_urls.append(absolute_url)
        
        # 동영상 추출
        content_elem = soup.select_one(self.selectors.get("content", ""))
        if content_elem:
            for video in content_elem.find_all('video'):
                src = video.get('src') or (video.find('source').get('src') if video.find('source') else None)
                if src:
                    media_urls.append(urljoin(self.base_url, src))

        return media_urls

    def parse_date(self, date_text: str) -> Optional[datetime]:
        """날짜 파싱"""
        try:
            return dateutil_parser.parse(date_text, fuzzy=True)
        except:
            return None

    def clean_html(self, html: str) -> str:
        """HTML 정리 및 placeholder 교체"""
        soup = BeautifulSoup(html, "lxml")
        for tag in soup.find_all(['script', 'iframe', 'embed', 'object', 'style', 'link', 'meta']):
            tag.decompose()
        
        # 사이트별 전처리
        self._clean_site_specific(soup)
        
        # 이미지 placeholder화
        for i, img in enumerate(soup.find_all('img')):
            placeholder = soup.new_tag('div')
            placeholder['data-image-index'] = str(i)
            placeholder['class'] = 'image-placeholder'
            img.replace_with(placeholder)
        
        # 비디오 placeholder화
        for i, video in enumerate(soup.find_all('video')):
            placeholder = soup.new_tag('div')
            placeholder['data-video-index'] = str(i)
            placeholder['class'] = 'video-placeholder'
            video.replace_with(placeholder)
        
        # 속성 제한
        allowed = ['href', 'alt', 'title', 'data-image-index', 'data-video-index']
        for tag in soup.find_all(True):
            tag.attrs = {k: v for k, v in tag.attrs.items() if k in allowed}
        
        return str(soup)

    def _clean_site_specific(self, soup: BeautifulSoup):
        """사이트별 하드코딩된 UI 제거"""
        if 'm.humoruniv.com' in self.base_url:
            for span in soup.find_all('span', string='원본'):
                if span.parent and span.parent.name in ['a', 'div']:
                    span.parent.decompose()
        
        if 'fmkorea.com' in self.base_url:
            for tag in soup.find_all(['span', 'p', 'div']):
                if tag.get_text(strip=True) in ['Video Player', '재생 에러', 'Download File:']:
                    if not tag.find('video'):
                        tag.decompose()
