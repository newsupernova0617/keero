#!/usr/bin/env python3
"""
Import 경로 자동 수정 스크립트
"""
import re
from pathlib import Path

def fix_imports_in_file(filepath: Path):
    """파일의 import 경로 수정"""
    try:
        content = filepath.read_text(encoding='utf-8')
        original = content
        
        # import 교체 규칙
        replacements = [
            (r'^from config import', 'from core.config import'),
            (r'^from scraper import', 'from core.scraper import'),
            (r'^from storage import', 'from core.storage import'),
            (r'^from api_client import', 'from core.api_client import'),
            (r'^from api_storage import', 'from core.api_storage import'),
            (r'^from logging_db import', 'from core.logging_db import'),
            (r'^from main import', 'from core.main import'),
            (r'^import config$', 'import core.config as config'),
            (r'^import scraper$', 'import core.scraper as scraper'),
            (r'^import storage$', 'import core.storage as storage'),
        ]
        
        for pattern, replacement in replacements:
            content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
        
        # 변경사항이 있으면 저장
        if content != original:
            filepath.write_text(content, encoding='utf-8')
            print(f"✅ Fixed: {filepath}")
            return True
        return False
    except Exception as e:
        print(f"❌ Error in {filepath}: {e}")
        return False

def main():
    base_path = Path('/home/yj437/coding/aagag_clone/crawler')
    
    # 수정 대상 파일들
    files_to_fix = []
    
    # core 폴더
    files_to_fix.extend(base_path.glob('core/*.py'))
    
    # utils 폴더
    files_to_fix.extend(base_path.glob('utils/*.py'))
    
    # tests 폴더
    files_to_fix.extend(base_path.glob('tests/*.py'))
    files_to_fix.extend(base_path.glob('tests/**/*.py'))
    
    # __init__.py 제외
    files_to_fix = [f for f in files_to_fix if f.name != '__init__.py']
    
    print(f"📝 Found {len(files_to_fix)} files to check")
    print("=" * 60)
    
    fixed_count = 0
    for filepath in sorted(files_to_fix):
        if fix_imports_in_file(filepath):
            fixed_count += 1
    
    print("=" * 60)
    print(f"✅ Fixed {fixed_count} files")

if __name__ == "__main__":
    main()
