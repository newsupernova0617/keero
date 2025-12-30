FROM node:20-slim

WORKDIR /app

# 의존성 파일 복사 및 설치
COPY package*.json ./
RUN npm ci

# 애플리케이션 코드 복사
COPY . .

# 빌드 시점 환경 변수 선언
ARG PUBLIC_SUPABASE_URL
ARG PUBLIC_SUPABASE_ANON_KEY
ARG R2_PUBLIC_URL
# 환경 변수 설정 (필요한 경우)
ARG PUBLIC_ADSENSE_ENABLED=1
ENV PUBLIC_ADSENSE_ENABLED=$PUBLIC_ADSENSE_ENABLED


# 환경 변수를 ENV로 설정 (빌드 시점에 사용)
ENV PUBLIC_SUPABASE_URL=$PUBLIC_SUPABASE_URL
ENV PUBLIC_SUPABASE_ANON_KEY=$PUBLIC_SUPABASE_ANON_KEY
ENV R2_PUBLIC_URL=$R2_PUBLIC_URL

# 빌드 전 동기화 및 빌드
RUN npx svelte-kit sync && npm run build

# 프로덕션 의존성만 설치
RUN npm prune --production

# 데이터 디렉토리 생성
RUN mkdir -p /data

# 포트 노출
EXPOSE 3000

# 프로덕션 서버 실행
CMD ["node", "build"]
