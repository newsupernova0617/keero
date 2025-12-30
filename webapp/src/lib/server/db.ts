import Database from 'better-sqlite3'
import { drizzle } from 'drizzle-orm/better-sqlite3'
import * as schema from './schema'
import { mkdirSync, existsSync } from 'fs'
import { dirname } from 'path'

// DB 경로 (환경 변수로 설정 가능, 기본값: /app/data/posts.db)
const DB_PATH = process.env.DATABASE_PATH || './data/posts.db'

// DB 디렉토리 자동 생성
const dbDir = dirname(DB_PATH)
if (!existsSync(dbDir)) {
    mkdirSync(dbDir, { recursive: true })
}

// SQLite 연결
const sqlite = new Database(DB_PATH)

// PRAGMA 설정 (성능 최적화)
sqlite.pragma('journal_mode = WAL') // Write-Ahead Logging (동시 읽기/쓰기)
sqlite.pragma('synchronous = NORMAL') // 성능과 안정성 균형
sqlite.pragma('cache_size = -64000') // 64MB 캐시
sqlite.pragma('temp_store = MEMORY') // 임시 테이블 메모리 사용
sqlite.pragma('mmap_size = 268435456') // 256MB 메모리 매핑
sqlite.pragma('busy_timeout = 5000') // 잠금 대기 5초

// Drizzle ORM 초기화
export const db = drizzle(sqlite, { schema })

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
