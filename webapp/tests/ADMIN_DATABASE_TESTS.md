# Admin Database Management 테스트 가이드 (개선판)

## 📋 테스트 파일 목록

### ✅ **보안 및 핵심 로직 테스트 (NEW!)**

#### 1. `crud-security.test.ts` - 18개 테스트

**CRUD 보안 및 권한 검증**

- ✅ SQL Injection 방지 - 특수문자 포함 테이블명 차단
- ✅ SQL Injection 방지 - whitelist 기반 검증
- ✅ 권한 검증 - canCreate: false 테이블
- ✅ 권한 검증 - canEdit: false 테이블
- ✅ 권한 검증 - canDelete: false 테이블
- ✅ 권한 검증 - editable: false 필드
- ✅ 필수 필드 검증 - required 필드 확인
- ✅ 데이터 타입 검증 - 컬럼 타입 정의
- ✅ select 타입 options 구조 검증
- ✅ 메타데이터 일관성 - primaryKey 존재
- ✅ 실제 DB 작업 - INSERT/SELECT/UPDATE/DELETE

#### 2. `sql-query-security.test.ts` - 20개 테스트

**SQL 쿼리 실행기 보안**

- ✅ 읽기 전용 모드 - SELECT만 허용
- ✅ 읽기 전용 모드 - UPDATE/DELETE/INSERT 차단
- ✅ 위험한 쿼리 감지 - WHERE 없는 DELETE
- ✅ 위험한 쿼리 감지 - WHERE 없는 UPDATE
- ✅ 위험한 쿼리 감지 - DROP TABLE
- ✅ 위험한 쿼리 감지 - TRUNCATE
- ✅ 쿼리 유효성 검증 - 빈 쿼리, 주석, 여러 줄
- ✅ 에러 케이스 - 잘못된 문법, 존재하지 않는 테이블

#### 3. `r2-backup-mock.test.ts` - 19개 테스트 (NEW!)

**R2 백업 로직 (Mock, 빠른 실행)**

- ✅ 백업 파일명 생성 - 타임스탬프 형식
- ✅ R2 키 생성 - backups/ 접두사
- ✅ 메타데이터 구조 검증
- ✅ 파일 크기 포맷팅 (Bytes/KB/MB/GB)
- ✅ 백업 목록 정렬 - 최신순
- ✅ 복원 안전성 - 현재 DB 자동 백업
- ✅ 에러 처리 - 존재하지 않는 파일, 네트워크 오류
- ✅ URL 생성 및 인코딩

### ✅ **기존 테스트**

#### 4. `admin-database.spec.ts` - 11개 테스트

**E2E 브라우저 테스트**

- ✅ 메인 대시보드 로드
- ✅ 테이블 목록 페이지
- ✅ SQL 쿼리 실행기 UI
- ✅ 백업 관리 페이지
- ✅ 성능 모니터링 페이지
- ✅ 감사 로그 페이지

#### 5. `r2-backup.test.ts` - 6개 테스트

**R2 통합 테스트 (실제 R2 호출)**

- ✅ 백업 파일 R2 업로드
- ✅ R2 백업 목록 조회
- ✅ R2 백업 다운로드
- ✅ R2 백업 삭제
- ✅ 에러 처리

#### 6. `table-metadata.test.ts` - 8개 테스트

**메타데이터 시스템**

- ✅ 테이블 메타데이터 구조
- ✅ 권한 설정 확인
- ✅ 컬럼 타입 검증

---

## 📊 테스트 통계

### **총 82개 테스트**

| 카테고리        | 테스트 수 | 실행 속도 |
| --------------- | --------- | --------- |
| **보안 테스트** | 38개      | ⚡ 빠름   |
| **단위 테스트** | 27개      | ⚡ 빠름   |
| **통합 테스트** | 6개       | 🐢 느림   |
| **E2E 테스트**  | 11개      | 🐢 느림   |

### **커버리지**

- ✅ SQL Injection 방지
- ✅ 권한 검증
- ✅ 데이터 유효성 검사
- ✅ 위험한 쿼리 감지
- ✅ 에러 처리
- ✅ 실제 DB 작업
- ✅ R2 백업 로직
- ✅ UI 렌더링

---

## 🚀 테스트 실행 방법

### **빠른 테스트 (보안 + 로직)**

