const Database = require('better-sqlite3');

const db = new Database('./data/app.db');

// 이미지 총 개수 확인
const totalImages = db.prepare('SELECT COUNT(*) as count FROM images').get();
console.log('총 이미지 개수:', totalImages.count);

// 게시물별 이미지 개수 확인
const postImages = db.prepare(`
    SELECT 
        p.id,
        p.title,
        COUNT(i.id) as image_count
    FROM posts p
    LEFT JOIN images i ON p.id = i.post_id
    GROUP BY p.id
    ORDER BY p.id DESC
    LIMIT 10
`).all();

console.log('\n최근 게시물 10개의 이미지 개수:');
postImages.forEach(post => {
    console.log(`ID ${post.id}: "${post.title}" - 이미지 ${post.image_count}개`);
});

// 이미지가 있는 게시물 샘플 확인
const sampleImages = db.prepare(`
    SELECT 
        i.id,
        i.post_id,
        i.r2_url,
        i.media_type
    FROM images i
    LIMIT 5
`).all();

console.log('\n이미지 샘플 (최대 5개):');
sampleImages.forEach(img => {
    console.log(`이미지 ID ${img.id} (게시물 ${img.post_id}): ${img.r2_url}`);
});

db.close();
