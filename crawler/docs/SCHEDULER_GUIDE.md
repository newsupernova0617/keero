# 커뮤니티 크롤러 - 스케줄러 설정 가이드

## 📋 개요

**최적화된 2그룹 병렬 크롤링**

- **그룹 1** (00분): 루리웹, 오유, 뽐뿌 (3개 동시)
- **그룹 2** (05분): 펨코, 웃대, 개드립 (3개 동시)
- **업데이트 주기**: 10분마다 전체 사이트 업데이트
- **동시 실행**: 최대 3개 사이트 병렬 처리

## 🕐 스케줄 타임라인

```
00:00 - 그룹 1 시작 (루리웹 + 오유 + 뽐뿌)
00:05 - 그룹 2 시작 (펨코 + 웃대 + 개드립)
00:10 - 그룹 1 재실행
00:15 - 그룹 2 재실행
00:20 - 그룹 1 재실행
...
```

**사용자 경험:**

- 5분마다 새 글 업데이트 (어떤 그룹이든)
- 10분마다 전체 사이트 업데이트

## 🚀 Railway 배포 (자동 스케줄링)

### 실행 방법

```bash
python scheduler.py
```

### 특징

- ✅ **BackgroundScheduler**: 백그라운드에서 자동 실행
- ✅ **ThreadPoolExecutor**: 3개 사이트 동시 병렬 처리
- ✅ **독립 실행**: 각 사이트 크롤링이 서로 영향 없음
- ✅ **자동 복구**: 실패 시 다음 주기에 재시도

### 로그 확인

```bash
# Railway 로그
railway logs

# 또는 로컬 로그
tail -f ../data/logs.db
```

## 📊 사이트별 크롤링 정보

| 사이트 | 그룹 | 방식       | 평균 시간 | 페이지 |
| ------ | ---- | ---------- | --------- | ------ |
| 루리웹 | 1    | requests   | ~30초     | 1      |
| 오유   | 1    | Playwright | ~1분      | 1      |
| 뽐뿌   | 1    | Playwright | ~30초     | 1      |
| 펨코   | 2    | Playwright | ~1분      | 1      |
| 웃대   | 2    | Playwright | ~1분      | 1      |
| 개드립 | 2    | requests   | ~30초     | 1      |

**예상 총 시간:**

- 그룹 1: ~1분 (병렬 실행, 가장 느린 것 기준)
- 그룹 2: ~1분 (병렬 실행, 가장 느린 것 기준)

## ⚙️ 설정 변경

### 크롤링 주기 변경

`scheduler.py` 수정:

```python
# 10분 → 15분으로 변경
trigger = IntervalTrigger(
    minutes=15,  # 여기 수정
    start_date=now,
    timezone='Asia/Seoul'
)
```

### 그룹 간격 변경

```python
# 5분 → 7분으로 변경
start_time_group2 = now + timedelta(minutes=7)  # 여기 수정
```

### 동시 실행 수 변경

```python
# 3개 → 6개로 변경 (모든 사이트 동시 실행)
executors = {
    'default': ThreadPoolExecutor(max_workers=6)  # 여기 수정
}
```

## 🧪 테스트 방법

### 로컬 테스트

```bash
# 단일 사이트 테스트
python main.py --site ruliweb --limit 3

# 스케줄러 테스트 (실제 실행)
python scheduler.py
```

### 로그 확인

```bash
# SQLite 로그 확인
sqlite3 ../data/logs.db "SELECT * FROM logs ORDER BY timestamp DESC LIMIT 10;"
```

## 🔍 모니터링

### 크롤링 상태 확인

```bash
# 최근 크롤링 통계
sqlite3 ../data/posts.db "SELECT site_name, COUNT(*) as posts FROM posts GROUP BY site_name;"

# 최근 크롤링 시간
sqlite3 ../data/posts.db "SELECT site_name, MAX(crawled_at) as last_crawl FROM posts GROUP BY site_name;"
```

### 에러 확인

```bash
# 최근 에러 로그
sqlite3 ../data/logs.db "SELECT * FROM logs WHERE level = 'ERROR' ORDER BY timestamp DESC LIMIT 10;"
```

## 🔧 문제 해결

### 스케줄러가 멈춤

```bash
# 프로세스 확인
ps aux | grep scheduler.py

# 재시작
pkill -f scheduler.py
python scheduler.py
```

### 특정 사이트만 실패

```bash
# 해당 사이트만 수동 실행
python main.py --site fmkorea --limit 3

# 로그 확인
sqlite3 ../data/logs.db "SELECT * FROM logs WHERE message LIKE '%fmkorea%' ORDER BY timestamp DESC LIMIT 10;"
```

### DB 잠금 오류

```bash
# WAL 모드 확인
sqlite3 ../data/posts.db "PRAGMA journal_mode;"

# WAL 모드로 변경 (자동으로 설정됨)
sqlite3 ../data/posts.db "PRAGMA journal_mode=WAL;"
```

## 📝 참고사항

### Early Stop 설정

- 연속 중복 3개 → 즉시 중단
- 페이지 100% 중복 → 다음 페이지 안 감

### Batch Commit 설정

- 20개 게시글마다 커밋
- 또는 5초마다 커밋

### 최적화 팁

1. **동영상 많은 사이트**: 그룹 분리 권장
2. **느린 사이트**: Playwright 대신 requests 사용 검토
3. **서버 부하**: 동시 실행 수 조절 (max_workers)

## 🎯 성능 지표

**기존 스케줄링 (순차 실행):**

- 업데이트 주기: 32분
- 총 소요 시간: ~24분

**새 스케줄링 (2그룹 병렬):**

- 업데이트 주기: 10분 ✅ (3.2배 빠름)
- 총 소요 시간: ~2분 ✅ (12배 빠름)
