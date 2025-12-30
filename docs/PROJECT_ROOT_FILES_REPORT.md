# 📁 프로젝트 루트 파일 보고서

> **생성일**: 2025-12-29  
> 프로젝트 루트 디렉토리의 모든 파일에 대한 설명

---

## 📊 파일 분류

| 분류               | 파일 수 | 설명                                            |
| ------------------ | ------- | ----------------------------------------------- |
| 📚 문서            | 11개    | 가이드, 분석, 계획 문서                         |
| 🐍 Python 스크립트 | 7개     | 테스트 및 유틸리티 도구                         |
| ⚙️ 설정            | 3개     | Node.js 및 Railway 설정                         |
| 📁 디렉토리        | 6개     | crawler, webapp, data, docs, node_modules, .git |

---

## 📚 문서 파일 (Documentation)

### 🟢 **핵심 가이드**

#### [API_MODE_GUIDE.md](file:///home/yj437/coding/aagag_clone/API_MODE_GUIDE.md)

- **목적**: API 게이트웨이 모드 사용법 간단 가이드
- **내용**: 로컬 개발, Railway 배포, 모드 전환, 문제 해결
- **대상**: 개발자 (빠른 참고용)

#### [RAILWAY_API_DEPLOY.md](file:///home/yj437/coding/aagag_clone/RAILWAY_API_DEPLOY.md)

- **목적**: Railway API 모드 배포 상세 가이드
- **내용**: 환경변수, 볼륨 설정, 배포 절차, 검증 방법
- **대상**: DevOps/배포 담당자

#### [RAILWAY_DEPLOY.md](file:///home/yj437/coding/aagag_clone/RAILWAY_DEPLOY.md)

- **목적**: Railway 기본 배포 가이드 (로컬 DB 모드)
- **내용**: Webapp과 Crawler의 Railway 배포 방법
- **대상**: 초기 배포 시 참고

---

### 🟡 **테스트 및 분석**

#### [TEST_PLAN.md](file:///home/yj437/coding/aagag_clone/TEST_PLAN.md)

- **목적**: 전체 프로젝트 테스트 계획
- **내용**: Phase 1 (Crawler), Phase 2 (Webapp E2E), Phase 3 (통합)
- **상태**: Phase 2 진행 중

#### [FINAL_TEST_REPORT.md](file:///home/yj437/coding/aagag_clone/FINAL_TEST_REPORT.md)

- **목적**: 최종 테스트 결과 보고서
- **내용**: Crawler 테스트 실패 분석 및 해결책
- **상태**: 테스트 완료

#### [TEST_FAILURE_ANALYSIS.md](file:///home/yj437/coding/aagag_clone/TEST_FAILURE_ANALYSIS.md)

- **목적**: 테스트 실패 원인 상세 분석
- **내용**: KeyError, assertion 실패 등의 근본 원인 분석
- **상태**: 분석 완료

---

### 🔵 **이슈 및 버그 분석**

#### [BUG_ANALYSIS_URL_REPLACEMENT.md](file:///home/yj437/coding/aagag_clone/BUG_ANALYSIS_URL_REPLACEMENT.md)

- **목적**: 이미지 URL 치환 버그 분석
- **내용**: HTML 내 이미지 URL이 R2 URL로 치환되지 않는 문제 분석
- **상태**: 해결됨

#### [IMAGE_FIX_GUIDE.md](file:///home/yj437/coding/aagag_clone/IMAGE_FIX_GUIDE.md)

- **목적**: 이미지 문제 수정 가이드
- **내용**: FMKorea 이미지, lazy loading, 반응형 디자인 수정
- **상태**: 수정 완료

---

### 📋 **계획 및 분석**

#### [implementation_plan.md](file:///home/yj437/coding/aagag_clone/implementation_plan.md)

- **목적**: 초기 구현 계획
- **내용**: 프로젝트 아키텍처 및 구현 단계
- **상태**: 구현 완료

#### [webapp_plan.md](file:///home/yj437/coding/aagag_clone/webapp_plan.md)

- **목적**: 웹앱 기능 계획서
- **내용**: 전체 페이지 구조, 기능 목록, 우선순위
- **상태**: 대부분 구현 완료

#### [crawler_analysis.md](file:///home/yj437/coding/aagag_clone/crawler_analysis.md)

- **목적**: Crawler 분석 문서
- **내용**: Crawler 구조, 주요 함수, 데이터 흐름
- **상태**: 분석 완료

#### [task.md](file:///home/yj437/coding/aagag_clone/task.md)

- **목적**: 작업 목록 및 진행 상황
- **내용**: TODO 리스트, 완료된 작업, 다음 단계
- **상태**: 지속 업데이트

---

