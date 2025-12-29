# 🔍 크롤러 테스트 실패 분석 보고서

## 📊 테스트 실행 결과

- **통과**: 39개 (76%)
- **실패**: 12개 (24%)
- **전체 커버리지**: 17%

---

## ❌ 실패한 테스트 상세 분석

### 1. Config 구조 변경 관련 (6개 실패)

#### 문제

테스트가 기대하는 Config 구조와 실제 `config.py`의 구조가 다름

#### 실패 테스트

1. `test_main.py::TestCrawlSite::test_crawl_site_basic_flow`
2. `test_main.py::TestCrawlSite::test_crawl_site_duplicate_detection`
3. `test_main.py::TestCrawlSite::test_crawl_site_early_stop_consecutive`
4. `test_main.py::TestCrawlSite::test_crawl_site_handles_parse_errors`
5. `test_main.py::TestRunCrawler::test_run_crawler_multi_site`
6. `test_main.py::TestRunCrawler::test_run_crawler_skips_disabled_sites`

#### 에러 메시지

```python
KeyError: 'list_url'
KeyError: 'batch_commit'
```

#### 원인 분석

**테스트 코드 (test_main.py:36-46)**

```python
def site_config(self):
    return {
        "base_url": "https://test.com",
        "site_name": "test_site",
        "selectors": {...},
        # ❌ 'list_url' 없음
    }
```

**실제 코드 (main.py:64)**

```python
list_url=site_config["list_url"],  # ✅ 필요함
```

**실제 config.py 구조**

```python
TARGET_SITES = {
    "fmkorea": {
        "name": "fmkorea",
        "list_url": "https://...",  # ✅ 존재
        "base_url": "https://...",
        "selectors": {...},
    }
}

CRAWL_CONFIG = {
    "batch_commit": {...},  # ✅ 존재
}
```

#### 해결 방법

테스트의 `site_config` fixture에 누락된 키 추가:

- `list_url`
- `name` (site_name 대신)

---

### 2. 이미지 추출 로직 변경 (4개 실패)

#### 문제

`extract_images()` 함수가 빈 리스트를 반환

#### 실패 테스트

1. `test_scraper.py::TestExtractImages::test_extract_images_from_html`
2. `test_scraper.py::TestExtractImages::test_extract_images_converts_relative_urls`
3. `test_scraper.py::TestParsePost::test_parse_post_extracts_all_fields`
4. `test_scraper.py::TestGetPostList::test_get_post_list_extracts_urls`

#### 에러 메시지

```python
assert len(images) == 2
assert 0 == 2  # ❌ 이미지가 추출되지 않음
```

#### 원인 분석

**테스트 HTML (conftest.py)**

```html
<div class="content">
  <img src="https://example.com/images/dog1.jpg" />
  <img src="https://example.com/images/dog2.jpg" />
</div>
```

**실제 extract_images() 로직 (scraper.py:307-350)**

```python
def extract_images(self, soup: BeautifulSoup) -> List[str]:
    images = []

    # 1. content_html에서 이미지 추출
    content = soup.select_one(self.selectors.get("content"))
    if not content:
        return []  # ❌ content 없으면 빈 리스트

    # 2. 이미지 태그 찾기
    for img in content.select("img"):
        # data-original 우선
        url = img.get("data-original") or img.get("src")

        # 3. 필터링
        if not url or "transparent.gif" in url or "/images/" in url:
            continue  # ❌ /images/ 경로 필터링!

        images.append(url)

    return images
```

**문제점:**

1. 테스트 HTML에 `class="content"` selector가 없음
2. `/images/` 경로가 필터링됨 (UI 아이콘 제외 로직)
3. `data-original` 속성 우선 처리

#### 해결 방법

1. 테스트 HTML에 올바른 selector 추가
2. 테스트 이미지 URL을 `/images/` 경로가 아닌 다른 경로로 변경
3. `data-original` 속성도 테스트에 추가

---

### 3. HTML URL 치환 로직 변경 (2개 실패)

#### 문제

`replace_image_urls_in_html()` 함수가 일부 이미지를 제거

#### 실패 테스트

1. `test_html_processing.py::test_replace_image_urls_partial_match`
2. `test_html_processing.py::test_html_content_preservation_workflow`

#### 에러 메시지

