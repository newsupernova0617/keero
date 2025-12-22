"""
HTML 처리 함수 테스트
"""
import pytest
from storage import clean_html, replace_image_urls_in_html


def test_clean_html_removes_dangerous_tags():
    """위험한 태그 제거 테스트"""
    html = '<p>안전한 텍스트</p><script>alert("XSS")</script><iframe src="evil.com"></iframe>'
    clean = clean_html(html)
    
    assert '<script>' not in clean
    assert '<iframe>' not in clean
    assert '안전한 텍스트' in clean


def test_clean_html_removes_dangerous_attributes():
    """위험한 속성 제거 테스트"""
    html = '<img src="test.jpg" onclick="alert(1)" onerror="hack()">'
    clean = clean_html(html)
    
    assert 'onclick' not in clean
    assert 'onerror' not in clean
    assert 'src="test.jpg"' in clean


def test_clean_html_preserves_safe_content():
    """안전한 콘텐츠 보존 테스트"""
    html = '''
    <p>텍스트입니다</p>
    <img src="image.jpg" alt="이미지">
    <a href="link.html" title="링크">링크</a>
    '''
    clean = clean_html(html)
    
    assert '텍스트입니다' in clean
    assert 'src="image.jpg"' in clean
    assert 'href="link.html"' in clean


def test_clean_html_empty_input():
    """빈 입력 테스트"""
    assert clean_html("") == ""
    assert clean_html(None) == ""


def test_replace_image_urls():
    """이미지 URL 치환 테스트"""
    html = '''
    <p>텍스트</p>
    <img src="http://old.com/img1.jpg">
    <p>더 많은 텍스트</p>
    <img src="http://old.com/img2.jpg">
    '''
    
    mapping = {
        "http://old.com/img1.jpg": "https://r2.dev/new1.jpg",
        "http://old.com/img2.jpg": "https://r2.dev/new2.jpg"
    }
    
    result = replace_image_urls_in_html(html, mapping)
    
    assert 'https://r2.dev/new1.jpg' in result
    assert 'https://r2.dev/new2.jpg' in result
    assert 'http://old.com/img1.jpg' not in result
    assert 'http://old.com/img2.jpg' not in result
    assert '텍스트' in result


def test_replace_image_urls_partial_match():
    """일부만 매칭되는 경우 테스트"""
    html = '''
    <img src="http://old.com/img1.jpg">
    <img src="http://old.com/img2.jpg">
    '''
    
    mapping = {
        "http://old.com/img1.jpg": "https://r2.dev/new1.jpg"
        # img2는 매핑 없음
    }
    
    result = replace_image_urls_in_html(html, mapping)
    
    assert 'https://r2.dev/new1.jpg' in result
    assert 'http://old.com/img2.jpg' in result  # 변경되지 않음


def test_replace_image_urls_empty_mapping():
    """빈 매핑 테스트"""
    html = '<img src="http://old.com/img.jpg">'
    result = replace_image_urls_in_html(html, {})
    
    assert result == html


def test_html_content_preservation_workflow():
    """전체 워크플로우 통합 테스트"""
    # 1. 원본 HTML (위험한 요소 포함)
    original_html = '''
    <p>게시글 내용입니다</p>
    <img src="http://original.com/image1.jpg" onclick="hack()">
    <script>alert("xss")</script>
    <p>더 많은 내용</p>
    <img src="http://original.com/image2.jpg">
    '''
    
    # 2. HTML 정리
    cleaned = clean_html(original_html)
    assert '<script>' not in cleaned
    assert 'onclick' not in cleaned
    assert '게시글 내용입니다' in cleaned
    
    # 3. 이미지 URL 치환
    mapping = {
        "http://original.com/image1.jpg": "https://r2.cdn.com/abc123.jpg",
        "http://original.com/image2.jpg": "https://r2.cdn.com/def456.jpg"
    }
    
    final_html = replace_image_urls_in_html(cleaned, mapping)
    
    # 4. 검증
    assert 'https://r2.cdn.com/abc123.jpg' in final_html
    assert 'https://r2.cdn.com/def456.jpg' in final_html
    assert 'http://original.com' not in final_html
    assert '게시글 내용입니다' in final_html
    assert '더 많은 내용' in final_html


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
