# 에이전트 작업 위임 프롬프트 템플릿

## 📋 프롬프트 작성 원칙

### ✅ 좋은 프롬프트의 특징
1. **명확한 목표**: 무엇을 달성해야 하는지 구체적으로 명시
2. **컨텍스트 제공**: 관련 파일 경로와 현재 상태 설명
3. **검증 기준**: 완료 여부를 어떻게 확인할지 명시
4. **제약 사항**: 하지 말아야 할 것 명시

### ❌ 피해야 할 것
- 모호한 지시 ("잘 해줘", "알아서 해줘")
- 너무 많은 작업을 한 번에 요청
- 검증 방법 누락
- 파일 경로 누락

---

# Part 1: Crawler 작업

## 1️⃣ 의존성 설치

```
프로젝트: C:\Users\yj437\OneDrive\Desktop\coding_windows\aagag_clone

작업: Python 크롤러 의존성 설치

참고 문서:
- task.md (프로젝트 루트)

구체적 작업:
1. crawler 폴더로 이동
2. venv 활성화
3. pip install -r requirements.txt

검증 방법:
- python -c "from bs4 import BeautifulSoup" 에러 없음
- pytest --version 정상 출력

완료 조건:
- 모든 패키지 설치 완료
```

---

## 2️⃣ 타겟 사이트 설정

```
프로젝트: C:\Users\yj437\OneDrive\Desktop\coding_windows\aagag_clone

작업: 실제 크롤링 대상 사이트 설정

참고 문서:
- task.md
- crawler/config.py

구체적 작업:
1. 크롤링할 유머 커뮤니티 사이트 선정
2. HTML 구조 분석 (브라우저 개발자 도구)
3. CSS 선택자 매핑: post_list, post_link, title, content, images, date
4. config.py의 TARGET_SITES에 추가
5. robots.txt 확인

주의사항:
- Rate limiting 고려 (1초 딜레이)
- 예제 사이트는 enabled: False로 변경

완료 조건:
- config.py에 실제 사이트 1개 이상 추가
- 모든 필수 선택자 설정 완료
```

---

## 3️⃣ 크롤링 테스트

```
프로젝트: C:\Users\yj437\OneDrive\Desktop\coding_windows\aagag_clone

작업: 실제 크롤링 테스트 실행

선행 조건: 의존성 설치 + 타겟 사이트 설정 완료

구체적 작업:
1. crawler 폴더에서 python main.py 실행
2. 데이터 검증:
   - data/app.db 생성 확인
   - posts, images 테이블 조회
   - R2 이미지 업로드 확인

검증 방법:
- sqlite3 data/app.db "SELECT COUNT(*) FROM posts"
- sqlite3 data/app.db "SELECT title FROM posts LIMIT 5"

완료 조건:
- 최소 5개 게시글 크롤링 성공
- 이미지 R2 업로드 확인
```

---

## 4️⃣ 미디어 최적화 구현

```
프로젝트: C:\Users\yj437\OneDrive\Desktop\coding_windows\aagag_clone

작업: 이미지/GIF/동영상 최적화 로직 구현

참고 문서:
- task.md (미디어 최적화 섹션)
- crawler/storage.py

구체적 작업:
1. Pillow로 이미지 WebP 변환 함수 구현
2. FFmpeg로 동영상 최적화 함수 구현
3. storage.py의 save_image_smart() 수정
4. 미디어 타입 감지 로직 추가

검증 방법:
- 테스트 이미지로 변환 테스트
- 용량 절감 확인

완료 조건:
- JPG/PNG → WebP 변환 동작
- 용량 메타데이터 기록됨
```

---

# Part 2: SvelteKit 웹앱

## 5️⃣ SvelteKit 프로젝트 초기화

```
프로젝트: C:\Users\yj437\OneDrive\Desktop\coding_windows\aagag_clone

작업: SvelteKit 프로젝트 생성 및 기본 설정

참고 문서:
- task.md (Phase 1)
- webapp_plan.md

구체적 작업:
1. npx sv create . (또는 src/ 폴더에)
   - TypeScript 선택
   - Tailwind CSS 선택
   - Drizzle ORM 선택 (better-sqlite3)
2. shadcn-svelte 설치: npx shadcn-svelte@latest init
3. 기본 테마 설정

검증 방법:
- npm run dev 실행
- localhost:5173 접속 확인

완료 조건:
- SvelteKit 정상 실행
- Tailwind + shadcn 적용됨
```

---

## 6️⃣ Supabase Auth 연동

