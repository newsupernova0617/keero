import Database from 'better-sqlite3'
import { drizzle } from 'drizzle-orm/better-sqlite3'
import * as schema from './schema'
import { mkdirSync, existsSync } from 'fs'
import { dirname } from 'path'

// DB 경로 (환경 변수로 설정 가능, Railway volume 기본값: /data/posts.db)
const DB_PATH = process.env.DATABASE_PATH || '/data/posts.db'

console.log('🔍 SQLite Connection Debug Info:')
console.log('  - DB_PATH:', DB_PATH)
console.log('  - DATABASE_PATH env:', process.env.DATABASE_PATH)
console.log('  - Current working directory:', process.cwd())

// DB 디렉토리 자동 생성
const dbDir = dirname(DB_PATH)
console.log('  - DB directory:', dbDir)
console.log('  - Directory exists:', existsSync(dbDir))

if (!existsSync(dbDir)) {
    console.log('  - Creating directory:', dbDir)
    try {
        mkdirSync(dbDir, { recursive: true })
        console.log('  ✅ Directory created successfully')
    } catch (error) {
        console.error('  ❌ Failed to create directory:', error)
        throw error
    }
}

console.log('  - DB file exists:', existsSync(DB_PATH))

// SQLite 연결
console.log('🔌 Attempting to connect to SQLite...')
const sqlite = new Database(DB_PATH)
console.log('✅ SQLite connection established')

// PRAGMA 설정 (성능 최적화)
sqlite.pragma('journal_mode = WAL') // Write-Ahead Logging (동시 읽기/쓰기)
sqlite.pragma('synchronous = NORMAL') // 성능과 안정성 균형
sqlite.pragma('cache_size = -64000') // 64MB 캐시
sqlite.pragma('temp_store = MEMORY') // 임시 테이블 메모리 사용
sqlite.pragma('mmap_size = 268435456') // 256MB 메모리 매핑
sqlite.pragma('busy_timeout = 5000') // 잠금 대기 5초

// Drizzle ORM 초기화
export const db = drizzle(sqlite, { schema })

// 테이블 자동 생성 (Railway 배포 대비)
function initializeDatabase() {
    try {
        // 테이블 존재 여부 확인
        const tables = sqlite
            .prepare("SELECT name FROM sqlite_master WHERE type='table' AND name='posts'")
            .get()

        if (!tables) {
            console.log('📦 Initializing database schema...')

            // 모든 테이블 생성
            sqlite.exec(`
                CREATE TABLE IF NOT EXISTS posts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    site_name TEXT NOT NULL,
                    title TEXT NOT NULL,
                    content TEXT,
                    content_html TEXT,
                    content_hash TEXT,
                    source_url TEXT NOT NULL UNIQUE,
                    created_at TEXT NOT NULL,
                    crawled_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    related_post_id INTEGER
                );

                CREATE TABLE IF NOT EXISTS images (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    post_id INTEGER NOT NULL REFERENCES posts(id),
                    media_type TEXT,
                    md5_hash TEXT,
                    perceptual_hash TEXT,
                    r2_key TEXT NOT NULL,
                    r2_url TEXT NOT NULL,
                    original_url TEXT,
                    order_index INTEGER NOT NULL DEFAULT 0,
                    uploaded_at TEXT,
                    is_similar_match INTEGER,
                    duration_seconds INTEGER,
                    frame_count INTEGER,
                    original_size_bytes INTEGER,
                    optimized_size_bytes INTEGER,
                    original_format TEXT,
                    optimized_format TEXT,
                    width INTEGER,
                    height INTEGER,
                    file_size INTEGER
                );

                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    supabase_id TEXT NOT NULL UNIQUE,
                    email TEXT NOT NULL,
                    display_name TEXT,
                    avatar_url TEXT,
                    role INTEGER DEFAULT 1,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                );

                CREATE TABLE IF NOT EXISTS comments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    post_id INTEGER NOT NULL REFERENCES posts(id),
                    user_id INTEGER NOT NULL REFERENCES users(id),
                    parent_comment_id INTEGER,
                    content TEXT NOT NULL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT,
                    is_deleted INTEGER DEFAULT 0
                );

                CREATE TABLE IF NOT EXISTS likes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL REFERENCES users(id),
                    post_id INTEGER REFERENCES posts(id),
                    comment_id INTEGER REFERENCES comments(id),
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                );

                CREATE TABLE IF NOT EXISTS bookmarks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL REFERENCES users(id),
                    post_id INTEGER NOT NULL REFERENCES posts(id),
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                );

                CREATE TABLE IF NOT EXISTS reports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL REFERENCES users(id),
                    post_id INTEGER REFERENCES posts(id),
                    comment_id INTEGER REFERENCES comments(id),
                    reason TEXT NOT NULL,
                    description TEXT,
                    status TEXT DEFAULT 'pending',
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    resolved_at TEXT,
                    resolved_by INTEGER REFERENCES users(id)
                );

                CREATE TABLE IF NOT EXISTS highlights (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    week_start TEXT NOT NULL,
                    week_end TEXT NOT NULL,
                    post_id INTEGER NOT NULL REFERENCES posts(id),
                    rank INTEGER NOT NULL,
                    editor_comment TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                );

                CREATE TABLE IF NOT EXISTS audit_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER REFERENCES users(id),
                    action TEXT NOT NULL,
                    table_name TEXT NOT NULL,
                    record_id INTEGER,
                    old_value TEXT,
                    new_value TEXT,
                    query TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                );

                CREATE TABLE IF NOT EXISTS backup_settings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    enabled INTEGER DEFAULT 0,
                    frequency TEXT DEFAULT 'daily',
                    time TEXT DEFAULT '03:00',
                    retention_days INTEGER DEFAULT 30,
                    last_backup_at TEXT,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                );

                CREATE INDEX IF NOT EXISTS idx_posts_site_name ON posts(site_name);
                CREATE INDEX IF NOT EXISTS idx_posts_crawled_at ON posts(crawled_at);
                CREATE INDEX IF NOT EXISTS idx_images_post_id ON images(post_id);
                CREATE INDEX IF NOT EXISTS idx_comments_post_id ON comments(post_id);
                CREATE INDEX IF NOT EXISTS idx_comments_user_id ON comments(user_id);
                CREATE INDEX IF NOT EXISTS idx_likes_user_post ON likes(user_id, post_id);
                CREATE INDEX IF NOT EXISTS idx_likes_user_comment ON likes(user_id, comment_id);
                CREATE INDEX IF NOT EXISTS idx_bookmarks_user_post ON bookmarks(user_id, post_id);
            `)

            console.log('✅ Database schema initialized successfully')
        }
    } catch (error) {
        console.error('❌ Database initialization error:', error)
        throw error
    }
}

// 앱 시작 시 DB 초기화
initializeDatabase()

// 연결 테스트 및 게시물 수 확인
testConnection()

// 연결 테스트 함수
export function testConnection() {
    try {
        const result = sqlite.prepare('SELECT COUNT(*) as count FROM posts').get() as {
            count: number
        }
        console.log(`✅ DB Connected: ${result.count} posts found`)
        return true
    } catch (error) {
        console.error('❌ DB Connection Error:', error)
        return false
    }
}
