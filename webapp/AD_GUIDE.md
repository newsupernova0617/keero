# 광고 컴포넌트 사용 가이드

## 📦 생성된 컴포넌트

### 1. AdSense (Google AdSense)
```svelte
<AdSense 
  slot="1234567890" 
  format="auto" 
  responsive={true}
  className="my-4"
/>
```

**Props:**
- `slot`: AdSense 광고 슬롯 ID (필수)
- `format`: 광고 형식 (`auto`, `rectangle`, `horizontal`, `vertical`)
- `responsive`: 반응형 여부 (기본: `true`)
- `className`: 추가 CSS 클래스

### 2. AdPost (네이버 애드포스트)
```svelte
<AdPost 
  unitId="UNIT-XXXXXXXX-1" 
  width={728} 
  height={90}
  className="my-4"
/>
```

**Props:**
- `unitId`: 애드포스트 유닛 ID (필수)
- `width`: 광고 너비 (기본: 300)
- `height`: 광고 높이 (기본: 250)
- `className`: 추가 CSS 클래스

### 3. AdFit (카카오 애드핏)
```svelte
<AdFit 
  unit="DAN-XXXXXXXXXXXXXXXX" 
  width={320} 
  height={100}
  className="my-4"
/>
```

**Props:**
- `unit`: 애드핏 유닛 ID (필수)
- `width`: 광고 너비 (기본: 320)
- `height`: 광고 높이 (기본: 100)
- `className`: 추가 CSS 클래스

---

## ⚙️ 광고 설정 (`src/lib/config/ads.ts`)

### 광고 플랫폼 활성화/비활성화

```typescript
export const AD_CONFIG = {
  adsense: {
    enabled: false,  // AdSense 승인 후 true로 변경
    client: 'ca-pub-XXXXXXXXXXXXXXXX',
    slots: { ... }
  },
  adpost: {
    enabled: true,   // 기본 활성화
    units: { ... }
  },
  adfit: {
    enabled: false,  // 필요 시 true로 변경
    units: { ... }
  }
}
```

### 광고 표시 규칙

```typescript
export const AD_RULES = {
  feedInterval: 6,        // 6개 게시글마다 광고 표시
  articlePosition: 0.5,   // 본문 50% 위치에 광고
  mobileOnly: ['adfit'],  // 모바일 전용 광고
  desktopOnly: []         // 데스크톱 전용 광고
}
```

---

## 📍 광고 배치 예시

### 홈페이지 (피드 내 광고)

```svelte
{#each data.posts as post, index}
  <!-- 게시글 카드 -->
  <PostCard {post} />

  <!-- 6개마다 광고 표시 -->
  {#if (index + 1) % AD_RULES.feedInterval === 0}
    <div class="col-span-full">
      {#if AD_CONFIG.adsense.enabled}
        <AdSense slot={AD_CONFIG.adsense.slots.inFeed} />
      {:else if AD_CONFIG.adpost.enabled}
        <AdPost unitId={AD_CONFIG.adpost.units.inFeed} />
      {/if}
    </div>
  {/if}
{/each}
```

### 게시글 상세 (본문 중간 광고)

```svelte
<article>
  <h1>{post.title}</h1>
  
  <div class="content">
    {post.content}
  </div>

  <!-- 본문 하단 광고 -->
  {#if AD_CONFIG.adsense.enabled}
    <AdSense slot={AD_CONFIG.adsense.slots.inArticle} format="rectangle" />
  {:else if AD_CONFIG.adpost.enabled}
    <AdPost unitId={AD_CONFIG.adpost.units.inArticle} width={336} height={280} />
  {/if}

  <!-- 댓글 영역 -->
  <Comments />
</article>
```

### 레이아웃 (헤더/푸터 배너)