```
프로젝트: C:\Users\yj437\OneDrive\Desktop\coding_windows\aagag_clone

작업: Supabase Auth 설정 및 OAuth 연동

참고 문서:
- webapp_plan.md (인증 섹션)

구체적 작업:
1. Supabase 프로젝트 생성 (supabase.com)
2. 카카오, 구글 OAuth 설정
3. 환경 변수 설정: SUPABASE_URL, SUPABASE_ANON_KEY
4. @supabase/supabase-js 설치
5. @supabase/auth-helpers-sveltekit 설치
6. OAuth 콜백 처리 구현

주의사항:
- 첫 로그인 시 로컬 SQLite users 테이블에 INSERT 필요

검증 방법:
- 카카오/구글 로그인 테스트
- 세션 유지 확인

완료 조건:
- OAuth 로그인 동작
- 로컬 DB에 사용자 생성됨
```

---

## 7️⃣ SQLite + Drizzle 설정

````
프로젝트: C:\Users\yj437\OneDrive\Desktop\coding_windows\aagag_clone

작업: better-sqlite3 + Drizzle ORM 설정

참고 문서:
- webapp_plan.md (데이터베이스 전략 섹션)

구체적 작업:
1. src/lib/server/db.ts 생성
2. PRAGMA 설정 (WAL, synchronous, cache_size 등)
3. Drizzle 스키마 정의 (posts, images, users, comments 등)
4. 읽기/쓰기 테스트

코드 참고:
```typescript
import Database from 'better-sqlite3';
import { drizzle } from 'drizzle-orm/better-sqlite3';

const sqlite = new Database('data/app.db');
sqlite.pragma('journal_mode = WAL');
sqlite.pragma('synchronous = NORMAL');

export const db = drizzle(sqlite);
```

테스트 (구현 직후 수행):
- [ ] npm run dev 실행
- [ ] 브라우저 콘솔에서 DB 에러 없는지 확인
- [ ] 간단한 조회 쿼리 실행: db.select().from(posts).limit(1)
- [ ] 결과 데이터 확인

완료 조건:
- 모든 테스트 통과
- DB 연결 정상
- 크롤링된 posts 조회 가능
````

---

## 8️⃣ 게시글 목록/상세 페이지

```
프로젝트: C:\Users\yj437\OneDrive\Desktop\coding_windows\aagag_clone

작업: 게시글 목록 및 상세 페이지 구현

참고 문서:
- webapp_plan.md (페이지 구조)

구체적 작업:
1. / (목록 페이지)
   - PostCard 컴포넌트
   - 페이지네이션
   - WHERE related_post_id IS NULL (원본만)
2. /post/[id] (상세 페이지)
   - 본문 표시
   - 이미지 갤러리 (lazy loading)
   - 좋아요 버튼

주의사항:
- 이미지 URL은 R2 Custom Domain 사용

테스트 (구현 직후 수행):
- [ ] npm run dev 실행
- [ ] / 접속하여 게시글 목록 표시 확인
- [ ] PostCard 레이아웃 정상 확인
- [ ] 페이지네이션 버튼 클릭 동작 확인
- [ ] 게시글 클릭하여 상세 페이지 이동
- [ ] 상세 페이지에서 본문/이미지 표시 확인
- [ ] 이미지 lazy loading 동작 확인 (스크롤)
- [ ] 좋아요 버튼 UI 확인

완료 조건:
- 모든 테스트 통과
- 게시글 목록 표시
- 상세 페이지 동작
- 이미지 정상 로드
```

---

## 9️⃣ 댓글 시스템

```
프로젝트: C:\Users\yj437\OneDrive\Desktop\coding_windows\aagag_clone

작업: 댓글 및 대댓글 기능 구현

참고 문서:
- webapp_plan.md (댓글 시스템, 스키마)

구체적 작업:
1. 댓글 목록 컴포넌트 (대댓글 포함)
2. 댓글 작성 폼 (로그인 필요)
3. 댓글 수정/삭제 (본인만)
4. 댓글 좋아요

주의사항:
- XSS 방지: DOMPurify로 sanitize
- Rate limiting: 10초당 1개

테스트 (구현 직후 수행):
- [ ] 게시글 상세 페이지에서 댓글 목록 확인
- [ ] 로그인 후 댓글 작성 폼 표시 확인
- [ ] 댓글 작성 → 목록에 즉시 표시
- [ ] 내 댓글 수정 버튼 표시 확인
- [ ] 댓글 수정 기능 동작
- [ ] 댓글 삭제 기능 동작
- [ ] 대댓글 작성 → 들여쓰기 표시
- [ ] 댓글 좋아요 버튼 클릭 → 숫자 증가
- [ ] Rate limiting 테스트 (10초 내 2회 작성 시도)

완료 조건:
- 모든 테스트 통과
- 댓글 CRUD 동작
- 대댓글 표시
- 좋아요 동작
```

---

## 🔟 검색 기능 (FTS5)

````
프로젝트: C:\Users\yj437\OneDrive\Desktop\coding_windows\aagag_clone

작업: 게시글 검색 기능 구현

참고 문서:
- webapp_plan.md
- storage.py (FTS5 테이블 이미 생성됨)

구체적 작업:
1. 검색바 UI 구현 (shadcn Input)
2. /search?q=검색어 라우트
3. FTS5 쿼리 구현

