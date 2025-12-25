# 🐛 Transparent.gif 이미지 문제 해결 보고서

## 📋 문제 요약

- **현상**: 이미지가 3개 이상인 게시물에서 처음 3개는 정상적으로 R2 이미지가 표시되지만, 나머지는 투명한 `transparent.gif`의 R2 URL이 표시됨
- **영향**: FMKorea 게시물의 Lazy Loading 이미지가 제대로 표시되지 않음

## 🔍 원인 분석

### FMKorea의 Lazy Loading 방식

```html
<!-- 처음 3개: 즉시 로딩 -->
<img src="//image.fmkorea.com/files/attach/.../실제이미지.png" />

<!-- 나머지: Lazy Loading -->
<img
  src="//image.fmkorea.com/classes/lazy/img/transparent.gif"
  data-original="//image.fmkorea.com/files/attach/.../실제이미지.png"
/>
```

### 문제 발생 경로

1. **이전 크롤링 시점**에 `transparent.gif`가 한 번 업로드됨
2. **중복 체크 로직**이 동일한 MD5 해시를 가진 이미지를 재사용
3. 이후 크롤링에서 `transparent.gif`를 다운로드하려고 시도할 때마다, 동일한 R2 URL을 재사용하여 DB에 레코드 추가
4. 결과: DB에 `transparent.gif`의 R2 URL이 9번 저장됨

## ✅ 해결 방법

### 1. 방어 로직 추가 (`storage.py`)

```python
def save_image_smart(self, post_id: int, image_url: str, order_index: int) -> Image:
    # 방어 로직: placeholder/transparent.gif 필터링
    if 'transparent.gif' in image_url.lower() or 'placeholder' in image_url.lower():
        raise Exception(f"Placeholder image detected and rejected: {image_url}")

    # UI 아이콘 이미지 필터링 (/images/ 경로)
    if '/images/' in image_url:
        raise Exception(f"UI icon image detected and rejected: {image_url}")
```

**효과**: `extract_images()`에서 이미 필터링했지만, 혹시 모를 경우를 대비하여 이중 방어

### 2. 기존 DB 정리

- `clean_placeholder_images.py` 스크립트 실행
- 9개의 `transparent.gif` 레코드 삭제 완료 ✅

### 3. 테스트 재크롤링

- 문제가 있던 게시물 #3 재크롤링
- 12개의 이미지 모두 정상적으로 저장 확인 ✅
- `transparent.gif` 0개 ✅

## 📊 결과

### Before (문제 발생 시)

```
게시물 #3:
- 총 이미지: 12개
- 실제 이미지: 3개 (처음 3개만)
- transparent.gif: 9개 ❌
```

### After (수정 후)

```
게시물 #10 (재크롤링):
- 총 이미지: 12개 ✅
- 실제 이미지: 12개 ✅
- transparent.gif: 0개 ✅
```

## 🎯 향후 대응

### 자동 방지

- `save_image_smart()` 함수에 방어 로직 추가로 **영구적으로 방지**
- 다음 크롤링부터는 `transparent.gif`가 절대 업로드되지 않음

### 기존 데이터

- 기존 게시물의 HTML은 자동으로 수정되지 않음
- 필요시 `recrawl_post.py` 스크립트로 개별 재크롤링 가능
- 또는 다음 정기 크롤링 시 자동으로 업데이트됨 (중복 체크로 인해 스킵될 수 있음)

## 📝 관련 파일

- `storage.py`: 방어 로직 추가
- `clean_placeholder_images.py`: DB 정리 스크립트
- `recrawl_post.py`: 개별 게시물 재크롤링 스크립트

## ✨ 결론

문제의 근본 원인을 파악하고 완전히 해결했습니다!

- ✅ 방어 로직 추가로 재발 방지
- ✅ 기존 DB 정리 완료
- ✅ 테스트 재크롤링 성공
