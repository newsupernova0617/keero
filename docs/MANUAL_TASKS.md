# 🛠️ 수동 작업 필요 항목

## ✅ 자동 구현 완료 (방금 완료됨)

1. ✅ HTML lang="ko" 변경
2. ✅ robots.txt에 sitemap 추가
3. ✅ SEO 유틸리티 함수 생성
4. ✅ 모든 하드코딩 URL → 환경변수 사용
5. ✅ og:site_name 추가
6. ✅ og:image 크기 명시 (1200x630)
7. ✅ 기본 OG 이미지 fallback 로직
8. ✅ JSON-LD 구조화 데이터 구현 (WebSite + Article)

---

## 🔴 수동 작업 필요 (사용자가 직접 해야 함)

### 1. Railway 환경변수 설정 ⭐ 최우선

**Railway 대시보드 → webapp 서비스 → Variables**에서 추가:

```bash
PUBLIC_BASE_URL=https://keerosveltekit-production.up.railway.app
```

**중요**: 이 환경변수를 설정하지 않으면 fallback URL이 사용되지만, 명시적으로 설정하는 것이 좋습니다.

---

### 2. 기본 OG 이미지 생성 및 업로드 ⭐ 중요

#### 이미지 사양

- **파일명**: `og-default.png`
- **크기**: 1200 x 630 픽셀
- **위치**: `/home/yj437/coding/aagag_clone/webapp/static/og-default.png`
- **포맷**: PNG 또는 JPG

#### 이미지 내용 권장사항

```
┌─────────────────────────────────────┐
│                                     │
│         KEERO 유머 게시판            │
│                                     │
│   FMKorea, 루리웹, 오늘의유머 등    │
│   재미있는 유머를 한곳에서!         │
│                                     │
└─────────────────────────────────────┘
```

#### 생성 방법 옵션

1. **Canva** (무료): https://www.canva.com/

   - 템플릿: "Facebook Post" 또는 "Open Graph"
   - 크기: 1200 x 630px로 설정

2. **Figma** (무료): https://www.figma.com/

   - Frame 생성: 1200 x 630px

3. **Photoshop/GIMP** (전문가용)

#### 업로드 후

```bash
cd /home/yj437/coding/aagag_clone
git add webapp/static/og-default.png
git commit -m "Add default OG image"
git push origin before_deploy
```

---

### 3. 로고 이미지 생성 (선택사항)

JSON-LD Article schema에서 publisher logo를 참조하고 있습니다:

- **파일명**: `logo.png`
- **크기**: 정사각형 권장 (예: 512 x 512px)
- **위치**: `/home/yj437/coding/aagag_clone/webapp/static/logo.png`

---

### 4. Google Search Console 등록 ⭐ 중요

1. https://search.google.com/search-console 접속
2. "속성 추가" 클릭
3. URL: `https://keerosveltekit-production.up.railway.app` 입력
4. 소유권 확인 방법 선택:

   - **권장**: HTML 태그 방법
   - 제공된 메타 태그를 `app.html`의 `<head>`에 추가

5. Sitemap 제출:
   - 좌측 메뉴 → Sitemaps
   - URL 입력: `https://keerosveltekit-production.up.railway.app/sitemap.xml`

---

### 5. Bing Webmaster Tools 등록 (선택사항)

1. https://www.bing.com/webmasters 접속
2. 사이트 추가
3. Sitemap 제출

---

### 6. 성능 모니터링 도구 설정 (선택사항)

#### Google Analytics 4

1. https://analytics.google.com 접속
2. 속성 생성
3. 측정 ID를 `app.html`에 추가

#### Google PageSpeed Insights

- https://pagespeed.web.dev/
- URL 입력하여 성능 측정

---

## 📋 체크리스트

### 필수 (즉시)

- [ ] Railway 환경변수 `PUBLIC_BASE_URL` 설정
- [ ] OG 기본 이미지 생성 및 업로드 (`og-default.png`)
- [ ] Google Search Console 등록
- [ ] Sitemap 제출

### 권장 (1주일 내)

- [ ] 로고 이미지 생성 및 업로드 (`logo.png`)
- [ ] Bing Webmaster Tools 등록
- [ ] Google Analytics 설정

### 선택 (개선 시)

- [ ] PageSpeed Insights 성능 측정
- [ ] Core Web Vitals 모니터링
- [ ] 추가 SEO 최적화

---

## 🎯 예상 소요 시간

- **환경변수 설정**: 2분
- **OG 이미지 생성**: 10-30분 (디자인 능력에 따라)
- **Search Console 등록**: 10분
- **Sitemap 제출**: 2분

**총 예상 시간**: 약 30-50분

---

## ❓ 도움이 필요한 경우

### OG 이미지 생성이 어려운 경우

간단한 텍스트 기반 이미지라도 괜찮습니다. 다음 무료 도구 사용:

- https://www.canva.com/ (가장 쉬움)
- https://www.photopea.com/ (Photoshop 대체)

### 환경변수 설정 방법

1. Railway 대시보드 접속
2. 프로젝트 선택
3. `webapp` 서비스 클릭
4. "Variables" 탭
5. "New Variable" 클릭
6. Name: `PUBLIC_BASE_URL`
7. Value: `https://keerosveltekit-production.up.railway.app`
8. "Add" 클릭
9. 자동 재배포 대기

---

## 🚀 완료 후 확인사항

배포 완료 후 다음 URL들을 테스트하세요:

1. **홈페이지**: https://keerosveltekit-production.up.railway.app/
2. **Sitemap**: https://keerosveltekit-production.up.railway.app/sitemap.xml
3. **robots.txt**: https://keerosveltekit-production.up.railway.app/robots.txt
4. **ads.txt**: https://keerosveltekit-production.up.railway.app/ads.txt

### OG 태그 테스트

- **Facebook**: https://developers.facebook.com/tools/debug/
- **Twitter**: https://cards-dev.twitter.com/validator
- **LinkedIn**: https://www.linkedin.com/post-inspector/

---

**작성일**: 2025-12-30
**작성자**: AI Assistant
