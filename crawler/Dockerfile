FROM python:3.11-slim

WORKDIR /app

# 시스템 의존성 설치 (Playwright + FFmpeg)
RUN apt-get update && apt-get install -y \
    gcc \
    ffmpeg \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libxshmfence1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Python 의존성 설치 및 Playwright 브라우저 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    playwright install chromium

# 애플리케이션 코드 복사
COPY . .

# 데이터 디렉토리 생성
RUN mkdir -p /data

# 스케줄러 실행 (계속 실행되면서 주기적으로 크롤링)
CMD ["python", "scheduler.py"]
