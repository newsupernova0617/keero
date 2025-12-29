# 이미지 표시 문제 해결 가이드

## 문제 상황
게시물에 이미지가 표시되지 않고 "이미지 로딩 중..." 메시지만 나타남

## 원인
Cloudflare R2의 기본 URL (`https://pub-{account_id}.r2.dev`)은 **인증이 필요한 비공개 URL**입니다.
브라우저에서 이미지에 접근하면 **401 Unauthorized** 에러가 발생합니다.

## 해결 방법

### 1단계: Cloudflare R2 Public Access 설정

1. **Cloudflare 대시보드** 접속
   - https://dash.cloudflare.com/ 로그인
   
2. **R2 버킷 설정**
   - 좌측 메뉴에서 `R2` 클릭
   - 사용 중인 버킷 선택 (예: `humor-posts`)
   
3. **Public Access 활성화**
   - `Settings` 탭 클릭
   - `Public Access` 섹션에서 `Allow Access` 클릭
   - 또는 `Custom Domains` 탭에서 커스텀 도메인 연결

4. **Public URL 확인**
   - Public Access 활성화 후 표시되는 URL 복사
   - 예: `https://pub-xxxxxxxxxxxxx.r2.dev`

### 2단계: 환경 변수 설정

#### Crawler 환경 변수 (.env)
```bash
# crawler/.env 파일 생성 또는 수정
R2_PUBLIC_URL=https://pub-xxxxxxxxxxxxx.r2.dev
```

**참고**: `crawler/.env.example` 파일을 복사해서 사용하세요
```bash
cp crawler/.env.example crawler/.env
```

### 3단계: 기존 이미지 URL 마이그레이션

기존에 저장된 이미지 URL을 새로운 공개 URL로 업데이트합니다.

```bash
cd crawler
python migrate_image_urls.py "https://pub-OLD_ACCOUNT_ID.r2.dev" "https://pub-NEW_ACCOUNT_ID.r2.dev"
```

**예시**:
```bash
python migrate_image_urls.py \
  "https://pub-d633a7c3cd0cd71ea3144f17896d4e65.r2.dev" \
  "https://pub-xxxxxxxxxxxxx.r2.dev"
```

### 4단계: 크롤러 재시작

환경 변수 변경 후 크롤러를 재시작하여 새로운 이미지가 올바른 URL로 저장되도록 합니다.

```bash
# Railway에 배포된 경우
railway up

# 로컬에서 실행 중인 경우
cd crawler
python main.py
```

### 5단계: 확인

1. **브라우저에서 이미지 URL 직접 접근**
   ```
   https://pub-xxxxxxxxxxxxx.r2.dev/images/91c11318f5707359f3fca02997c84120.jpg
   ```
   - 이미지가 정상적으로 표시되어야 합니다
   - 401 에러가 나오면 Public Access 설정을 다시 확인하세요

2. **웹사이트에서 게시물 확인**
   - http://localhost:5175/post/114 등의 게시물 페이지 접속
   - 이미지가 정상적으로 표시되는지 확인

## 대안: Custom Domain 사용 (선택사항)

Public URL 대신 자신의 도메인을 사용할 수도 있습니다.

### 장점
- 더 깔끔한 URL (예: `https://cdn.yourdomain.com/images/...`)
- 브랜딩 일관성
- 나중에 CDN 변경 시 유연성

### 설정 방법

1. **Cloudflare R2 대시보드**
   - 버킷 선택 → `Custom Domains` 탭
   - `Connect Domain` 클릭
   - 소유한 도메인 또는 서브도메인 입력 (예: `cdn.yourdomain.com`)

2. **환경 변수 업데이트**
   ```bash
   R2_PUBLIC_URL=https://cdn.yourdomain.com
   ```

3. **마이그레이션 실행**
   ```bash
   python migrate_image_urls.py \
     "https://pub-xxxxxxxxxxxxx.r2.dev" \
     "https://cdn.yourdomain.com"
   ```

## 트러블슈팅

### 이미지가 여전히 안 보이는 경우

1. **브라우저 개발자 도구 확인**
   - F12 → Network 탭
   - 이미지 요청의 상태 코드 확인
   - 401: Public Access 설정 미완료
   - 404: URL이 잘못됨
   - 403: CORS 문제 (R2는 기본적으로 CORS 허용)

2. **데이터베이스 확인**
   ```sql
   SELECT r2_url FROM images LIMIT 5;
   ```
   - URL이 올바른 형식인지 확인

3. **환경 변수 확인**
   ```bash
   cd crawler
   python -c "from config import Config; print(Config.R2_CONFIG['public_url'])"
   ```
   - 공개 URL이 올바르게 설정되었는지 확인

## 참고 자료

- [Cloudflare R2 Public Buckets 문서](https://developers.cloudflare.com/r2/buckets/public-buckets/)
- [Cloudflare R2 Custom Domains 문서](https://developers.cloudflare.com/r2/buckets/public-buckets/#custom-domains)