```svelte
<!-- +layout.svelte -->
<header>
  <!-- 헤더 내용 -->
</header>

<!-- 헤더 하단 배너 -->
{#if AD_CONFIG.adpost.enabled}
  <AdPost unitId={AD_CONFIG.adpost.units.header} width={728} height={90} />
{/if}

<main>
  {@render children()}
</main>

<!-- 푸터 상단 배너 -->
{#if AD_CONFIG.adpost.enabled}
  <AdPost unitId={AD_CONFIG.adpost.units.footer} width={728} height={90} />
{/if}

<footer>
  <!-- 푸터 내용 -->
</footer>
```

---

## 🚀 광고 적용 단계

### 1단계: 광고 플랫폼 가입

#### Google AdSense
1. https://www.google.com/adsense 접속
2. 사이트 등록 및 심사 신청
3. 승인 후 광고 코드 발급
4. `AD_CONFIG.adsense.client`에 ID 입력
5. `AD_CONFIG.adsense.enabled = true`

#### 네이버 애드포스트
1. https://adpost.naver.com 접속
2. 사이트 등록
3. 광고 유닛 생성
4. `AD_CONFIG.adpost.units`에 유닛 ID 입력
5. `AD_CONFIG.adpost.enabled = true`

#### 카카오 애드핏
1. https://adfit.kakao.com 접속
2. 앱/사이트 등록
3. 광고 단위 생성
4. `AD_CONFIG.adfit.units`에 유닛 ID 입력
5. `AD_CONFIG.adfit.enabled = true`

### 2단계: 광고 ID 설정

`src/lib/config/ads.ts` 파일에서 실제 광고 ID로 변경:

```typescript
adsense: {
  client: 'ca-pub-1234567890123456',  // 실제 ID
  slots: {
    header: '9876543210',              // 실제 슬롯 ID
    // ...
  }
}
```

### 3단계: 광고 배치

원하는 페이지에 광고 컴포넌트 추가:

```svelte
<script>
  import AdPost from '$lib/components/ads/AdPost.svelte'
  import { AD_CONFIG } from '$lib/config/ads'
</script>

{#if AD_CONFIG.adpost.enabled}
  <AdPost unitId={AD_CONFIG.adpost.units.header} width={728} height={90} />
{/if}
```

---

## ⚠️ 주의사항

### AdSense 정책
- 클릭 유도 금지
- 광고 라벨 필수 ("광고", "Ads")
- 성인/불법 콘텐츠 금지
- 최소 콘텐츠 요구사항 (30개 이상)

### 광고 개수 제한
- **페이지당 권장**: 3~5개
- **너무 많으면**: 사용자 경험 저하, 승인 거부
- **너무 적으면**: 수익 감소

### 성능 최적화
- 광고 lazy loading 활용
- 광고 스크립트 비동기 로딩
- Core Web Vitals 모니터링

---

## 📊 수익 최적화 팁

### 1. A/B 테스트
- 광고 위치 변경
- 광고 크기 변경
- 광고 개수 조정

### 2. 광고 위치 우선순위
1. **본문 중간** (가장 높은 CTR)
2. **피드 내** (자연스러운 노출)
3. **헤더 하단** (높은 가시성)
4. **댓글 위** (체류 시간 활용)
5. **푸터** (낮은 CTR)

### 3. 모바일 최적화
- 모바일 전용 광고 크기 (320x100, 300x250)
- 스크롤 시 고정 광고 (Sticky Ad)
- 네이티브 광고 활용

---

## 🔧 트러블슈팅

### 광고가 표시되지 않음
1. 광고 ID 확인
2. `enabled: true` 확인
3. 브라우저 콘솔 에러 확인
4. 광고 차단 프로그램 비활성화

### 광고 승인 거부
1. 콘텐츠 품질 개선 (30개 이상)
2. 개인정보처리방침 추가
3. 이용약관 추가
4. 불법/성인 콘텐츠 제거

### 수익이 낮음
1. 트래픽 증가 (SEO 최적화)
2. 광고 위치 최적화
3. 광고 크기 변경
4. 다른 광고 플랫폼 병행
