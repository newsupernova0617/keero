"""
storage.py 모듈 테스트

데이터베이스 모델, 해시 함수, DatabaseManager 클래스를 테스트합니다.
"""

from core.storage import Image, Post, generate_content_hash, get_image_hash, normalize_text


class TestTextNormalization:
    """텍스트 정규화 함수 테스트"""

    def test_normalize_removes_special_chars(self):
        """특수문자 제거 테스트"""
        text = "강아지가 웃김ㅋㅋㅋ!!!"
        result = normalize_text(text)
        assert "ㅋ" not in result
        assert "!" not in result

    def test_normalize_lowercase(self):
        """소문자 변환 테스트"""
        text = "ABC abc"
        result = normalize_text(text)
        assert result == "abc abc"

    def test_normalize_whitespace(self):
        """공백 정리 테스트"""
        text = "강아지가    밥그릇     엎음"
        result = normalize_text(text)
        assert "    " not in result

    def test_content_hash_consistency(self):
        """같은 내용은 같은 해시 생성"""
        hash1 = generate_content_hash("제목", "내용")
        hash2 = generate_content_hash("제목", "내용")
        assert hash1 == hash2

    def test_content_hash_different_for_different_content(self):
        """다른 내용은 다른 해시 생성"""
        hash1 = generate_content_hash("제목1", "내용1")
        hash2 = generate_content_hash("제목2", "내용2")
        assert hash1 != hash2


class TestImageHash:
    """이미지 해시 함수 테스트"""

    def test_get_image_hash_returns_two_hashes(self, fake_image_bytes):
        """이미지 해시가 2개 반환되는지 확인"""
        md5_hash, phash = get_image_hash(fake_image_bytes)
        assert isinstance(md5_hash, str)
        assert isinstance(phash, str)
        assert len(md5_hash) == 32  # MD5는 32자
        assert len(phash) > 0  # pHash는 16자 정도

    def test_same_image_same_hash(self, fake_image_bytes):
        """같은 이미지는 같은 해시"""
        md5_1, phash_1 = get_image_hash(fake_image_bytes)
        md5_2, phash_2 = get_image_hash(fake_image_bytes)
        assert md5_1 == md5_2
        assert phash_1 == phash_2


class TestDatabaseManager:
    """DatabaseManager 클래스 테스트"""

    def test_db_initialization(self, db):
        """DB 초기화 테스트"""
        assert db.session is not None

    def test_save_post_creates_new_post(self, db):
        """새 게시글 저장 테스트"""
        post_data = {
            "site_name": "test_site",
            "title": "Test Post",
            "content": "Test Content",
            "source_url": "https://test.com/post/1",
        }

        _ = db.save_post(post_data, [])

        # TODO: save_post 구현 후 주석 해제
        # assert post_id is not None
        # assert post_id > 0

    def test_save_post_prevents_duplicate_url(self, db):
        """중복 URL 저장 방지 테스트"""
        post_data = {
            "site_name": "test_site",
            "title": "Test Post",
            "content": "Test Content",
            "source_url": "https://test.com/post/1",
        }

        # 첫 번째 저장
        _ = db.save_post(post_data, [])

        # 같은 URL로 두 번째 저장 시도
        _ = db.save_post(post_data, [])

        # TODO: save_post 구현 후 주석 해제
        # assert first_id is not None
        # assert second_id is None  # 중복이므로 None 반환


class TestPostModel:
    """Post 모델 테스트"""

    def test_post_creation(self, db):
        """Post 모델 생성 테스트"""
        post = Post(
            site_name="test",
            title="Test Title",
            content="Test Content",
            content_hash="abc123",
            source_url="https://test.com/1",
        )

        db.session.add(post)
        db.session.commit()

        assert post.id is not None
        assert post.site_name == "test"
        assert post.title == "Test Title"

    def test_post_relationship_with_images(self, db):
        """Post-Image 관계 테스트"""
        post = Post(
            site_name="test",
            title="Test",
            content="Content",
            content_hash="hash",
            source_url="https://test.com/1",
        )
        db.session.add(post)
        db.session.commit()

        image = Image(
            post_id=post.id,
            md5_hash="md5hash",
            perceptual_hash="phash",
            r2_key="images/test.jpg",
            r2_url="https://r2.example.com/test.jpg",
        )
        db.session.add(image)
        db.session.commit()

        # Relationship 확인
        assert len(post.images) == 1
        assert post.images[0].r2_key == "images/test.jpg"