FTS5 쿼리 예시:
```sql
SELECT posts.* FROM posts
JOIN posts_fts ON posts.id = posts_fts.rowid
WHERE posts_fts MATCH ? AND posts.related_post_id IS NULL
```

테스트 (구현 직후 수행):
- [ ] 검색바에 테스트 키워드 입력
- [ ] /search?q=키워드 페이지로 이동 확인
- [ ] 검색 결과 목록 표시 확인
- [ ] 검색어가 포함된 게시글만 표시되는지 확인
- [ ] 중복 게시글(related_post_id != NULL) 제외 확인
- [ ] 검색 결과 없을 때 "결과 없음" 메시지 표시

완료 조건:
- 모든 테스트 통과
- 검색 동작
- FTS5 쿼리 정상 작동
````

---

## 1️⃣1️⃣ 관리자 기능

```
프로젝트: C:\Users\yj437\OneDrive\Desktop\coding_windows\aagag_clone

작업: 관리자 페이지 구현

참고 문서:
- webapp_plan.md (관리자 기능)
- task.md (Phase 6)

구체적 작업:
1. /admin 레이아웃 (role=99 체크)
2. /admin/posts - 게시글 관리 (삭제/숨김)
3. /admin/comments - 댓글 관리
4. /admin/users - 사용자 관리 (차단)
5. /admin/reports - 신고 관리
6. /admin (대시보드) - 통계

테스트 (구현 직후 수행):
- [ ] 일반 사용자로 /admin 접근 → 403 또는 리다이렉트
- [ ] 관리자(role=99)로 /admin 접근 → 대시보드 표시
- [ ] /admin/posts에서 게시글 목록 확인
- [ ] 게시글 삭제 버튼 → 확인 모달 → 삭제 동작
- [ ] /admin/comments에서 댓글 목록 확인
- [ ] 댓글 삭제 동작 확인
- [ ] /admin/users에서 사용자 목록 확인
- [ ] 사용자 차단 기능 동작 확인
- [ ] /admin/reports에서 신고 목록 확인
- [ ] 대시보드 통계 (게시글 수, 사용자 수 등) 표시 확인

완료 조건:
- 모든 테스트 통과
- 관리자만 접근 가능
- 모든 CRUD 동작
```

---

# Part 3: 배포

## 1️⃣2️⃣ Railway 배포

```
프로젝트: C:\Users\yj437\OneDrive\Desktop\coding_windows\aagag_clone

작업: Railway에 webapp + crawler 배포

참고 문서:
- task.md (Part 3: 배포)

구체적 작업:
1. Railway 프로젝트 생성
2. webapp 서비스 생성:
   - Root: /
   - Build: npm run build
   - Start: node build
3. crawler 서비스 생성:
   - Root: /crawler
   - Build: pip install -r requirements.txt
   - Start: python main.py
   - Cron: 0 */2 * * *
4. 공유 볼륨 설정: /data
5. R2 Custom Domain 설정

환경 변수:
- webapp: SUPABASE_URL, SUPABASE_ANON_KEY, DATABASE_PATH
- crawler: R2_*, DB_PATH

완료 조건:
- 두 서비스 모두 실행
- 같은 DB 파일 공유
- 크롤러 Cron 동작
```

---

# 🔄 병렬 실행 전략

## 독립적으로 실행 가능 (병렬)
- 1️⃣ 의존성 설치
- 5️⃣ SvelteKit 초기화

## 순차 실행 필요
```
1️⃣ 의존성 설치 → 2️⃣ 타겟 사이트 → 3️⃣ 크롤링 테스트 → 4️⃣ 미디어 최적화
                                                    ↓
5️⃣ SvelteKit 초기화 → 6️⃣ Supabase Auth → 7️⃣ SQLite 설정 → 8️⃣ 페이지 구현
                                                            ↓
                                     9️⃣ 댓글 시스템 → 🔟 검색 → 1️⃣1️⃣ 관리자
                                                            ↓
                                                      1️⃣2️⃣ Railway 배포
```

---

# 💡 프롬프트 작성 팁

## 1. 파일 경로는 절대 경로 사용
```
❌ "config.py 수정해줘"
✅ "C:\Users\yj437\OneDrive\Desktop\coding_windows\aagag_clone\crawler\config.py 수정해줘"
```

## 2. 현재 상태 명시
```
❌ "테스트 추가해줘"
✅ "현재 scraper.py 커버리지가 26%인데, 80%로 올려줘."
```

## 3. 검증 방법 구체화
```
❌ "잘 되는지 확인해줘"
✅ "npm run dev 실행해서 localhost:5173 접속되는지 확인해줘"
```

## 4. 제약 사항 명시
```
✅ "기존 코드 로직은 변경하지 말고, 테스트만 추가해줘"
✅ "shadcn-svelte의 기본 컴포넌트만 사용해줘"
```
