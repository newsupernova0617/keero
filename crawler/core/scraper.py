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
        
        # User-Agent 설정 (외부에서 주입 가능)
        self.user_agent = user_agent or "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        self.session.headers.update({"User-Agent": self.user_agent})

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
        # Playwright 사용 시
        if self.use_playwright:
            return self.fetch_page_playwright(url)
        
        # requests 사용 시
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

    def fetch_page_playwright(self, url: str) -> BeautifulSoup:
        """
        Playwright로 페이지 HTML 가져오기 (JavaScript 렌더링 지원)

        Args:
            url: 페이지 URL

        Returns:
            BeautifulSoup 객체

        Raises:
            FetchError: 페이지 로드 실패 시
        """
        try:
            from playwright.sync_api import sync_playwright
            
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                context = browser.new_context(
                    user_agent=self.user_agent
                )
                page = context.new_page()
                
                # 페이지 로드
                page.goto(url, wait_until='domcontentloaded', timeout=30000)
                time.sleep(2)  # 추가 대기 (동적 콘텐츠)
                
                # HTML 가져오기
                html = page.content()
                browser.close()
                
                return BeautifulSoup(html, "lxml")
                
        except Exception as e:
            raise FetchError(f"Playwright Error: {url} - {e}") from e

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
            # 루리웹: best/광고 클래스 제외
            if 'ruliweb.com' in self.base_url:
                classes = item.get('class', [])
                if 'best' in classes or 'list_inner' in classes:
                    continue  # 핫 포스트 또는 광고 스킵
            
            # 펨코: 인기 게시물/핫딜 제외
            if 'fmkorea.com' in self.base_url:
                classes = item.get('class', [])
                # li_best2_pop1 (인기) 또는 li_best2_hotdeal1 (핫딜) 스킵
                if 'li_best2_pop1' in classes or 'li_best2_hotdeal1' in classes:
                    continue
            
            link = item.select_one(self.selectors["post_link"])
            # post_link를 못 찾으면 item 자체가 링크인지 확인
            if not link and item.get("href"):
                link = item
            if link and link.get("href"):
                url = urljoin(self.base_url, link["href"])
                
                # 뽐뿌: freeboard 제외 (humor만 허용)
                if 'ppomppu.co.kr' in self.base_url:
                    if 'id=freeboard' in url:
                        continue  # 자유게시판 스킵
                
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
        
        # 오유: 시사 게시판 필터링
        if 'todayhumor.co.kr' in self.base_url:
            # HTML에서 parent_table 변수 확인
            html_str = str(soup)
            if 'var parent_table = "sisa"' in html_str or 'var parent_table = "sisaarch"' in html_str:
                logger.info(f"⏭️  Skipping sisa board post: {url}")
                return None

        try:
            # 제목 추출
            title_elem = soup.select_one(self.selectors["title"])
            logger.debug(f"Title selector: {self.selectors['title']}, Found: {title_elem is not None}")
            if title_elem:
                logger.debug(f"Title element HTML: {str(title_elem)[:200]}")
            title = title_elem.get_text(strip=True) if title_elem else "제목 없음"
            logger.debug(f"Extracted title: {title[:50]}")
            
            # 개드립: title 태그에서 사이트명 제거
            if 'dogdrip.net' in self.base_url and ' - DogDrip' in title:
                title = title.split(' - DogDrip')[0].strip()
                logger.debug(f"Cleaned dogdrip title: {title[:50]}")
            
            # 펨코: title 태그에서 사이트명 제거
            if 'fmkorea.com' in self.base_url and ' - ' in title:
                # "제목 - 게시판 - 에펨코리아" 형식
                title = title.split(' - ')[0].strip()
                logger.debug(f"Cleaned fmkorea title: {title[:50]}")

            # 본문 추출
            content_elem = soup.select_one(self.selectors["content"])
            logger.debug(f"Content selector: {self.selectors['content']}, Found: {content_elem is not None}")
            
            # 펨코: URL 복사 섹션 제거 (텍스트 추출 전)
            if 'fmkorea.com' in self.base_url and content_elem:
                for doc_addr in content_elem.select('div.document_address'):
                    doc_addr.decompose()
            
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
        본문에서 이미지 및 동영상 URL 추출

        Args:
            soup: BeautifulSoup 객체

        Returns:
            이미지/동영상 URL 리스트
        """
        media_urls = []
        
        # 이미지 추출
        img_elements = soup.select(self.selectors["images"])
        for img in img_elements:
            # Lazy loading 이미지 처리: data-original 우선 확인 (FMKorea 등)
            src = img.get("data-original") or img.get("src")
            if src:
                # 상대 경로를 절대 경로로 변환
                absolute_url = urljoin(self.base_url, src)
                
                # UI 버튼/아이콘 이미지 필터링 (/images/ 경로 제외)
                # 예: /images/doscrap2.gif, /images/view_source2.gif 등
                if '/images/' in absolute_url:
                    continue
                
                # Lazy loading placeholder 제외 (transparent.gif 등)
                if 'transparent.gif' in absolute_url or 'placeholder' in absolute_url.lower():
                    continue
                
                media_urls.append(absolute_url)
        
        # 동영상 추출 (<video> 태그)
        # content selector 내의 모든 video 태그 찾기
        content_selector = self.selectors.get("content", "")
        if content_selector:
            content_elem = soup.select_one(content_selector)
            if content_elem:
                # <video> 태그에서 src 추출
                for video in content_elem.find_all('video'):
                    src = video.get('src')
                    if src:
                        absolute_url = urljoin(self.base_url, src)
                        media_urls.append(absolute_url)
                    
                    # <source> 태그에서 src 추출
                    for source in video.find_all('source'):
                        src = source.get('src')
                        if src:
                            absolute_url = urljoin(self.base_url, src)
                            media_urls.append(absolute_url)
                            break  # 첫 번째 source만 사용

        return media_urls

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
        HTML 정리 및 보안 처리
        
        Args:
            html: 원본 HTML
        
        Returns:
            정리된 HTML
        """
        soup = BeautifulSoup(html, "lxml")
        
        # 위험한 태그 제거
        for tag in soup.find_all(['script', 'iframe', 'embed', 'object', 'style', 'link', 'meta']):
            tag.decompose()
        
        # 사이트별 커스텀 정리
        self._clean_site_specific(soup)
        
        # Lazy loading 이미지 처리 (data-original -> src 복사)
        # 속성 정리 전에 수행해야 함
        for img in soup.find_all('img'):
            data_original = img.get('data-original')
            src = img.get('src', '')
            # src가 placeholder이고 data-original이 있으면 복사
            if data_original and ('transparent.gif' in src or 'placeholder' in src.lower() or not src):
                img['src'] = data_original
        
        # 이미지는 유지 (나중에 R2 URL로 치환됨)
        # UI 아이콘은 replace_image_urls_in_html 후에 제거됨
        
        # 모든 태그에서 class, style, id 속성 제거 (보안상 이유)
        # 허용된 속성만 남기기
        allowed_attrs = ['src', 'href', 'alt', 'title', 'controls', 'autoplay', 'loop', 'muted', 'playsinline']
        for tag in soup.find_all(True):
            tag.attrs = {k: v for k, v in tag.attrs.items() if k in allowed_attrs}
        
        return str(soup)
    
    def _clean_site_specific(self, soup: BeautifulSoup):
        """
        사이트별 커스텀 HTML 정리
        
        Args:
            soup: BeautifulSoup 객체 (in-place 수정)
        """
        site_name = self.base_url
        
        # 웃긴대학 모바일: "원본" 버튼 제거
        if 'm.humoruniv.com' in site_name:
            # "원본" 버튼 (btn_nemo 클래스)
            for btn in soup.find_all('span', string='원본'):
                # 버튼의 부모 div/a 태그도 함께 제거
                parent = btn.parent
                if parent and parent.name in ['a', 'div']:
                    parent.decompose()
                else:
                    btn.decompose()
            
            # 이미지 확장 버튼 관련 div 제거
            for div in soup.find_all('div'):
                # id가 btn_nemo로 시작하는 div
                div_id = div.get('id', '')
                if 'btn_nemo' in div_id or 'expand' in div_id:
                    div.decompose()
        
        # 펨코 비디오 플레이어 UI 및 찌꺼기 완벽 제거 (최종병기: 비디오 중심 탐색)
        if 'fmkorea.com' in site_name:
                # 1. 모든 비디오 태그를 찾는다.
                videos = soup.find_all('video')
                for video in videos:
                    # 이미 처리되어 트리에서 떨어진 비디오는 스킵
                    if video.parent is None: continue

                    # 비디오의 조상들을 타고 올라가며 'Video Player' 텍스트를 가진 '껍데기'를 찾는다.
                    curr = video.parent
                    target_container = None
                    
                    # 최대 15단계 위까지 탐색
                    for _ in range(15):
                        # body나 article까지 올라가면 중단 (안전장치)
                        if not curr or curr.name in ['article', 'body', 'html']: break
                        
                        # 텍스트 검사를 위해 get_text() 사용 (비용이 좀 들지만 가장 확실함)
                        # 하지만 전체 텍스트를 가져오면 너무 느리므로, 
                        # 'Video Player' 텍스트를 가진 span이 이 조상의 자손으로 있는지 확인하는 것이 더 효율적
                        if curr.find('span', string=lambda t: t and 'Video Player' in t):
                            target_container = curr
                            # 가장 가까운 껍데기를 찾으면 그게 범인이다.
                            break
                        
                        curr = curr.parent
                    
                    if target_container:
                        # 껍데기 발견! 비디오 추출 후 껍데기 교체
                        video_node = video.extract()
                        target_container.replace_with(video_node)
                        # 가독성을 위해 줄바꿈 추가
                        video_node.insert_after(soup.new_tag('br'))

                # 2. 잔당 소탕 (비디오 없이 껍데기만 남은 경우 등)
                for tag in soup.find_all(['span', 'p', 'div', 'a']):
                    # 텍스트가 조금이라도 있으면 검사
                    if tag.string or tag.get_text(strip=True): 
                        text = tag.get_text()
                        if 'Video Player' in text or '재생 에러' in text or 'Download File:' in text or 'Use Up/Down' in text:
                            # 비디오를 포함하지 않고, 최상위 요소가 아니면 삭제
                            if not tag.find('video') and tag.name not in ['body', 'article', 'html']:
                                tag.decompose()
                
                # 3. 비디오 컨트롤러 잔여물 (input, label, svg 등)
                # 비디오 태그 내부가 아닌 곳에 있는 불필요한 태그들 삭제
                for tag in soup.find_all(['label', 'input', 'svg']):
                    if not tag.find_parent('video'):
                        tag.decompose()