```bash
# 보안 테스트만 실행 (1초 이내)
npm run test tests/crud-security.test.ts
npm run test tests/sql-query-security.test.ts

# R2 Mock 테스트 (1초 이내)
npm run test tests/r2-backup-mock.test.ts

# 메타데이터 테스트 (1초 이내)
npm run test tests/table-metadata.test.ts
```

### **통합 테스트 (실제 R2 호출)**

```bash
# R2 환경 변수 필요
npm run test tests/r2-backup.test.ts
```

### **E2E 테스트 (브라우저)**

```bash
# 개발 서버 실행 필요
npx playwright test tests/admin-database.spec.ts
```

### **전체 테스트**

```bash
# 모든 단위 테스트 (빠름)
npm run test -- --exclude tests/r2-backup.test.ts --exclude tests/admin-database.spec.ts

# 모든 테스트 (느림)
npm run test && npx playwright test
```

---

## 🎯 테스트 우선순위

### **1순위: 보안 테스트 (필수)**

```bash
npm run test tests/crud-security.test.ts
npm run test tests/sql-query-security.test.ts
```

**이유:** SQL Injection, 권한 우회 등 치명적 취약점 검증

### **2순위: 로직 테스트**

```bash
npm run test tests/r2-backup-mock.test.ts
npm run test tests/table-metadata.test.ts
```

**이유:** 핵심 비즈니스 로직 검증

### **3순위: 통합 테스트**

```bash
npm run test tests/r2-backup.test.ts
```

**이유:** 외부 서비스 연동 확인 (느림, 비용 발생)

### **4순위: E2E 테스트**

```bash
npx playwright test
```

**이유:** 전체 플로우 확인 (가장 느림)

---

## ⚠️ 주의사항

### **보안 테스트**

- ✅ **자동 실행 가능** - 외부 의존성 없음
- ✅ **빠른 실행** - 1초 이내
- ⚠️ **실제 DB 사용** - test-data/ 디렉토리에 임시 DB 생성

### **R2 통합 테스트**

- ⚠️ **실제 R2 버킷 사용** - 테스트 파일 업로드
- ⚠️ **환경 변수 필요** - R2\_\* 변수 설정
- ⚠️ **비용 발생 가능** - API 호출
- ✅ **자동 정리** - 테스트 후 파일 삭제

### **E2E 테스트**

- ⚠️ **개발 서버 필요** - `npm run dev` 실행 중이어야 함
- ⚠️ **Admin 권한 필요** - 로그인 로직 구현 필요
- ⚠️ **실제 데이터 의존** - DB에 데이터 필요

---

## � 개선 사항

### **이전 (25개 테스트)**

- ❌ 보안 테스트 없음
- ❌ 비즈니스 로직 테스트 부족
- ❌ R2 테스트가 느림 (실제 호출만)
- ⚠️ UI 렌더링만 확인

### **현재 (82개 테스트)**

- ✅ **보안 테스트 38개** (SQL Injection, 권한 검증)
- ✅ **로직 테스트 충실** (실제 DB 작업 포함)
- ✅ **빠른 Mock 테스트** (R2 로직 검증)
- ✅ **에러 케이스 포함** (20개 이상)

---

## 🎓 테스트 작성 가이드

### **좋은 테스트**

```typescript
// ✅ 명확한 주석
it('SQL Injection 방지 - 특수문자 포함 테이블명 차단', () => {
  // ✅ 구체적인 테스트 케이스
  const maliciousName = "posts'; DROP TABLE users--"

  // ✅ 명확한 검증
  expect(isValidTableName(maliciousName)).toBe(false)
})
```

### **나쁜 테스트**

```typescript
// ❌ 모호한 설명
it('테스트', () => {
  // ❌ 무엇을 테스트하는지 불명확
  const result = someFunction()

  // ❌ 왜 이 값이어야 하는지 불명확
  expect(result).toBe(true)
})
```

---

## ✅ 테스트 승인 체크리스트

### **보안 (필수)**

- [ ] SQL Injection 방지 테스트 통과
- [ ] 권한 검증 테스트 통과
- [ ] 위험한 쿼리 감지 테스트 통과

### **로직**

- [ ] CRUD 작업 테스트 통과
- [ ] 메타데이터 테스트 통과
- [ ] R2 Mock 테스트 통과

### **통합**

- [ ] R2 실제 연동 테스트 통과
- [ ] E2E 테스트 통과

### **정리**

- [ ] 테스트 DB 파일 정리됨
- [ ] R2 테스트 파일 삭제됨

**총 82개 테스트 통과 시 승인 가능** ✅
