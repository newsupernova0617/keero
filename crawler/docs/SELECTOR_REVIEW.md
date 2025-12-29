# Crawler Selector 검토 결과

## 검토 완료 (2025-12-23)

### ✅ 수정 완료

1. **todayhumor** (오늘의유머)

   - **문제**: `td.subject a` selector가 개별 게시글 페이지에서 30개 요소를 매칭
   - **해결**: `div.viewSubjectDiv` (제목), `div.contentContainer` (본문)으로 변경
   - **상태**: ✅ 정상 작동 확인

2. **ruliweb** (루리웹)
   - **문제**: `a.subject_link` selector가 개별 게시글 페이지에서 32개 요소를 매칭
   - **해결**: `span.subject_text` (제목)로 변경
   - **상태**: ✅ 정상 작동 확인

### ⚠️ 검토 필요

3. **fmkorea** (에펨코리아)

   - **use_playwright**: True
   - **현재 selector**: `h3.title a` (목록/개별 모두)
   - **상태**: 일부 중복 제목 발견 (실제 중복 게시글일 가능성)
   - **TODO**: Playwright로 개별 게시글 페이지 구조 확인 필요

4. **mlbpark** (엠엘비파크)

   - **use_playwright**: True
   - **현재 selector**: `a.txt` (목록/개별 모두)
   - **상태**: 미테스트
   - **TODO**: Playwright로 개별 게시글 페이지 구조 확인 필요

5. **clien** (클리앙)

   - **use_playwright**: True (Cloudflare 우회)
   - **현재 selector**: `a.list_subject` (목록/개별 모두)
   - **상태**: 미테스트
   - **TODO**: Playwright로 개별 게시글 페이지 구조 확인 필요

6. **humoruniv** (웃긴대학)

   - **use_playwright**: True
   - **현재 selector**: `a[href*='read']` (목록/개별 모두)
   - **상태**: 미테스트
   - **TODO**: Playwright로 개별 게시글 페이지 구조 확인 필요

7. **dogdrip** (개드립)

   - **use_playwright**: True
   - **현재 selector**: `a` (목록/개별 모두)
   - **상태**: 미테스트
   - **TODO**: Playwright로 개별 게시글 페이지 구조 확인 필요

8. **ppomppu** (뽐뿌)
   - **use_playwright**: True (변경됨)
   - **enabled**: False (비활성화)
   - **상태**: requests로 접근 불가, Playwright 필요
   - **TODO**: Playwright로 목록/개별 페이지 구조 모두 확인 필요

## 일반적인 문제 패턴

**문제**: 목록 페이지의 selector를 개별 게시글 페이지에도 사용

- 목록 페이지: 게시글 링크를 찾기 위한 selector
- 개별 페이지: 해당 페이지에도 사이드바/관련글 등에 같은 selector가 존재
- 결과: 항상 첫 번째 요소(사이드바의 첫 게시글)만 선택됨

**해결**: 개별 게시글 페이지에서 유일한 제목 요소를 찾아야 함

- 예: `div.viewSubjectDiv`, `span.subject_text` 등

## 검증 방법

1. **test_selectors.py**: requests 사이트 자동 테스트
2. **check_duplicate_titles.py**: DB에서 중복 제목 확인
3. **수동 크롤링**: `python3 main.py --site [사이트명]`으로 실제 크롤링 테스트

## 권장 사항

Playwright 사이트들은 다음 순서로 검토:

1. 실제 크롤링 실행
2. DB에서 중복 제목 확인
3. 문제 발견 시 Playwright로 개별 페이지 HTML 구조 확인
4. 올바른 selector 찾아서 config.py 수정
