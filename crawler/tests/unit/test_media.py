#!/usr/bin/env python3
"""
GIF/동영상 최적화 테스트 스크립트

사용법:
    python test_media.py
"""

import os
from dotenv import load_dotenv
from core.storage import DatabaseManager

# 환경 변수 로드
load_dotenv()

# 테스트할 미디어 URL들
TEST_MEDIA = [
    # 애니메이션 GIF
    "https://i.imgur.com/example.gif",  # 실제 GIF URL로 교체 필요
    
    # MP4 동영상
    "https://i2.ruliweb.com/ori/25/12/23/19b4a57647c55a0ce.mp4",  # 루리웹 MP4
    
    # WebM 동영상
    # "https://example.com/video.webm",
]

def test_media_optimization():
    """미디어 최적화 테스트"""
    
    # DB 초기화
    db_path = os.getenv("DB_PATH", "../data/posts.db")
    
    # R2 설정
    r2_config = {
        "account_id": os.getenv("R2_ACCOUNT_ID"),
        "access_key_id": os.getenv("R2_ACCESS_KEY_ID"),
        "secret_access_key": os.getenv("R2_SECRET_ACCESS_KEY"),
        "bucket_name": os.getenv("R2_BUCKET_NAME"),
        "public_url": os.getenv("R2_PUBLIC_URL"),
    }
    
    db = DatabaseManager(db_path, r2_config=r2_config, auto_commit=True)
    
    print("=" * 60)
    print("🧪 GIF/동영상 최적화 테스트")
    print("=" * 60)
    
    # 테스트 게시글 생성
    post_data = {
        "site_name": "test",
        "title": "미디어 테스트 게시글",
        "content": "GIF/동영상 최적화 테스트",
        "content_html": "<p>테스트</p>",
        "source_url": "http://test.com/test",
        "created_at": None,
    }
    
    try:
        post_id = db.save_post_with_html(post_data, TEST_MEDIA)
        
        if post_id:
            print(f"\n✅ 게시글 저장 완료 (ID: {post_id})")
            
            # 저장된 이미지 확인
            from storage import Image
            images = db.session.query(Image).filter_by(post_id=post_id).all()
            
            print(f"\n📊 저장된 미디어: {len(images)}개")
            print("-" * 60)
            
            for idx, img in enumerate(images, 1):
                print(f"\n{idx}. {img.original_url}")
                print(f"   원본 포맷: {img.original_format}")
                print(f"   최적화 포맷: {img.optimized_format}")
                print(f"   원본 크기: {img.original_size_bytes:,} bytes")
                print(f"   최적화 크기: {img.optimized_size_bytes:,} bytes")
                
                if img.original_size_bytes and img.optimized_size_bytes:
                    reduction = (1 - img.optimized_size_bytes / img.original_size_bytes) * 100
                    print(f"   압축률: {reduction:.1f}% 감소")
                
                print(f"   R2 URL: {img.r2_url[:80]}..." if img.r2_url else "   R2 URL: None")
        else:
            print("❌ 게시글 저장 실패 (중복?)")
            
    except Exception as e:
        print(f"\n❌ 에러 발생: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    test_media_optimization()
