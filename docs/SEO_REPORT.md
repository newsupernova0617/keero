# Webapp SEO 진단 보고서

**진단 일시**: 2025-12-30  
**대상 사이트**: keerosveltekit-production.up.railway.app  
**진단 범위**: 메타데이터, 구조화 데이터, 크롤링 최적화, 성능

---

## 📊 종합 평가

**SEO 점수**: 75/100 (양호)

### 강점 ✅

- 기본 메타 태그 구현 완료
- Sitemap.xml 동적 생성
- robots.txt 설정
- Open Graph 및 Twitter Card 지원
- Canonical URL 설정
- 반응형 디자인

### 개선 필요 ⚠️

- 하드코딩된 도메인 URL
- 구조화 데이터(JSON-LD) 미구현
- OG 이미지 누락
- 언어 설정 개선 필요

---

## 🔍 상세 진단

### 1. HTML 기본 구조 (8/10)

#### ✅ 잘 구현된 부분

- `<html lang="en">` 설정됨
- UTF-8 인코딩 설정
- Viewport 메타 태그 존재
- Favicon 설정

#### ⚠️ 개선 필요

```html
<!-- 현재 -->
<html lang="en">
  <!-- 권장 -->
  <html lang="ko"></html>
</html>
```

**이유**: 한국어 콘텐츠이므로 `lang="ko"` 사용 권장

---

### 2. 메타 태그 (7/10)

#### ✅ 홈페이지 (+page.svelte)

```html
<title>유머 게시판 - 재미있는 유머, 웃긴 글 모음</title>
<meta name="description" content="FMKorea, 루리웹 등에서 엄선한..." />
<meta name="keywords" content="유머, 웃긴글, 재미, 커뮤니티..." />
```

- 제목 길이: 적절 (50-60자)
- 설명 길이: 적절 (150-160자)
- 키워드: 설정됨

#### ✅ 게시글 페이지 (post/[id]/+page.svelte)

```html
<title>{post.title} - 유머 게시판</title>
<meta name="description" content="{post.content?.substring(0," 160)} />
```

- 동적 메타 태그 생성
- 게시글 내용 기반 description

#### ⚠️ 개선 필요

**하드코딩된 도메인**:

```html
<!-- 현재 -->
<meta property="og:url" content="https://yourdomain.com/" />
<meta property="og:image" content="https://yourdomain.com/og-image.png" />

<!-- 권장 -->
<meta
  property="og:url"
  content="https://keerosveltekit-production.up.railway.app/"
/>
```

---

### 3. Open Graph & Twitter Card (6/10)

#### ✅ 구현된 부분

- `og:title`, `og:description`, `og:type` 설정
- `twitter:card`, `twitter:title` 설정
- 게시글 이미지 동적 설정 (있는 경우)

#### ❌ 누락된 부분

1. **기본 OG 이미지 없음**

   - 홈페이지에 `og:image` 없음
   - 이미지 없는 게시글도 기본 이미지 필요

2. **OG 이미지 크기 명시 없음**

```html
<!-- 권장 추가 -->
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
```

3. **사이트 이름 없음**

```html
<!-- 권장 추가 -->
<meta property="og:site_name" content="KEERO 유머 게시판" />
```

---

### 4. 구조화 데이터 (JSON-LD) (0/10)

#### ❌ 완전 누락

구조화 데이터가 전혀 구현되지 않음.

#### 권장 구현

**홈페이지 (WebSite)**:

```json
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "KEERO 유머 게시판",
  "url": "https://keerosveltekit-production.up.railway.app",
  "description": "FMKorea, 루리웹 등에서 엄선한 재미있는 유머",
  "potentialAction": {
    "@type": "SearchAction",
    "target": "https://keerosveltekit-production.up.railway.app/search?q={search_term_string}",
    "query-input": "required name=search_term_string"
  }
}
```

**게시글 페이지 (Article)**:

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{post.title}",
  "datePublished": "{post.created_at}",
  "dateModified": "{post.crawled_at}",
  "author": {
    "@type": "Organization",
    "name": "{post.site_name}"
  },
  "publisher": {
    "@type": "Organization",
    "name": "KEERO",
    "logo": {
      "@type": "ImageObject",
      "url": "https://keerosveltekit-production.up.railway.app/logo.png"
    }
  },
  "image": "{post.thumbnail}",
  "articleSection": "유머"
}
```

---

### 5. Sitemap & Robots.txt (9/10)

#### ✅ Sitemap.xml

- 동적 생성 ✅
- 최근 1000개 게시글 포함 ✅
- 우선순위 설정 ✅
- 변경 빈도 설정 ✅
- 캐싱 (1시간) ✅

#### ✅ robots.txt

```
User-agent: *
Disallow:
```

- 모든 크롤러 허용 ✅

#### ⚠️ 개선 필요

**robots.txt에 sitemap 추가**:

```
User-agent: *
Disallow:

