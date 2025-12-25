# 크롤링 사이트 체크리스트

## 진행 상태

- [x] 루리웹 (Ruliweb) ✅ 완료
- [x] 오유 (Todayhumor) ✅ 완료
- [x] 웃대 (Humoruniv) ✅ 완료
- [x] 뽐뿌 (Ppomppu) ✅ 완료
- [x] 개드립 (Dogdrip) ✅ 완료
- [x] 펨코 (Fmkorea) ✅ 완료
- [ ] ~~엠팍 (Mlbpark)~~ 🚫 비활성화
- [ ] ~~클리앙 (Clien)~~ 🚫 비활성화

---

## 완료된 사이트 상세

### ✅ 뽐뿌 (Ppomppu)

- **URL**: https://www.ppomppu.co.kr/hot.php?category=2
- **타입**: HOT 게시물 (유머/자유 혼합)
- **Selector**: `tr.baseList` (게시글 목록)
- **완료 날짜**: 2025-12-25
- **특이사항**:
  - freeboard (자유게시판) 필터링 추가
  - humor (유머게시판)만 크롤링
  - 제목 파싱 정상 확인

### ✅ 웃긴대학 (Humoruniv)

- **URL**: https://m.humoruniv.com/board/list.html?table=pds
- **타입**: 모바일 버전
- **Selector**: `a.list_body_href[href*='read']` (일반 게시글, 최신순)
- **완료 날짜**: 2025-12-24
- **특이사항**:
  - "원본" 버튼 제거 로직 추가
  - 일반 게시물 크롤링 (베스트 아님)
  - 이미지 정상 크롤링 확인

---

## 작업 대기 중

**펨코 (Fmkorea)**: Selector 검증 필요