### ⚪ **기타 문서**

#### [PHASE2_COMPLETE.md](file:///home/yj437/coding/aagag_clone/PHASE2_COMPLETE.md)

- **목적**: Phase 2 완료 보고서
- **내용**: Webapp E2E 테스트 구현 완료 상태
- **상태**: Phase 2 완료

#### [agent_prompts.md](file:///home/yj437/coding/aagag_clone/agent_prompts.md)

- **목적**: AI 에이전트 프롬프트 모음
- **내용**: 개발 과정에서 사용한 프롬프트 기록
- **상태**: 참고용

---

## 🐍 Python 스크립트 (Utility Scripts)

### 🧪 **테스트 스크립트**

#### [test_api.py](file:///home/yj437/coding/aagag_clone/test_api.py)

- **목적**: SvelteKit Crawler API 통합 테스트
- **기능**:
  - `test_posts_api()` - 게시글 저장 API 테스트
  - `test_logs_api()` - 로그 저장 API 테스트
  - `test_unauthorized()` - 인증 실패 테스트
- **사용법**: `python3 test_api.py`
- **전제조건**: SvelteKit 서버 실행 중 (localhost:5173)

---

### 🔍 **진단 스크립트**

#### [check_content_html.py](file:///home/yj437/coding/aagag_clone/check_content_html.py)

- **목적**: DB의 content_html 필드 확인
- **기능**: content_html이 있는 게시글 조회 및 통계
- **사용법**: `python3 check_content_html.py`
- **참고**: Windows 경로 하드코딩됨 (수정 필요)

#### [check_databases.py](file:///home/yj437/coding/aagag_clone/check_databases.py)

- **목적**: 데이터베이스 파일 존재 및 크기 확인
- **기능**: posts.db, logs.db 상태 체크
- **사용법**: `python3 check_databases.py`

#### [check_db_schema.py](file:///home/yj437/coding/aagag_clone/check_db_schema.py)

- **목적**: 데이터베이스 스키마 확인
- **기능**: 테이블 구조 및 컬럼 출력
- **사용법**: `python3 check_db_schema.py`

---

### 🛠️ **유틸리티 스크립트**

#### [fix_duplicate_images.py](file:///home/yj437/coding/aagag_clone/fix_duplicate_images.py)

- **목적**: 중복 이미지 레코드 정리
- **기능**: 동일한 post_id + order_index 중복 제거
- **사용법**: `python3 fix_duplicate_images.py`
- **주의**: 백업 후 실행 권장

#### [migrate_add_content_html.py](file:///home/yj437/coding/aagag_clone/migrate_add_content_html.py)

- **목적**: content_html 컬럼 추가 마이그레이션
- **기능**: 기존 DB에 content_html 필드 추가
- **사용법**: `python3 migrate_add_content_html.py`
- **상태**: 이미 적용됨

#### [check_images.js](file:///home/yj437/coding/aagag_clone/check_images.js)

- **목적**: Node.js 이미지 확인 스크립트
- **기능**: 이미지 관련 검증 (내용 확인 필요)
- **사용법**: `node check_images.js`

---

## ⚙️ 설정 파일 (Configuration)

### 📦 **Node.js 설정**

#### [package.json](file:///home/yj437/coding/aagag_clone/package.json)

- **목적**: 루트 레벨 Node.js 의존성
- **내용**: `@types/node` TypeScript 타입 정의
- **이유**: webapp에서 사용하는 타입 공유

#### [package-lock.json](file:///home/yj437/coding/aagag_clone/package-lock.json)

- **목적**: Node.js 의존성 잠금 파일
- **내용**: 정확한 패키지 버전 고정
- **관리**: npm이 자동 생성

---

### 🚂 **Railway 설정**

#### [railway.crawler.json](file:///home/yj437/coding/aagag_clone/railway.crawler.json)

- **목적**: Crawler 서비스 Railway 설정
- **내용**: 빌드 명령, 실행 디렉토리, 환경변수
- **사용**: Railway 배포 시 자동 감지

#### [railway.webapp.json](file:///home/yj437/coding/aagag_clone/railway.webapp.json)

- **목적**: Webapp 서비스 Railway 설정
- **내용**: 빌드 명령, 실행 디렉토리, 환경변수
- **사용**: Railway 배포 시 자동 감지

---

## 📁 디렉토리 (Directories)

### 🟢 **핵심 디렉토리**

#### [crawler/](file:///home/yj437/coding/aagag_clone/crawler/)

- **목적**: Python 크롤러 코드
- **구조**:
  - `core/` - 핵심 모듈 (8개)
  - `utils/` - 유틸리티 (13개)
  - `tests/` - 테스트 (24개)
  - `docs/` - 문서 (6개)
  - `archive/` - 백업/결과물 (4개)