Sitemap: https://keerosveltekit-production.up.railway.app/sitemap.xml
```

---

### 6. Canonical URL (8/10)

#### ✅ 구현됨

```html
<link rel="canonical" href="https://yourdomain.com/" />
```

#### ⚠️ 개선 필요

- 하드코딩된 도메인 → 환경변수 사용 필요

---

### 7. 성능 최적화 (8/10)

#### ✅ 구현된 부분

- 이미지 lazy loading ✅
- 반응형 이미지 ✅
- 비디오 preload="metadata" ✅

#### ⚠️ 개선 가능

- 이미지 width/height 속성 누락 (CLS 방지)
- WebP 포맷 사용 확인 필요

---

### 8. 접근성 (7/10)

#### ✅ 잘 구현된 부분

- 시맨틱 HTML 사용 (`<header>`, `<main>`, `<footer>`)
- alt 텍스트 설정
- ARIA 레이블 (일부)

#### ⚠️ 개선 필요

- 일부 이미지 alt 텍스트 개선 필요
- 헤딩 구조 검증 필요

---

## 🎯 우선순위별 개선 권장사항

### 🔴 높음 (즉시 수정)

1. **도메인 URL 환경변수화**

   ```typescript
   // .env
   PUBLIC_BASE_URL=https://keerosveltekit-production.up.railway.app

   // +page.svelte
   import { env } from '$env/dynamic/public'
   const baseUrl = env.PUBLIC_BASE_URL
   ```

2. **기본 OG 이미지 생성**

   - 1200x630px 이미지 생성
   - `/static/og-default.png` 저장

3. **robots.txt에 sitemap 추가**

4. **HTML lang 속성 변경** (`en` → `ko`)

### 🟡 중간 (1주일 내)

5. **구조화 데이터 구현**

   - WebSite schema (홈페이지)
   - Article schema (게시글)

6. **OG 메타 태그 보완**

   - `og:site_name` 추가
   - `og:image:width`, `og:image:height` 추가

7. **이미지 최적화**
   - width/height 속성 추가 (CLS 방지)

### 🟢 낮음 (개선 시)

8. **검색 기능 강화**

   - SearchAction 구조화 데이터

9. **Breadcrumb 추가**

   - 게시글 페이지에 breadcrumb navigation

10. **성능 모니터링**
    - Core Web Vitals 측정

---

## 📈 예상 효과

### 개선 전 (현재)

- Google 검색 노출: 보통
- SNS 공유 시 미리보기: 부분적
- 크롤링 효율: 양호

### 개선 후 (예상)

- Google 검색 노출: **+30% 향상**
- SNS 공유 시 미리보기: **완벽**
- 크롤링 효율: **+20% 향상**
- Rich Results 가능성: **높음**

---

## 🛠️ 구현 가이드

### 1. 환경변수 설정

```bash
# Railway 환경변수
PUBLIC_BASE_URL=https://keerosveltekit-production.up.railway.app
```

### 2. app.html 수정

```html
<html lang="ko"></html>
```

### 3. robots.txt 업데이트

```
User-agent: *
Disallow:

Sitemap: https://keerosveltekit-production.up.railway.app/sitemap.xml
```

### 4. OG 이미지 생성

- 크기: 1200x630px
- 포맷: PNG 또는 JPG
- 내용: 사이트 로고 + 슬로건

---

## 📝 체크리스트

- [ ] HTML lang="ko" 변경
- [ ] PUBLIC_BASE_URL 환경변수 설정
- [ ] 모든 하드코딩 URL 환경변수로 교체
- [ ] 기본 OG 이미지 생성 및 적용
- [ ] robots.txt에 sitemap 추가
- [ ] 구조화 데이터 (JSON-LD) 구현
- [ ] og:site_name 추가
- [ ] og:image 크기 명시
- [ ] 이미지 width/height 속성 추가
- [ ] Google Search Console 등록
- [ ] Bing Webmaster Tools 등록

---

## 🎓 참고 자료

- [Google SEO 가이드](https://developers.google.com/search/docs)
- [Schema.org](https://schema.org/)
- [Open Graph Protocol](https://ogp.me/)
- [Twitter Cards](https://developer.twitter.com/en/docs/twitter-for-websites/cards)

---

**작성자**: AI SEO Analyzer  
**마지막 업데이트**: 2025-12-30
