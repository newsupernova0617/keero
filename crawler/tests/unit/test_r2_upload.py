"""
R2 이미지 업로드 테스트 스크립트
"""
import sys
from pathlib import Path
from core.storage import DatabaseManager

from core.config import Config

# DB 초기화
db = DatabaseManager(db_path=Config.DATABASE["path"])

# 테스트용 게시글 ID (이미 존재하는 게시글)
test_post_id = 1

# Mock 이미지 파일 경로
test_image_path = Path(__file__).parent / "test_image.jpg"

print(f"Testing R2 upload with mock image: {test_image_path}")
print(f"Post ID: {test_post_id}")

try:
    # 이미지 업로드 시도
    with open(test_image_path, 'rb') as f:
        image_data = f.read()
    
    # R2에 업로드
    from storage import R2Uploader
    
    r2 = R2Uploader(
        account_id=Config.R2_CONFIG['account_id'],
        access_key=Config.R2_CONFIG['access_key_id'],
        secret_key=Config.R2_CONFIG['secret_access_key'],
        bucket_name=Config.R2_CONFIG['bucket_name']
    )
    
    # 테스트 파일명
    test_filename = "test/mock_image_001.jpg"
    
    print(f"Uploading to R2: {test_filename}")
    r2_url = r2.upload(image_data, test_filename)
    
    print(f"✅ SUCCESS! Image uploaded to: {r2_url}")
    
except Exception as e:
    print(f"❌ FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
