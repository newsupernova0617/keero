# 크롤링 사이트 체크리스트

## 진행 상태

- [x] 루리웹 (Ruliweb) ✅ 완료
- [x] 오유 (Todayhumor) ✅ 완료
- [x] 웃대 (Humoruniv) ✅ 완료
- [ ] 뽐뿌 (Ppomppu)
- [x] 개드립 (Dogdrip) ✅ 완료
- [ ] 펨코 (Fmkorea)
- [ ] ~~엠팍 (Mlbpark)~~ 🚫 비활성화
- [ ] ~~클리앙 (Clien)~~ 🚫 비활성화

---

## 완료된 사이트 상세

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

나머지 사이트들은 selector 설정 및 테스트 필요
