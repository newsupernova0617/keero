// 광고 설정
export const AD_CONFIG = {
    // Google AdSense
    adsense: {
        enabled: false, // 승인 후 true로 변경
        client: 'ca-pub-2995631331341713', // ads.txt와 일치
        slots: {
            header: '1234567890', // 헤더 배너
            footer: '1234567891', // 푸터 배너
            inFeed: '1234567892', // 피드 내 광고
            inArticle: '1234567893', // 본문 중간 광고
            sidebar: '1234567894' // 사이드바 광고
        }
    },

    // 네이버 애드포스트
    adpost: {
        enabled: false, // 웹사이트 불가
        units: {
            header: 'UNIT-XXXXXXXX-1', // 헤더 배너
            footer: 'UNIT-XXXXXXXX-2', // 푸터 배너
            inFeed: 'UNIT-XXXXXXXX-3', // 피드 내 광고
            inArticle: 'UNIT-XXXXXXXX-4' // 본문 중간 광고
        }
    },

    // 카카오 애드핏
    adfit: {
        enabled: true, // AdSense 미승인 시 true로 변경
        units: {
            header: 'DAN-XXXXXXXXXXXXXXXX', // 헤더 배너 (728x90)
            footer: 'DAN-YYYYYYYYYYYYYYYY', // 푸터 배너 (728x90)
            inFeed: 'DAN-ZZZZZZZZZZZZZZZZ', // 피드 내
            inArticle: 'DAN-AAAAAAAAAAAAAAAA', // 본문 중간
            mobile: 'DAN-BBBBBBBBBBBBBBBB', // 모바일 배너
            sidebar: 'DAN-CCCCCCCCCCCCCCCC', // 사이드바
            mediumRectangle: 'DAN-r7zwxqiBXJy8ONPu', // 300x250 중형 직사각형
            leaderboard: 'DAN-AIl1kDMY7LlVY3S4', // 728x90 리더보드 (데스크톱)
            mobileLarge: 'DAN-Cb3IghrE9LSBEjZm' // 320x100 모바일 대형 배너
        }
    }
}

// 광고 표시 규칙
export const AD_RULES = {
    // 피드 광고 간격 (N개 게시글마다)
    feedInterval: 6,

    // 본문 광고 위치 (본문 길이의 N%)
    articlePosition: 0.5,

    // 모바일에서만 표시할 광고
    mobileOnly: ['adfit'],

    // 데스크톱에서만 표시할 광고
    desktopOnly: []
}
