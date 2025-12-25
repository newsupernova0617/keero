"""
데이터베이스 및 R2 저장 모듈

역할:
- SQLAlchemy ORM을 통한 데이터베이스 관리
- 게시글 메타데이터 저장
- 이미지 다운로드 및 R2 업로드
- 중복 데이터 방지
"""

import hashlib
import io
import re
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple

import imagehash
from PIL import Image as PILImage
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    create_engine,
    text,
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()


class Post(Base):
    """게시글 모델"""

    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    site_name = Column(String(50), nullable=False)
    title = Column(Text, nullable=False)
    content = Column(Text)
    content_html = Column(Text)  # HTML with preserved structure
    content_hash = Column(String(64), index=True)
    source_url = Column(Text, unique=True, nullable=False)
    created_at = Column(DateTime)
    crawled_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # 중복/관련 글 관리
    related_post_id = Column(Integer, ForeignKey("posts.id"))

    # 관계 설정
    images = relationship("Image", back_populates="post", cascade="all, delete-orphan")
    related_posts = relationship("Post", remote_side=[id], backref="derivatives")


class Image(Base):
    """이미지/GIF/동영상 모델"""

    __tablename__ = "images"

    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)

    # 미디어 타입 ('image', 'gif', 'video')
    media_type = Column(String(10), default="image")

    # 이미지 중복 감지용 해시
    md5_hash = Column(String(32), index=True)
    perceptual_hash = Column(String(16), index=True)

    # R2 저장 정보
    r2_key = Column(Text, nullable=False)
    r2_url = Column(Text, nullable=False)
    original_url = Column(Text)  # 원본 이미지 URL (R2 업로드 실패 시 fallback)
    order_index = Column(Integer, default=0)
    uploaded_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    is_similar_match = Column(Boolean, default=False)

    # GIF/동영상 메타데이터
    duration_seconds = Column(Integer)  # GIF/동영상 길이 (초)
    frame_count = Column(Integer)       # GIF 프레임 수

    # 최적화 정보 (R2 비용 추적용)
    original_size_bytes = Column(Integer)    # 원본 용량
    optimized_size_bytes = Column(Integer)   # 최적화 후 용량
    original_format = Column(String(10))     # 원본 포맷 (jpg, png, gif, mp4 등)
    optimized_format = Column(String(10))    # 최적화 포맷 (webp, mp4 등)
    
    # 이미지 크기 정보
    width = Column(Integer)      # 이미지 가로 크기 (px)
    height = Column(Integer)     # 이미지 세로 크기 (px)
    file_size = Column(Integer)  # 파일 크기 (bytes) - optimized_size_bytes와 동일

    post = relationship("Post", back_populates="images")



def normalize_text(text: str) -> str:
    """텍스트 정규화 (중복 감지용)"""
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[ㅋㅎ!?.~]+", "", text)
    text = text.replace(".", "").replace(",", "")
    return text.strip()


def generate_content_hash(title: str, content: str) -> str:
    """정규화된 텍스트로 해시 생성"""
    normalized = normalize_text(f"{title}{content}")
    return hashlib.md5(normalized.encode()).hexdigest()


def get_image_hash(image_data: bytes) -> Tuple[str, str]:
    """
    이미지 해시 2개 반환:
    1. MD5: 정확히 같은 파일용
    2. pHash: 시각적으로 유사한 이미지용
    """
    md5_hash = hashlib.md5(image_data).hexdigest()
    image = PILImage.open(io.BytesIO(image_data))
    phash = str(imagehash.phash(image))
    return md5_hash, phash


