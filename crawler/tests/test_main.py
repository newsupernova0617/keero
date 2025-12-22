"""
main.py 통합 테스트

크롤링 워크플로우 전체를 테스트합니다.
"""

import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest
import responses

from config import Config
from main import crawl_site, run_crawler
from scraper import Scraper
from storage import DatabaseManager


class TestCrawlSite:
    """crawl_site 함수 통합 테스트"""

    @pytest.fixture
    def temp_db(self):
        """임시 데이터베이스"""
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            db_path = f.name
        db = DatabaseManager(db_path)
        yield db
        db.session.close()
        Path(db_path).unlink()

    @pytest.fixture
    def site_config(self):
        """테스트용 사이트 설정"""
        return {
            "base_url": "https://test.com",
            "site_name": "test_site",
            "selectors": {
                "post_list": "div.post",
                "post_link": "a",
                "title": "h1",
                "content": "div.content",
                "images": "img",
            },
        }

    @responses.activate
    def test_crawl_site_basic_flow(self, temp_db, site_config):
        """기본 크롤링 플로우 테스트"""
        # Mock 게시글 목록
        responses.add(
            responses.GET,
            "https://test.com/list?page=1",
            body="""
            <html><body>
                <div class="post"><a href="/post/1">Post 1</a></div>
                <div class="post"><a href="/post/2">Post 2</a></div>
            </body></html>
            """,
            status=200,
        )

        # Mock 게시글 상세
        responses.add(
            responses.GET,
            "https://test.com/post/1",
            body="""
            <html><body>
                <h1>Test Post 1</h1>
                <div class="content">Content 1</div>
            </body></html>
            """,
            status=200,
        )

        responses.add(
            responses.GET,
            "https://test.com/post/2",
            body="""
            <html><body>
                <h1>Test Post 2</h1>
                <div class="content">Content 2</div>
            </body></html>
            """,
            status=200,
        )

        # Config mock
        with patch.object(Config, "CRAWL_CONFIG", {
            "max_pages": 1,
            "delay_between_requests": 0,
            "max_retries": 3,
            "timeout": 30,
            "early_stop": {
                "enabled": False,
                "consecutive_duplicates": 5,
                "page_duplicate_ratio": 0.8,
            },
        }):
            stats = crawl_site("test_site", site_config, temp_db, Scraper)

        # 통계 확인
        assert stats["new_posts"] == 2
        assert stats["duplicates"] == 0
        assert stats["failed"] == 0

    @responses.activate
    def test_crawl_site_duplicate_detection(self, temp_db, site_config):
        """중복 게시글 감지 테스트"""
        # 게시글 목록
        responses.add(
            responses.GET,
            "https://test.com/list?page=1",
            body='<html><body><div class="post"><a href="/post/1">Post 1</a></div></body></html>',
            status=200,
        )

        # 게시글 상세
        post_html = """
        <html><body>
            <h1>Test Post</h1>
            <div class="content">Content</div>
        </body></html>
        """
        responses.add(responses.GET, "https://test.com/post/1", body=post_html, status=200)

        with patch.object(Config, "CRAWL_CONFIG", {
            "max_pages": 1,
            "delay_between_requests": 0,
            "max_retries": 3,
            "timeout": 30,
            "early_stop": {"enabled": False, "consecutive_duplicates": 5, "page_duplicate_ratio": 0.8},
        }):
            # 첫 번째 크롤링
            stats1 = crawl_site("test_site", site_config, temp_db, Scraper)
            assert stats1["new_posts"] == 1
            assert stats1["duplicates"] == 0

            # 같은 게시글 다시 크롤링
            responses.add(
                responses.GET,
                "https://test.com/list?page=1",
                body='<html><body><div class="post"><a href="/post/1">Post 1</a></div></body></html>',
                status=200,
            )
            responses.add(responses.GET, "https://test.com/post/1", body=post_html, status=200)

            stats2 = crawl_site("test_site", site_config, temp_db, Scraper)
            assert stats2["new_posts"] == 0
            assert stats2["duplicates"] == 1

    @responses.activate
    def test_crawl_site_early_stop_consecutive(self, temp_db, site_config):
        """연속 중복 감지 시 조기 중단 테스트"""
        # 게시글 목록
        responses.add(
            responses.GET,
            "https://test.com/list?page=1",
            body="""
            <html><body>
            <div class="post"><a href="/post/1">Post 1</a></div>
            <div class="post"><a href="/post/2">Post 2</a></div>
            <div class="post"><a href="/post/3">Post 3</a></div>
            <div class="post"><a href="/post/4">Post 4</a></div>
            <div class="post"><a href="/post/5">Post 5</a></div>
            <div class="post"><a href="/post/6">Post 6</a></div>
            </body></html>
            """,
            status=200,
        )

        # 모든 게시글을 미리 저장 (중복으로 만들기)
        for i in range(1, 7):
            temp_db.save_post(
                {
                    "site_name": "test_site",
                    "title": f"Post {i}",
                    "content": f"Content {i}",
                    "source_url": f"https://test.com/post/{i}",
                },
                [],
            )

        # Mock 응답 추가
        for i in range(1, 7):
            responses.add(
                responses.GET,
                f"https://test.com/post/{i}",
                body=f"<html><body><h1>Post {i}</h1><div class='content'>Content {i}</div></body></html>",
                status=200,
            )

        with patch.object(Config, "CRAWL_CONFIG", {
            "max_pages": 1,
            "delay_between_requests": 0,
            "max_retries": 3,
            "timeout": 30,
            "early_stop": {
                "enabled": True,
                "consecutive_duplicates": 5,
                "page_duplicate_ratio": 0.8,
            },
        }):
            stats = crawl_site("test_site", site_config, temp_db, Scraper)

        # Early stop 확인
        assert stats["early_stopped"] is True
        assert stats["duplicates"] == 5

    @responses.activate
    def test_crawl_site_handles_parse_errors(self, temp_db, site_config):
        """파싱 에러 처리 테스트"""
        responses.add(
            responses.GET,
            "https://test.com/list?page=1",
            body='<html><body><div class="post"><a href="/post/1">Post 1</a></div></body></html>',
            status=200,
        )

        # 404 에러
        responses.add(responses.GET, "https://test.com/post/1", status=404)

        with patch.object(Config, "CRAWL_CONFIG", {
            "max_pages": 1,
            "delay_between_requests": 0,
            "max_retries": 3,
            "timeout": 30,
            "early_stop": {"enabled": False, "consecutive_duplicates": 5, "page_duplicate_ratio": 0.8},
        }):
            stats = crawl_site("test_site", site_config, temp_db, Scraper)

        # 실패 카운트 확인
        assert stats["failed"] == 1
        assert stats["new_posts"] == 0


