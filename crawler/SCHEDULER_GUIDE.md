# 커뮤니티 크롤러 - Windows 작업 스케줄러 설정 가이드

## 📋 개요

15분 간격으로 8개 사이트를 순차적으로 크롤링합니다.
- 각 사이트는 2시간마다 크롤링됨
- 사용자는 15분마다 새 글을 볼 수 있음

## 🕐 스케줄 타임라인

| 시간 | 사이트 | 비고 |
|------|--------|------|
| :00 | Ruliweb | requests (빠름) |
| :15 | TodayHumor | requests (빠름) |
| :30 | Ppomppu | requests (빠름) |
| :45 | FMKorea | Playwright (느림) |
| :00 | MLBPark | Playwright (느림) |
| :15 | Clien | Playwright (느림) |
| :30 | Humoruniv | Playwright (느림) |
| :45 | Dogdrip | Playwright (느림) |
| :00 | Ruliweb | (반복) |

## 🔧 Windows 작업 스케줄러 설정 방법

### 1단계: 작업 스케줄러 열기
```
시작 → "작업 스케줄러" 검색 → 실행
```

### 2단계: 기본 작업 만들기 (8번 반복)

#### 작업 1: Ruliweb
1. **이름**: `Crawler - Ruliweb`
2. **트리거**: 
   - 매일
   - 시작: 00:00
   - 반복 간격: 2시간
   - 기간: 1일
3. **동작**: 
   - 프로그램 시작
   - 프로그램: `C:\Users\yj437\OneDrive\Desktop\coding_windows\aagag_clone\crawler\run_crawler.bat`
   - 인수: `ruliweb`
   - 시작 위치: `C:\Users\yj437\OneDrive\Desktop\coding_windows\aagag_clone\crawler`

#### 작업 2: TodayHumor
1. **이름**: `Crawler - TodayHumor`
2. **트리거**: 
   - 매일
   - 시작: 00:15
   - 반복 간격: 2시간
   - 기간: 1일
3. **동작**: 
   - 프로그램: `run_crawler.bat`
   - 인수: `todayhumor`

#### 작업 3: Ppomppu
1. **이름**: `Crawler - Ppomppu`
2. **트리거**: 
   - 매일
   - 시작: 00:30
   - 반복 간격: 2시간
   - 기간: 1일
3. **동작**: 
   - 프로그램: `run_crawler.bat`
   - 인수: `ppomppu`

#### 작업 4: FMKorea
1. **이름**: `Crawler - FMKorea`
2. **트리거**: 
   - 매일
   - 시작: 00:45
   - 반복 간격: 2시간
   - 기간: 1일
3. **동작**: 
   - 프로그램: `run_crawler.bat`
   - 인수: `fmkorea`

#### 작업 5: MLBPark
1. **이름**: `Crawler - MLBPark`
2. **트리거**: 
   - 매일
   - 시작: 01:00
   - 반복 간격: 2시간
   - 기간: 1일
3. **동작**: 
   - 프로그램: `run_crawler.bat`
   - 인수: `mlbpark`

#### 작업 6: Clien
1. **이름**: `Crawler - Clien`
2. **트리거**: 
   - 매일
   - 시작: 01:15
   - 반복 간격: 2시간
   - 기간: 1일
3. **동작**: 
   - 프로그램: `run_crawler.bat`
   - 인수: `clien`

#### 작업 7: Humoruniv
1. **이름**: `Crawler - Humoruniv`
2. **트리거**: 
   - 매일
   - 시작: 01:30
   - 반복 간격: 2시간
   - 기간: 1일
3. **동작**: 
   - 프로그램: `run_crawler.bat`
   - 인수: `humoruniv`

#### 작업 8: Dogdrip
1. **이름**: `Crawler - Dogdrip`
2. **트리거**: 
   - 매일
   - 시작: 01:45
   - 반복 간격: 2시간
   - 기간: 1일
3. **동작**: 
   - 프로그램: `run_crawler.bat`
   - 인수: `dogdrip`

## 🧪 테스트 방법

### 수동 테스트
```bash
cd crawler
python main.py --site ruliweb
```

### 배치 파일 테스트
```bash
cd crawler
run_crawler.bat ruliweb
```

### 로그 확인
```bash
cd crawler/logs
type crawler_ruliweb_20241222.log
```

## 📊 모니터링

### 로그 파일 위치
```
crawler/logs/crawler_[사이트명]_[날짜].log
```

### 로그 내용
- 시작/종료 시간
- 크롤링된 게시글 수
- 에러 메시지

## ⚙️ 고급 설정

### 조건 추가 (선택사항)
- **전원**: AC 전원 연결 시에만 실행
- **유휴**: 컴퓨터가 유휴 상태일 때만
- **네트워크**: 네트워크 연결 시에만

### 우선순위
- 일반 (기본값)
- 낮음 (백그라운드 실행)

## 🔍 문제 해결

### 작업이 실행되지 않음
1. 작업 스케줄러에서 "마지막 실행 결과" 확인
2. 로그 파일 확인
3. 수동으로 배치 파일 실행해보기

### Python 경로 오류
`run_crawler.bat`에서 Python 경로 수정:
```batch
set PYTHON=C:\Python311\python.exe
```

### 권한 오류
작업 스케줄러에서:
- "가장 높은 권한으로 실행" 체크
- "사용자가 로그온했는지 여부에 관계없이 실행" 선택

## 📝 참고사항

- 각 사이트는 2시간마다 크롤링됨
- 배치 커밋으로 DB 잠금 최소화
- Early Stop으로 중복 시 빠른 종료
- Playwright 사이트는 3~5분 소요
- requests 사이트는 1~2분 소요