def replace_image_urls_in_html(html: str, image_mapping: Dict[str, str]) -> str:
    """
    HTML 내 이미지 URL을 R2 URL로 치환하고 UI 아이콘 제거
    
    Args:
        html: 원본 HTML
        image_mapping: {원본_URL: R2_URL} 매핑
    
    Returns:
        이미지 URL이 R2 URL로 치환되고 UI 아이콘이 제거된 HTML
    """
    from bs4 import BeautifulSoup
    from urllib.parse import urlparse
    
    if not html or not image_mapping:
        return html
    
    soup = BeautifulSoup(html, 'lxml')
    
    # URL 정규화 함수 (프로토콜 차이 무시)
    def normalize_url(url: str) -> str:
        """프로토콜을 제거하고 URL을 정규화"""
        if url.startswith('//'):
            url = 'https:' + url
        return url.replace('https://', '').replace('http://', '')
    
    # 정규화된 매핑 생성
    normalized_mapping = {}
    for original_url, r2_url in image_mapping.items():
        normalized_key = normalize_url(original_url)
        normalized_mapping[normalized_key] = r2_url
    
    # 1단계: 이미지 URL을 R2 URL로 치환
    for img in soup.find_all('img'):
        # Lazy loading 처리: data-original 우선 확인 (FMKorea 등)
        original_src = img.get('data-original') or img.get('src')
        if original_src:
            # 상대 경로나 프로토콜 상대 경로 처리
            normalized_src = normalize_url(original_src)
            
            if normalized_src in normalized_mapping:
                # src 속성을 R2 URL로 교체
                img['src'] = normalized_mapping[normalized_src]
                # data-original 속성 제거 (더 이상 필요 없음)
                if img.get('data-original'):
                    del img['data-original']
    
    # 2단계: UI 아이콘 및 R2로 치환되지 않은 이미지 제거
    for img in soup.find_all('img'):
        src = img.get('src', '')
        # R2 URL이 아니면 제거 (상대 경로, /images/, icon_ 등)
        if 'r2.dev' not in src:
            img.decompose()
    
    # 3단계: 비디오 URL을 R2 URL로 치환
    for video in soup.find_all('video'):
        original_src = video.get('src')
        if original_src:
            normalized_src = normalize_url(original_src)
            if normalized_src in normalized_mapping:
                video['src'] = normalized_mapping[normalized_src]
        
        # <source> 태그도 처리
        for source in video.find_all('source'):
            original_src = source.get('src')
            if original_src:
                normalized_src = normalize_url(original_src)
                if normalized_src in normalized_mapping:
                    source['src'] = normalized_mapping[normalized_src]
    
    # 4단계: 이미지를 감싸는 <a> 태그의 href도 R2 URL로 치환
    for a in soup.find_all('a'):
        href = a.get('href')
        if href:
            normalized_href = normalize_url(href)
            if normalized_href in normalized_mapping:
                a['href'] = normalized_mapping[normalized_href]
    
    return str(soup)


def clean_html(html: str) -> str:
    """
    HTML 정리 및 보안 처리
    - 위험한 태그 제거 (script, iframe, embed 등)
    - 외부 스타일시트 제거
    - 불필요한 속성 제거 (onclick, onerror 등)
    
    Args:
        html: 원본 HTML
    
    Returns:
        정리된 안전한 HTML
    """
    from bs4 import BeautifulSoup
    
    if not html:
        return ""
    
    soup = BeautifulSoup(html, 'lxml')
    
    # 위험한 태그 제거
    for tag in soup.find_all(['script', 'iframe', 'embed', 'object', 'style', 'link', 'meta', 'head']):
        tag.decompose()
    
    # 허용할 속성만 남기고 모두 제거 (디자인 일관성 및 보안)
    allowed_attrs = ['src', 'href', 'alt', 'title']
    for tag in soup.find_all(True):
        tag.attrs = {k: v for k, v in tag.attrs.items() if k in allowed_attrs}
    
    # body 태그가 있으면 그 내용만 반환, 없으면 전체 반환
    body = soup.find('body')
    if body:
        return ''.join(str(child) for child in body.children)
    
    return str(soup)


