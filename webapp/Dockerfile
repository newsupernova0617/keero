FROM node:20-slim

WORKDIR /app

# 의존성 파일 복사 및 설치
COPY package*.json ./
RUN npm ci

# 애플리케이션 코드 복사
COPY . .

# 빌드
RUN npm run build

# 프로덕션 의존성만 설치
RUN npm prune --production

# 데이터 디렉토리 생성
RUN mkdir -p /data

# 포트 노출
EXPOSE 3000

# 프로덕션 서버 실행
CMD ["node", "build"]
