#!/bin/bash

# 가상환경 활성화 및 스케줄러 실행
cd "$(dirname "$0")"
source venv/bin/activate
python3 scheduler.py
