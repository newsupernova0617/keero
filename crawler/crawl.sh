#!/bin/bash
# 크롤러 실행 스크립트 (Cron용)

# 프로젝트 디렉토리로 이동
cd /home/yj437/coding/aagag_clone/crawler

# 가상환경 파이썬으로 실행
./venv/bin/python run.py >> cron.log 2>&1
