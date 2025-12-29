"""
pytest 설정 및 공통 fixture

이 파일은 모든 테스트에서 사용할 수 있는 공통 fixture를 정의합니다.
"""

import sys
from pathlib import Path

import pytest

# 프로젝트 루트를 Python path에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from core.scraper import Scraper  # noqa: E402
from core.storage import DatabaseManager  # noqa: E402


@pytest.fixture
def db():
    """테스트용 in-memory 데이터베이스"""
    db_manager = DatabaseManager(":memory:")
    yield db_manager
    db_manager.session.close()


@pytest.fixture
def scraper():
    """테스트용 Scraper 인스턴스"""
    return Scraper(
        base_url="https://example.com",
        selectors={
            "post_list": "div.post-item",
            "post_link": "a.title",
            "title": "h2.title",
            "content": "div.content",
            "images": "div.content img",  # content 내의 img 태그
            "date": "span.date",
        },
    )


@pytest.fixture
def sample_post_html():
    """샘플 게시글 HTML"""
    return """
    <html>
        <head><title>Test Post</title></head>
        <body>
            <h2 class="title">강아지가 밥그릇 엎음ㅋㅋ</h2>
            <div class="content">
                <p>오늘 우리집 강아지가 밥그릇을 엎었어요</p>
                <img src="/images/dog1.jpg" alt="강아지1">
                <img src="/images/dog2.jpg" alt="강아지2">
            </div>
            <span class="date">2025-12-17</span>
        </body>
    </html>
    """


@pytest.fixture
def sample_list_html():
    """샘플 목록 페이지 HTML"""
    return """
    <html>
        <body>
            <div class="post-list">
                <div class="post-item">
                    <a class="title" href="/post/1">첫 번째 게시글</a>
                </div>
                <div class="post-item">
                    <a class="title" href="/post/2">두 번째 게시글</a>
                </div>
                <div class="post-item">
                    <a class="title" href="/post/3">세 번째 게시글</a>
                </div>
            </div>
        </body>
    </html>
    """


@pytest.fixture
def fake_image_bytes():
    """테스트용 가짜 이미지 바이트"""
    import io

    from PIL import Image as PILImage

    img = PILImage.new("RGB", (100, 100), color="red")
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()
