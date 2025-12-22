# requirements.txt

## 필수 패키지

```txt
# 웹 크롤링
requests==2.31.0
beautifulsoup4==4.12.2
lxml==4.9.3

# 클라우드 스토리지
boto3==1.34.0

# 데이터베이스
SQLAlchemy==2.0.23

# 환경 변수
python-dotenv==1.0.0

# 날짜 파싱
python-dateutil==2.8.2

# 스케줄링
APScheduler==3.10.4

# 이미지 처리 및 최적화
Pillow==10.1.0
imagehash==4.3.1

# 테스트 및 개발 도구
pytest==7.4.3
pytest-cov==4.1.0
responses==0.24.1
ruff==0.1.8
```

## 패키지 용도

| 패키지          | 용도                    |
| --------------- | ----------------------- |
| requests        | HTTP 요청               |
| beautifulsoup4  | HTML 파싱               |
| lxml            | 파서 백엔드             |
| boto3           | R2 업로드               |
| SQLAlchemy      | ORM, DB 관리            |
| python-dotenv   | 환경 변수 로드          |
| python-dateutil | 유연한 날짜 파싱        |
| APScheduler     | 크롤링 스케줄링         |
| Pillow          | 이미지 처리             |
| imagehash       | 이미지 유사도 해시 생성 |
| pytest          | 테스트 프레임워크       |
| pytest-cov      | 코드 커버리지 측정      |
| responses       | HTTP 요청 모킹          |
| ruff            | 코드 품질 검사/포매팅   |

## 설치 방법

```bash
# 가상 환경 생성
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 패키지 설치
pip install -r requirements.txt
```