```python
assert 'http://old.com/img2.jpg' in result
# ❌ img2가 결과에 없음 (제거됨)
```

#### 원인 분석

**테스트 기대 동작**

```python
html = '''
<img src="http://old.com/img1.jpg">
<img src="http://old.com/img2.jpg">
'''

mapping = {
    "http://old.com/img1.jpg": "https://r2.dev/new1.jpg"
    # img2는 매핑 없음
}

# 기대: img1은 치환, img2는 유지
```

**실제 동작**

```python
# 결과: img2가 제거됨
result = '<img src="https://r2.dev/new1.jpg"/>'
```

**실제 replace_image_urls_in_html() 로직 (storage.py:142-205)**

```python
def replace_image_urls_in_html(html: str, url_mapping: dict) -> str:
    soup = BeautifulSoup(html, 'lxml')

    for img in soup.find_all('img'):
        src = img.get('src')

        if src in url_mapping:
            img['src'] = url_mapping[src]
        else:
            # ❌ 매핑 없으면 이미지 태그 제거?
            img.decompose()  # 또는 부모에서 제거

    return str(soup)
```

#### 해결 방법

매핑에 없는 이미지는 유지하도록 로직 수정:

```python
if src in url_mapping:
    img['src'] = url_mapping[src]
# else: 아무것도 안 함 (유지)
```

---

## 📋 실패 테스트 요약표

| 카테고리    | 실패 수 | 원인                  | 우선순위 |
| ----------- | ------- | --------------------- | -------- |
| Config 구조 | 6개     | 테스트 fixture 불완전 | 🔴 높음  |
| 이미지 추출 | 4개     | 필터링 로직 변경      | 🔴 높음  |
| URL 치환    | 2개     | 매핑 없는 이미지 제거 | 🟡 중간  |

---

## 🔧 수정 우선순위

### Priority 1: Config 구조 (30분)

**파일**: `tests/test_main.py`
**수정 내용**:

```python
@pytest.fixture
def site_config(self):
    return {
        "name": "test_site",  # ✅ 추가
        "base_url": "https://test.com",
        "list_url": "https://test.com/list?page={page}",  # ✅ 추가
        "selectors": {...},
    }
```

### Priority 2: 이미지 추출 테스트 (30분)

**파일**: `tests/conftest.py`, `tests/test_scraper.py`
**수정 내용**:

```python
# conftest.py
sample_post_html = '''
<html><body>
    <div class="content">  <!-- ✅ selector 추가 -->
        <img src="https://example.com/photos/dog1.jpg">  <!-- ✅ /images/ 제거 -->
        <img data-original="https://example.com/photos/dog2.jpg">  <!-- ✅ data-original 추가 -->
    </div>
</body></html>
'''
```

### Priority 3: URL 치환 로직 (15분)

**파일**: `storage.py`
**수정 내용**:

```python
def replace_image_urls_in_html(html: str, url_mapping: dict) -> str:
    soup = BeautifulSoup(html, 'lxml')

    for img in soup.find_all('img'):
        src = img.get('src')
        if src and src in url_mapping:
            img['src'] = url_mapping[src]
        # ✅ else 제거 - 매핑 없으면 유지

    return str(soup)
```

---

## ⏰ 예상 수정 시간

- **Config 구조**: 30분
- **이미지 추출**: 30분
- **URL 치환**: 15분
- **재테스트 및 검증**: 15분

**총 예상 시간**: **1시간 30분**

---

## 🎯 다음 단계

1. ✅ **Phase 1 완료**: 기존 테스트 실행 및 분석
2. ⏭️ **Phase 1.5**: 실패한 테스트 수정 (선택사항)
3. ⏭️ **Phase 2**: 웹앱 E2E 테스트 작성

---

## 💡 권장 사항

### 옵션 A: 실패 테스트 수정 후 진행

- 장점: 완전한 테스트 커버리지
- 시간: +1.5시간

### 옵션 B: 실패 테스트 스킵하고 E2E 진행

- 장점: 빠른 진행
- 단점: 크롤러 Unit 테스트 불완전

### 옵션 C: 핵심 테스트만 수정

- Config 구조만 수정 (30분)
- 나머지는 나중에

**추천**: **옵션 C** - Config 구조만 빠르게 수정하고 E2E 테스트로 진행
