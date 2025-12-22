"""
scraper.py 모듈 테스트

HTML 파싱, 데이터 추출 기능을 테스트합니다.
"""

import pytest
import responses
from bs4 import BeautifulSoup

from scraper import FetchError


class TestFetchPage:
    """페이지 가져오기 테스트"""

    @responses.activate
    def test_fetch_page_success(self, scraper):
        """정상적인 페이지 가져오기"""
        responses.add(
            responses.GET,
            "https://example.com/post/1",
            body="<html><body><title>Test</title></body></html>",
            status=200,
        )

        soup = scraper.fetch_page("https://example.com/post/1")
        assert soup is not None
        assert soup.find("title").text == "Test"

    @responses.activate
    def test_fetch_page_404(self, scraper):
        """404 에러 처리"""
        responses.add(responses.GET, "https://example.com/post/404", status=404)

        with pytest.raises(FetchError) as exc_info:
            scraper.fetch_page("https://example.com/post/404")
        assert "404" in str(exc_info.value)

    @responses.activate
    def test_fetch_page_403(self, scraper):
        """403 에러 처리"""
        responses.add(responses.GET, "https://example.com/post/403", status=403)

        with pytest.raises(FetchError) as exc_info:
            scraper.fetch_page("https://example.com/post/403")
        assert "403" in str(exc_info.value)

    @responses.activate
    def test_fetch_page_with_retry_success(self, scraper):
        """재시도 후 성공"""
        # 첫 번째 실패, 두 번째 성공
        responses.add(responses.GET, "https://example.com/post/1", status=500)
        responses.add(
            responses.GET,
            "https://example.com/post/1",
            body="<html><body>Success</body></html>",
            status=200,
        )

        soup = scraper.fetch_page_with_retry("https://example.com/post/1", max_retries=2)
        assert soup is not None

    @responses.activate
    def test_fetch_page_with_retry_all_fail(self, scraper):
        """모든 재시도 실패"""
        responses.add(responses.GET, "https://example.com/post/1", status=500)
        responses.add(responses.GET, "https://example.com/post/1", status=500)
        responses.add(responses.GET, "https://example.com/post/1", status=500)

        result = scraper.fetch_page_with_retry("https://example.com/post/1", max_retries=3)
        assert result is None


class TestExtractImages:
    """이미지 추출 테스트"""

    def test_extract_images_from_html(self, scraper, sample_post_html):
        """HTML에서 이미지 URL 추출"""
        soup = BeautifulSoup(sample_post_html, "lxml")
        images = scraper.extract_images(soup)

        assert len(images) == 2
        assert "https://example.com/images/dog1.jpg" in images
        assert "https://example.com/images/dog2.jpg" in images

    def test_extract_images_converts_relative_urls(self, scraper):
        """상대 경로를 절대 경로로 변환"""
        html = '<html><body><div class="content"><img src="/images/test.jpg"></div></body></html>'
        soup = BeautifulSoup(html, "lxml")
        images = scraper.extract_images(soup)

        assert len(images) == 1
        assert images[0].startswith("https://")  # 절대 경로로 변환됨

    def test_extract_images_empty(self, scraper):
        """이미지가 없는 경우"""
        html = '<html><body><div class="content"><p>No images</p></div></body></html>'
        soup = BeautifulSoup(html, "lxml")
        images = scraper.extract_images(soup)

        assert len(images) == 0


class TestParsePost:
    """게시글 파싱 테스트"""

    @responses.activate
    def test_parse_post_extracts_all_fields(self, scraper, sample_post_html):
        """게시글의 모든 필드 추출"""
        responses.add(
            responses.GET,
            "https://example.com/post/1",
            body=sample_post_html,
            status=200,
        )

        data = scraper.parse_post("https://example.com/post/1")

        assert data is not None
        assert data["title"] == "강아지가 밥그릇 엎음ㅋㅋ"
        assert "강아지" in data["content"]
        assert len(data["images"]) == 2
        assert data["source_url"] == "https://example.com/post/1"

    @responses.activate
    def test_parse_post_returns_none_on_failure(self, scraper):
        """페이지 가져오기 실패 시 None 반환"""
        responses.add(responses.GET, "https://example.com/post/404", status=404)
        responses.add(responses.GET, "https://example.com/post/404", status=404)
        responses.add(responses.GET, "https://example.com/post/404", status=404)

        result = scraper.parse_post("https://example.com/post/404", max_retries=3)
        assert result is None


class TestGetPostList:
    """게시글 목록 가져오기 테스트"""

    @responses.activate
    def test_get_post_list_extracts_urls(self, scraper, sample_list_html):
        """목록 페이지에서 게시글 URL 추출"""
        responses.add(
            responses.GET,
            "https://example.com/list?page=1",
            body=sample_list_html,
            status=200,
        )

        urls = scraper.get_post_list(page_num=1)

        assert len(urls) == 3
        assert "https://example.com/post/1" in urls
        assert "https://example.com/post/2" in urls
        assert "https://example.com/post/3" in urls

    @responses.activate
    def test_get_post_list_empty_on_failure(self, scraper):
        """페이지 가져오기 실패 시 빈 리스트"""
        responses.add(responses.GET, "https://example.com/list?page=1", status=500)
        responses.add(responses.GET, "https://example.com/list?page=1", status=500)
        responses.add(responses.GET, "https://example.com/list?page=1", status=500)

        urls = scraper.get_post_list(page_num=1)
        assert urls == []


class TestExceptionChaining:
    """예외 체이닝 테스트"""

    @responses.activate
    def test_fetch_error_has_cause(self, scraper):
        """FetchError가 원본 예외를 체이닝하는지 확인"""
        responses.add(responses.GET, "https://example.com/post/1", status=404)

        with pytest.raises(FetchError) as exc_info:
            scraper.fetch_page("https://example.com/post/1")

        # 원본 예외가 체이닝되어 있어야 함
        assert exc_info.value.__cause__ is not None