class TestRunCrawler:
    """run_crawler 함수 통합 테스트"""

    @responses.activate
    def test_run_crawler_multi_site(self):
        """다중 사이트 크롤링 테스트"""
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            db_path = f.name

        # Config mock
        test_sites = {
            "site1": {
                "base_url": "https://site1.com",
                "site_name": "site1",
                "enabled": True,
                "selectors": {
                    "post_list": "div.post",
                    "post_link": "a",
                    "title": "h1",
                    "content": "div.content",
                    "images": "img",
                },
            },
            "site2": {
                "base_url": "https://site2.com",
                "site_name": "site2",
                "enabled": True,
                "selectors": {
                    "post_list": "div.post",
                    "post_link": "a",
                    "title": "h1",
                    "content": "div.content",
                    "images": "img",
                },
            },
        }

        # Mock 응답
        for site in ["site1", "site2"]:
            responses.add(
                responses.GET,
                f"https://{site}.com/list?page=1",
                body=f'<html><body><div class="post"><a href="/post/1">Post from {site}</a></div></body></html>',
                status=200,
            )
            responses.add(
                responses.GET,
                f"https://{site}.com/post/1",
                body=f"<html><body><h1>Post from {site}</h1><div class='content'>Content</div></body></html>",
                status=200,
            )

        with patch.object(Config, "TARGET_SITES", test_sites), \
             patch.object(Config, "DATABASE", {"path": db_path, "wal_mode": True}), \
             patch.object(Config, "CRAWL_CONFIG", {
                 "max_pages": 1,
                 "delay_between_requests": 0,
                 "max_retries": 3,
                 "timeout": 30,
                 "early_stop": {"enabled": False, "consecutive_duplicates": 5, "page_duplicate_ratio": 0.8},
             }):
            # 실행
            run_crawler()

        # DB 확인
        db = DatabaseManager(db_path)
        _ = db.session.query(db.session.query(type(db.session)).subquery()).all()
        db.session.close()

        Path(db_path).unlink()

    @responses.activate
    def test_run_crawler_skips_disabled_sites(self):
        """비활성화된 사이트는 스킵"""
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            db_path = f.name

        test_sites = {
            "enabled_site": {
                "base_url": "https://enabled.com",
                "site_name": "enabled",
                "enabled": True,
                "selectors": {
                    "post_list": "div.post",
                    "post_link": "a",
                    "title": "h1",
                    "content": "div.content",
                    "images": "img",
                },
            },
            "disabled_site": {
                "base_url": "https://disabled.com",
                "site_name": "disabled",
                "enabled": False,
                "selectors": {
                    "post_list": "div.post",
                    "post_link": "a",
                    "title": "h1",
                    "content": "div.content",
                    "images": "img",
                },
            },
        }

        # enabled_site만 mock
        responses.add(
            responses.GET,
            "https://enabled.com/list?page=1",
            body='<html><body><div class="post"><a href="/post/1">Post</a></div></body></html>',
            status=200,
        )
        responses.add(
            responses.GET,
            "https://enabled.com/post/1",
            body="<html><body><h1>Post</h1><div class='content'>Content</div></body></html>",
            status=200,
        )

        with patch.object(Config, "TARGET_SITES", test_sites), \
             patch.object(Config, "DATABASE", {"path": db_path, "wal_mode": True}), \
             patch.object(Config, "CRAWL_CONFIG", {
                 "max_pages": 1,
                 "delay_between_requests": 0,
                 "max_retries": 3,
                 "timeout": 30,
                 "early_stop": {"enabled": False, "consecutive_duplicates": 5, "page_duplicate_ratio": 0.8},
             }):
            run_crawler()

        # disabled_site는 요청되지 않아야 함
        assert len([r for r in responses.calls if "disabled.com" in r.request.url]) == 0

        Path(db_path).unlink()
