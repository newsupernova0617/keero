# 관리자 권한 설정 가이드

## 현재 상태

- `/admin` 접근 시 303 리다이렉트 발생
- 원인: 로그인 안 됨 또는 관리자 권한 없음

## 해결 방법

### 1. 로그인

1. https://keero.site/auth/login 접속
2. Supabase 계정으로 로그인

### 2. 관리자 권한 확인

- **자동 관리자**: `yj43773@gmail.com` 이메일로 로그인하면 자동으로 관리자 권한 부여
- **수동 설정**: DB에서 role을 99로 변경

### 3. DB에서 관리자 권한 부여 (필요시)

**Railway CLI 사용**:

```bash
# Railway DB 접속
railway connect

# SQLite 쿼리 실행
sqlite3 data/posts.db

# 관리자 권한 부여
UPDATE users SET role = 99 WHERE email = 'yj43773@gmail.com';

# 확인
SELECT email, role FROM users;
```

**또는 Railway 대시보드**:

1. Railway 프로젝트 → webapp 서비스
2. Data 탭
3. SQLite 쿼리 실행

## 관리자 권한 체크 로직

`/admin/+layout.server.ts`:

```typescript
// 관리자 조건:
// 1. users 테이블에서 role = 99
// 2. 또는 email = 'yj43773@gmail.com'
const isAdmin =
  (dbUser && dbUser.length > 0 && dbUser[0].role === 99) ||
  user.email === "yj43773@gmail.com";
```

## 개발 중 임시 해결

개발 환경에서만 관리자 체크를 비활성화하려면:

```typescript
// admin/+layout.server.ts
const isAdmin =
  process.env.NODE_ENV === "development" || // 개발 환경에서는 모두 관리자
  (dbUser && dbUser.length > 0 && dbUser[0].role === 99) ||
  user.email === "yj43773@gmail.com";
```

⚠️ **주의**: 프로덕션에서는 반드시 제거하세요!
