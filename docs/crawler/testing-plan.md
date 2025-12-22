# 테스트 및 코드 품질 개선 계획

## 현재 상태

### 테스트 커버리지

| 파일            | 현재 | 목표 | 이슈                  |
| --------------- | ---- | ---- | --------------------- |
| `config.py`     | 100% | 100% | ✅ 완료               |
| `logging_db.py` | 97%  | 97%  | ✅ 완료               |
| `storage.py`    | 62%  | 80%  | R2/이미지 처리 미커버 |
| `scraper.py`    | 26%  | 80%  | HTTP 요청 로직 미커버 |
| `main.py`       | 12%  | 70%  | 통합 테스트 부족      |

### Ruff 린트 이슈

- `conftest.py`: E402 (2개) - sys.path 수정 필요로 의도적 설계
- `test_main.py`: F401, F841 (2개) - 미사용 import/변수

## 개선 계획

### Phase 1: 테스트 인프라 개선

1. **conftest.py 리팩토링**

   - noqa 주석 추가로 E402 경고 무시
   - 공통 fixture 추가 (mock HTTP 응답)

2. **test_main.py 수정**
   - 미사용 import 제거
   - HTML mock 구조 개선

### Phase 2: scraper.py 테스트 활성화

1. 주석 처리된 테스트 활성화
2. 실제 로직 테스트 추가:
   - `fetch_page()` 성공/실패 시나리오
   - `parse_post()` 데이터 추출 검증
   - `extract_images()` URL 변환 검증
   - 예외 체이닝 검증

### Phase 3: storage.py 테스트 확장

1. `save_post()` 완전 테스트
2. `download_image()` mock 테스트
3. `upload_to_r2()` mock 테스트

### Phase 4: main.py 통합 테스트 수정

1. HTML 구조 문제 해결
2. crawl_site() 테스트 개선
3. run_crawler() 테스트 개선

## 우선순위

1. 🔴 **높음**: Ruff 이슈 정리 (즉시)
2. 🟡 **중간**: scraper.py 테스트 활성화
3. 🟢 **낮음**: 통합 테스트 개선

## 예상 결과

### 테스트 커버리지 목표

- `scraper.py`: 26% → 80%
- `storage.py`: 62% → 75%
- `main.py`: 12% → 50%
- **전체**: 53% → 70%

### Ruff 이슈

- 현재: 4개
- 목표: 0개 (noqa 포함)