- **파일 수**: 105개 (재구조화 완료)

#### [webapp/](file:///home/yj437/coding/aagag_clone/webapp/)

- **목적**: SvelteKit 웹 애플리케이션
- **구조**:
  - `src/routes/` - 페이지 라우트
  - `src/lib/` - 컴포넌트, 유틸
  - `src/lib/server/` - 서버 사이드 코드
- **파일 수**: 214개

#### [data/](file:///home/yj437/coding/aagag_clone/data/)

- **목적**: 데이터베이스 파일 저장
- **내용**:
  - `posts.db` - 게시글 SQLite DB
  - `logs.db` - 로그 SQLite DB
  - `*.db-wal`, `*.db-shm` - WAL 모드 파일
- **파일 수**: 5개

#### [docs/](file:///home/yj437/coding/aagag_clone/docs/)

- **목적**: 추가 문서 보관
- **내용**: 아키텍처, 설계 문서
- **파일 수**: 9개

---

### 🔵 **시스템 디렉토리**

#### [.git/](file:///home/yj437/coding/aagag_clone/.git/)

- **목적**: Git 버전 관리
- **내용**: 커밋 히스토리, 브랜치 정보
- **관리**: Git이 자동 관리

#### [node_modules/](file:///home/yj437/coding/aagag_clone/node_modules/)

- **목적**: Node.js 패키지 저장
- **내용**: `@types/node` 패키지
- **관리**: npm이 자동 관리

---

## 📊 파일 통계

| 카테고리                     | 개수     |
| ---------------------------- | -------- |
| 문서 파일 (.md)              | 11개     |
| Python 스크립트 (.py)        | 7개      |
| JavaScript 파일 (.js, .json) | 3개      |
| 디렉토리                     | 6개      |
| **총 파일**                  | **21개** |
| **총 디렉토리**              | **6개**  |

---

## 🎯 파일 정리 권장사항

### ✅ 보관 필요

- **API_MODE_GUIDE.md** - 현역 가이드
- **RAILWAY_API_DEPLOY.md** - 배포 필수 문서
- **test_api.py** - API 테스트 필수
- **railway.\*.json** - Railway 배포 설정

### 📦 정리 가능 (docs/ 이동)

- **TEST_PLAN.md** → `docs/testing/`
- **FINAL_TEST_REPORT.md** → `docs/testing/`
- **TEST_FAILURE_ANALYSIS.md** → `docs/testing/`
- **BUG*ANALYSIS*\*.md** → `docs/issues/`
- **IMAGE_FIX_GUIDE.md** → `docs/guides/`
- **implementation_plan.md** → `docs/planning/`
- **webapp_plan.md** → `docs/planning/`
- **crawler_analysis.md** → `docs/analysis/`
- **PHASE2_COMPLETE.md** → `docs/milestones/`
- **agent_prompts.md** → `docs/development/`

### 🔧 수정 필요

- **check_content_html.py** - Windows 경로 하드코딩 → 상대 경로로 수정

### ❌ 삭제 가능

- **task.md** - 내용이 오래됨 (최신화 또는 삭제)

---

## 🗂️ 제안 구조

```
aagag_clone/
├── 📁 crawler/              # 크롤러 (재구조화 완료)
├── 📁 webapp/               # 웹앱
├── 📁 data/                 # 데이터베이스
├── 📁 docs/                 # 모든 문서 통합
│   ├── guides/              # API_MODE, RAILWAY_DEPLOY
│   ├── testing/             # TEST_PLAN, REPORTS
│   ├── issues/              # BUG_ANALYSIS
│   ├── planning/            # implementation_plan, webapp_plan
│   ├── analysis/            # crawler_analysis
│   ├── milestones/          # PHASE2_COMPLETE
│   └── development/         # agent_prompts
├── 📁 scripts/              # 모든 스크립트 통합
│   ├── test_api.py
│   ├── check_*.py
│   ├── fix_*.py
│   └── migrate_*.py
├── .git/
├── node_modules/
├── package.json
├── package-lock.json
├── railway.crawler.json
└── railway.webapp.json
```

---

## 📌 요약

### 현재 상태

- ✅ Crawler 재구조화 완료 (65 → 10 루트 파일)
- ⚠️ 프로젝트 루트에 21개 파일 (정리 필요)
- ⚠️ 문서 11개가 루트에 분산

### 개선 효과 (정리 후)

- 루트 파일: **21개 → 8개** (62% 감소)
- 문서 집중화: `docs/` 폴더로 통합
- 스크립트 집중화: `scripts/` 폴더로 통합

---

_프로젝트 루트 파일 분석 완료_
