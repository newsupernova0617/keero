#!/usr/bin/env python3
"""
R2 버킷의 모든 이미지 삭제 스크립트
"""

import os
import boto3
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

def delete_all_r2_images():
    """R2 버킷의 images/ 폴더 내 모든 파일 삭제"""
    
    # R2 설정
    account_id = os.getenv("R2_ACCOUNT_ID")
    access_key = os.getenv("R2_ACCESS_KEY_ID")
    secret_key = os.getenv("R2_SECRET_ACCESS_KEY")
    bucket_name = os.getenv("R2_BUCKET_NAME")
    
    if not all([account_id, access_key, secret_key, bucket_name]):
        print("❌ R2 credentials가 설정되지 않았습니다.")
        return
    
    print(f"R2 버킷: {bucket_name}")
    print(f"Account ID: {account_id}")
    
    # S3 클라이언트 초기화
    s3_client = boto3.client(
        "s3",
        endpoint_url=f"https://{account_id}.r2.cloudflarestorage.com",
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
    )
    
    try:
        # images/ 폴더의 모든 객체 나열
        print("\n📋 이미지 목록 조회 중...")
        
        paginator = s3_client.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=bucket_name, Prefix='images/')
        
        objects_to_delete = []
        total_count = 0
        
        for page in pages:
            if 'Contents' in page:
                for obj in page['Contents']:
                    objects_to_delete.append({'Key': obj['Key']})
                    total_count += 1
        
        if total_count == 0:
            print("✅ 삭제할 이미지가 없습니다.")
            return
        
        print(f"\n⚠️  총 {total_count}개의 이미지를 삭제합니다.")
        print(f"정말 삭제하시겠습니까? (yes/no): ", end="")
        
        response = input().strip().lower()
        
        if response != 'yes':
            print("❌ 삭제가 취소되었습니다.")
            return
        
        # 배치 삭제 (최대 1000개씩)
        print("\n🗑️  삭제 중...")
        deleted_count = 0
        
        # 1000개씩 나눠서 삭제
        for i in range(0, len(objects_to_delete), 1000):
            batch = objects_to_delete[i:i+1000]
            
            response = s3_client.delete_objects(
                Bucket=bucket_name,
                Delete={'Objects': batch}
            )
            
            if 'Deleted' in response:
                deleted_count += len(response['Deleted'])
                print(f"  삭제됨: {deleted_count}/{total_count}")
            
            if 'Errors' in response:
                print(f"  ⚠️  에러: {len(response['Errors'])}개")
                for error in response['Errors'][:5]:  # 처음 5개만 표시
                    print(f"    - {error['Key']}: {error['Message']}")
        
        print(f"\n✅ 완료! 총 {deleted_count}개의 이미지가 삭제되었습니다.")
        
    except Exception as e:
        print(f"❌ 에러 발생: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    delete_all_r2_images()