class DatabaseManager:
    """SQLAlchemy를 이용한 데이터베이스 관리"""

    def __init__(self, db_path: str, r2_config: Optional[Dict] = None, auto_commit: bool = True):
        """
        DB 엔진 및 세션 초기화
        
        Args:
            db_path: SQLite 데이터베이스 경로
            r2_config: R2 설정 딕셔너리 (account_id, access_key_id, secret_access_key, bucket_name)
            auto_commit: 자동 커밋 여부 (False면 flush() 호출 시에만 커밋)
        """
        self.auto_commit = auto_commit
        engine = create_engine(f"sqlite:///{db_path}")

        # SQLite 최적화 설정
        with engine.connect() as connection:
            # WAL 모드: 동시 읽기/쓰기 지원
            connection.execute(text("PRAGMA journal_mode=WAL"))
            # 동기화 수준: NORMAL (성능과 안정성 균형)
            connection.execute(text("PRAGMA synchronous=NORMAL"))
            # 캐시 크기: 64MB (음수 = KB 단위)
            connection.execute(text("PRAGMA cache_size=-64000"))
            # 임시 테이블: 메모리에 저장
            connection.execute(text("PRAGMA temp_store=MEMORY"))
            # 메모리 매핑: 256MB
            connection.execute(text("PRAGMA mmap_size=268435456"))
            # 잠금 대기 시간: 5초
            connection.execute(text("PRAGMA busy_timeout=5000"))
            connection.commit()

        Base.metadata.create_all(engine)
        
        # FTS5 가상 테이블 생성 (검색용)
        with engine.connect() as connection:
            # FTS5 테이블 생성 (이미 있으면 무시)
            connection.execute(text("""
                CREATE VIRTUAL TABLE IF NOT EXISTS posts_fts USING fts5(
                    title,
                    content,
                    content='posts',
                    content_rowid='id'
                )
            """))
            
            # 자동 동기화 트리거들
            # INSERT 트리거
            connection.execute(text("""
                CREATE TRIGGER IF NOT EXISTS posts_fts_insert 
                AFTER INSERT ON posts BEGIN
                    INSERT INTO posts_fts(rowid, title, content) 
                    VALUES (new.id, new.title, new.content);
                END
            """))
            
            # UPDATE 트리거
            connection.execute(text("""
                CREATE TRIGGER IF NOT EXISTS posts_fts_update 
                AFTER UPDATE ON posts BEGIN
                    INSERT INTO posts_fts(posts_fts, rowid, title, content) 
                    VALUES ('delete', old.id, old.title, old.content);
                    INSERT INTO posts_fts(rowid, title, content) 
                    VALUES (new.id, new.title, new.content);
                END
            """))
            
            # DELETE 트리거
            connection.execute(text("""
                CREATE TRIGGER IF NOT EXISTS posts_fts_delete 
                AFTER DELETE ON posts BEGIN
                    INSERT INTO posts_fts(posts_fts, rowid, title, content) 
                    VALUES ('delete', old.id, old.title, old.content);
                END
            """))
            
            connection.commit()
        
        Session = sessionmaker(bind=engine)
        self.session = Session()
        
        # R2 Uploader 초기화 (설정이 있으면)
        self.r2_uploader = None
        if r2_config:
            self.r2_uploader = R2Uploader(
                account_id=r2_config["account_id"],
                access_key=r2_config["access_key_id"],
                secret_key=r2_config["secret_access_key"],
                bucket_name=r2_config["bucket_name"],
                public_url=r2_config.get("public_url", ""),
            )

    def flush(self):
        """
        수동 커밋 (배치 모드에서 사용)
        
        batch_commit 모드에서는 자동 커밋하지 않고,
        이 메서드를 호출해야 DB에 반영됩니다.
        """
        self.session.commit()

    def save_post(self, post_data: Dict, image_urls: List[str]) -> Optional[int]:
        """
        게시글 저장 (중복 체크 + 관련글 연결)

        Returns:
            post_id: 저장된 게시글 ID (중복이면 None)
        """
        # URL 중복 체크
        existing = self.session.query(Post).filter_by(source_url=post_data["source_url"]).first()

        if existing:
            return None

        # content_hash 생성
        content_hash = generate_content_hash(post_data["title"], post_data["content"])

        # 관련 게시글 찾기 (같은 이미지 사용하는 기존 글)
        related_post = None
        if image_urls:
            # 첫 번째 이미지로 간단히 체크 (실제로는 모든 이미지 체크 가능)
            # TODO: 이미지 해시 기반 관련글 찾기는 나중에 구현
            pass

        # 새 게시글 생성
        post = Post(
            site_name=post_data["site_name"],
            title=post_data["title"],
            content=post_data["content"],
            content_hash=content_hash,
            source_url=post_data["source_url"],
            created_at=post_data.get("created_at"),
            related_post_id=related_post.id if related_post else None,
        )
        self.session.add(post)
        if self.auto_commit:
            self.session.commit()
        return post.id

    def save_post_with_html(self, post_data: Dict, image_urls: List[str]) -> Optional[int]:
        """
        게시글 저장 + 이미지 업로드 + HTML 내 URL 치환
        
        HTML content가 있는 경우:
        1. 게시글 저장 (content_html 포함)
        2. 이미지 업로드 및 URL 매핑 생성
        3. HTML 내 이미지 URL을 R2 URL로 치환
        4. DB 업데이트
        
        Args:
            post_data: 게시글 데이터 (content_html 포함)
            image_urls: 이미지 URL 리스트
        
        Returns:
            post_id: 저장된 게시글 ID (중복이면 None)
        """
        # URL 중복 체크
        existing = self.session.query(Post).filter_by(source_url=post_data["source_url"]).first()
        if existing:
            return None

        # content_hash 생성
        content_hash = generate_content_hash(post_data["title"], post_data["content"])

        # 관련 게시글 찾기
        related_post = None
        
        # 새 게시글 생성 (content_html 포함)
        post = Post(
            site_name=post_data["site_name"],
            title=post_data["title"],
            content=post_data["content"],
            content_html=post_data.get("content_html"),  # HTML 저장
            content_hash=content_hash,
            source_url=post_data["source_url"],
            created_at=post_data.get("created_at"),
            related_post_id=related_post.id if related_post else None,
        )
        self.session.add(post)
        if self.auto_commit:
            self.session.commit()
        else:
            # 배치 모드: flush를 통해 post.id를 즉시 얻기 (커밋은 아님)
            self.session.flush()
        post_id = post.id

        # 이미지 업로드 및 URL 매핑 생성
        image_mapping = {}
        if image_urls:
            for idx, img_url in enumerate(image_urls):
                try:
                    image = self.save_image_smart(post_id, img_url, idx)
                    image_mapping[img_url] = image.r2_url
                except Exception as e:
                    print(f"Warning: Failed to save image {img_url}: {e}")
                    continue

        # HTML 내 이미지 URL 치환
        if post_data.get("content_html") and image_mapping:
            updated_html = replace_image_urls_in_html(
                post_data["content_html"],
                image_mapping
            )
            # DB 업데이트
            post.content_html = updated_html
            if self.auto_commit:
                self.session.commit()

        return post_id

    def save_image_smart(self, post_id: int, image_url: str, order_index: int) -> Image:
        """
        이미지/동영상 저장 (2단계 중복 체크)
        1. MD5로 정확히 같은 파일 찾기
        2. pHash로 유사 이미지 찾기
        3. R2 업로드 실패 시에도 original_url 저장
        """
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 방어 로직: placeholder/transparent.gif 필터링
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # extract_images()에서 이미 필터링했지만, 혹시 모를 경우를 대비
        if 'transparent.gif' in image_url.lower() or 'placeholder' in image_url.lower():
            raise Exception(f"Placeholder image detected and rejected: {image_url}")
        
        # UI 아이콘 이미지 필터링 (/images/ 경로)
        if '/images/' in image_url:
            raise Exception(f"UI icon image detected and rejected: {image_url}")
        
        # URL 확장자로 동영상 파일 감지
        video_extensions = ('.mp4', '.webm', '.mov', '.avi', '.mkv', '.flv')
        url_lower = image_url.lower()
        is_video = any(url_lower.endswith(ext) or f'{ext}?' in url_lower for ext in video_extensions)
        
        # 동영상 파일은 바로 동영상 처리
        if is_video:
            print(f"Detected video file: {image_url}")
            video_data = self.download_image(image_url)  # download_image는 범용 다운로드 함수
            md5_hash = hashlib.md5(video_data).hexdigest()
            
            # 동영상 최적화
            try:
                optimized_data, original_format, optimized_format, original_size, optimized_size = self.optimize_video(video_data, url_lower.split('.')[-1].split('?')[0])
            except Exception as e:
                print(f"Warning: Video optimization failed for {image_url}: {e}")
                optimized_data = video_data
                original_format = 'mp4'
                optimized_format = 'mp4'
                original_size = len(video_data)
                optimized_size = len(video_data)
            
            # 이미지 크기 정보 추출 (동영상은 ffprobe 필요, 일단 None)
            width, height = None, None
            
            # R2 키 생성
            r2_key = f"images/{md5_hash}.{optimized_format}"
            r2_url = None
            
            try:
                r2_url = self.upload_to_r2(optimized_data, r2_key)
            except Exception as e:
                print(f"Warning: R2 upload failed for {image_url}, using original URL: {e}")
                r2_key = ""
                r2_url = image_url
            
            image = Image(
                post_id=post_id,
                md5_hash=md5_hash,
                perceptual_hash=None,  # 동영상은 pHash 없음
                r2_key=r2_key,
                r2_url=r2_url,
                original_url=image_url,
                order_index=order_index,
                is_similar_match=False,
                original_format=original_format,
                optimized_format=optimized_format,
                original_size_bytes=original_size,
                optimized_size_bytes=optimized_size,
                width=width,
                height=height,
            )
            self.session.add(image)
            if self.auto_commit:
                self.session.commit()
            return image
        
        # 이미지 다운로드
        img_data = self.download_image(image_url)

        # 해시 생성
        md5_hash, phash = get_image_hash(img_data)

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 1단계: 정확히 같은 파일 찾기 (MD5)
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        exact_match = self.session.query(Image).filter_by(md5_hash=md5_hash).first()

        if exact_match:
            # 완전히 같은 파일! R2 재사용
            image = Image(
                post_id=post_id,
                md5_hash=md5_hash,
                perceptual_hash=phash,
                r2_key=exact_match.r2_key,
                r2_url=exact_match.r2_url,
                original_url=image_url,  # 원본 URL 저장
                order_index=order_index,
                is_similar_match=False,
            )
            self.session.add(image)
            if self.auto_commit:
                self.session.commit()
            return image

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 2단계: 유사한 이미지 찾기 (pHash)
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        all_images = self.session.query(Image.perceptual_hash, Image.r2_key, Image.r2_url).all()

        for stored_phash, r2_key, r2_url in all_images:
            if not stored_phash:
                continue

            # 해밍 거리 계산
            h1 = imagehash.hex_to_hash(phash)
            h2 = imagehash.hex_to_hash(stored_phash)
            distance = h1 - h2

            if distance <= 5:  # 5비트 이하 차이 = 유사
                image = Image(
                    post_id=post_id,
                    md5_hash=md5_hash,
                    perceptual_hash=phash,
                    r2_key=r2_key,  # 유사 이미지의 R2 재사용
                    r2_url=r2_url,
                    original_url=image_url,  # 원본 URL 저장
                    order_index=order_index,
                    is_similar_match=True,
                )
                self.session.add(image)
                if self.auto_commit:
                    self.session.commit()
                return image

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 3단계: 새 이미지 → 최적화 → R2 업로드 (실패해도 original_url 저장)
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        
        # 이미지 최적화 (WebP 변환)
        try:
            optimized_data, original_format, optimized_format, original_size, optimized_size = self.optimize_image(img_data)
        except Exception as e:
            print(f"Warning: Image optimization failed for {image_url}, using original: {e}")
            optimized_data = img_data
            original_format = 'unknown'
            optimized_format = 'jpg'
            original_size = len(img_data)
            optimized_size = len(img_data)
        
        # 이미지 크기 정보 추출
        try:
            img_pil = PILImage.open(io.BytesIO(optimized_data))
            width, height = img_pil.size
        except:
            width, height = None, None
        
        # R2 키 생성 (최적화된 포맷 사용)
        r2_key = f"images/{md5_hash}.{optimized_format}"
        r2_url = None
        
        try:
            r2_url = self.upload_to_r2(optimized_data, r2_key)
        except Exception as e:
            # R2 업로드 실패 시에도 original_url로 저장
            print(f"Warning: R2 upload failed for {image_url}, using original URL: {e}")
            r2_key = ""  # R2 key는 비워둠
            r2_url = image_url  # 원본 URL을 r2_url로 사용

        image = Image(
            post_id=post_id,
            md5_hash=md5_hash,
            perceptual_hash=phash,
            r2_key=r2_key,
            r2_url=r2_url,
            original_url=image_url,  # 원본 URL 항상 저장
            order_index=order_index,
            is_similar_match=False,
            # 최적화 정보 저장
            original_format=original_format,
            optimized_format=optimized_format,
            original_size_bytes=original_size,
            optimized_size_bytes=optimized_size,
            width=width,
            height=height,
        )
        self.session.add(image)
        if self.auto_commit:
            self.session.commit()
        return image

    def download_image(self, url: str) -> bytes:
        """이미지 다운로드"""
        import requests

        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            return response.content
        except requests.RequestException as e:
            raise Exception(f"Failed to download image from {url}: {e}") from e

    def optimize_image(self, image_data: bytes) -> tuple[bytes, str, str, int, int]:
        """
        이미지 최적화 (WebP 변환)
        
        Args:
            image_data: 원본 이미지 데이터
        
        Returns:
            (optimized_data, original_format, optimized_format, original_size, optimized_size)
        """
        from PIL import Image
        import io
        
        original_size = len(image_data)
        
        # 이미지 열기
        img = PILImage.open(io.BytesIO(image_data))
        original_format = img.format.lower() if img.format else 'unknown'
        
        # GIF는 동영상으로 변환 (VP9 WebM)
        if original_format == 'gif':
            try:
                # GIF가 애니메이션인지 확인 (여러 프레임이 있는지)
                is_animated = getattr(img, 'is_animated', False)
                n_frames = getattr(img, 'n_frames', 1)
                
                if is_animated or n_frames > 1:
                    # 애니메이션 GIF → VP9 WebM 변환
                    print(f"Converting animated GIF ({n_frames} frames) to VP9 WebM...")
                    return self.optimize_video(image_data, 'gif')
            except Exception as e:
                print(f"GIF animation check failed: {e}")
            # 정적 GIF는 일반 이미지로 처리
        
        # RGBA 이미지는 RGB로 변환 (WebP는 투명도 지원하지만 파일 크기를 위해)
        if img.mode in ('RGBA', 'LA', 'P'):
            # 투명 배경을 흰색으로
            background = PILImage.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        
        # 이미지 크기 제한 (최대 2000px)
        max_dimension = 2000
        if max(img.size) > max_dimension:
            ratio = max_dimension / max(img.size)
            new_size = tuple(int(dim * ratio) for dim in img.size)
            img = img.resize(new_size, PILImage.Resampling.LANCZOS)
        
        # WebP로 변환
        output = io.BytesIO()
        img.save(output, format='WEBP', quality=85, method=6)
        optimized_data = output.getvalue()
        optimized_size = len(optimized_data)
        
        return optimized_data, original_format, 'webp', original_size, optimized_size

    def optimize_video(self, video_data: bytes, original_format: str) -> tuple[bytes, str, str, int, int]:
        """
        동영상/GIF 최적화 (VP9 WebM 변환)
        
        Args:
            video_data: 원본 동영상/GIF 데이터
            original_format: 원본 포맷 ('gif', 'mp4', 'webm' 등)
        
        Returns:
            (optimized_data, original_format, optimized_format, original_size, optimized_size)
        """
        import ffmpeg
        import tempfile
        import os
        import subprocess
        
        original_size = len(video_data)
        
        # 임시 파일 생성
        with tempfile.NamedTemporaryFile(suffix=f'.{original_format}', delete=False) as input_file:
            input_file.write(video_data)
            input_path = input_file.name
        
        output_path = input_path.replace(f'.{original_format}', '.webm')
        
        try:
            # ffmpeg-python을 사용한 VP9 WebM 변환
            # 설정:
            # - VP9 코덱
            # - CRF 31 (품질, 낮을수록 고품질, 23-31 권장)
            # - 2-pass 인코딩 (더 나은 압축)
            # - 최대 해상도 1080p
            # - 오디오: Opus 코덱 (WebM 표준)
            
            # 입력 비디오 정보 가져오기
            probe = ffmpeg.probe(input_path)
            video_info = next(s for s in probe['streams'] if s['codec_type'] == 'video')
            width = int(video_info['width'])
            height = int(video_info['height'])
            duration = float(probe['format'].get('duration', 0))
            
            # 해상도 제한 (최대 1080p)
            max_height = 1080
            if height > max_height:
                scale_ratio = max_height / height
                new_width = int(width * scale_ratio)
                new_height = max_height
                # 2의 배수로 맞추기 (VP9 요구사항)
                new_width = new_width - (new_width % 2)
                new_height = new_height - (new_height % 2)
                scale_filter = f'scale={new_width}:{new_height}'
            else:
                scale_filter = None
            
            # ffmpeg 명령 구성 (subprocess 사용)
            cmd = [
                'ffmpeg',
                '-i', input_path,
                '-vcodec', 'libvpx-vp9',
                '-crf', '31',
                '-b:v', '0',
                '-cpu-used', '4',
                '-row-mt', '1',
                '-tile-columns', '2',
                '-threads', '4',
            ]
            
            # 해상도 제한이 필요한 경우
            if scale_filter:
                cmd.extend(['-vf', f'scale={new_width}:{new_height}'])
            
            # 오디오 처리
            if 'audio' in [s['codec_type'] for s in probe['streams']]:
                cmd.extend(['-acodec', 'libopus', '-b:a', '64k'])
            
            cmd.extend(['-y', output_path])  # -y: 덮어쓰기
            
            # 실행
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                raise Exception(f"ffmpeg failed with code {result.returncode}: {result.stderr[:500]}")
            
            # 결과 파일 읽기
            with open(output_path, 'rb') as f:
                optimized_data = f.read()
            
            optimized_size = len(optimized_data)
            
            return optimized_data, original_format, 'webm', original_size, optimized_size
            
        except Exception as e:
            print(f"Warning: Video optimization failed: {e}")
            # 실패 시 원본 반환
            return video_data, original_format, original_format, original_size, original_size
            
        finally:
            # 임시 파일 삭제
            try:
                os.unlink(input_path)
                if os.path.exists(output_path):
                    os.unlink(output_path)
            except:
                pass

    def upload_to_r2(self, data: bytes, key: str) -> str:
        """
        R2에 이미지 업로드 (R2Uploader 사용)
        
        Args:
            data: 업로드할 이미지 데이터
            key: R2 객체 키
        
        Returns:
            R2 공개 URL
        
        Raises:
            Exception: R2Uploader가 초기화되지 않았거나 업로드 실패 시
        """
        if not self.r2_uploader:
            raise Exception("R2Uploader is not initialized. Provide r2_config in __init__.")
        
        return self.r2_uploader.upload(data, key)


class R2Uploader:
    """Cloudflare R2 업로드 관리"""

    def __init__(self, account_id: str, access_key: str, secret_key: str, bucket_name: str, public_url: str = ""):
        """
        R2 클라이언트 초기화
        
        Args:
            account_id: R2 계정 ID
            access_key: R2 Access Key ID
            secret_key: R2 Secret Access Key
            bucket_name: R2 버킷 이름
            public_url: R2 공개 URL (Public Bucket URL 또는 Custom Domain)
        """
        import boto3

        self.bucket_name = bucket_name
        self.account_id = account_id
        self.public_url = public_url.rstrip("/")  # 끝의 슬래시 제거
        
        # R2 S3-compatible 클라이언트 초기화
        self.s3_client = boto3.client(
            "s3",
            endpoint_url=f"https://{account_id}.r2.cloudflarestorage.com",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
        )

    def upload(self, file_data: bytes, key: str) -> str:
        """
        파일 업로드 및 URL 반환
        
        Args:
            file_data: 업로드할 파일 데이터
            key: R2 객체 키 (예: "images/abc123.jpg")
        
        Returns:
            공개 URL (R2 public domain 설정 시)
        
        Raises:
            Exception: 업로드 실패 시
        """
        try:
            # R2에 업로드
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=key,
                Body=file_data,
                ContentType=self._guess_content_type(key),
            )

            # 공개 URL 생성
            if self.public_url:
                # 환경 변수에서 제공된 공개 URL 사용
                r2_url = f"{self.public_url}/{key}"
            else:
                # Fallback: 기본 r2.dev URL (인증 필요할 수 있음)
                r2_url = f"https://pub-{self.account_id}.r2.dev/{key}"
            return r2_url
        except Exception as e:
            raise Exception(f"Failed to upload to R2: {e}") from e

    def _guess_content_type(self, key: str) -> str:
        """파일 확장자로 Content-Type 추측"""
        if key.endswith(".jpg") or key.endswith(".jpeg"):
            return "image/jpeg"
        elif key.endswith(".png"):
            return "image/png"
        elif key.endswith(".gif"):
            return "image/gif"
        elif key.endswith(".webp"):
            return "image/webp"
        elif key.endswith(".webm"):
            return "video/webm"
        elif key.endswith(".mp4"):
            return "video/mp4"
        else:
            return "application/octet-stream"

