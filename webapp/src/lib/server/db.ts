import { drizzle } from 'drizzle-orm/d1'
import * as schema from './schema'

// Cloudflare D1 타입 정의
// @cloudflare/workers-types 패키지에서 제공
declare global {
    interface Env {
        DB: D1Database
        R2: R2Bucket
    }
}

// Cloudflare D1 데이터베이스
// platform.env.DB는 wrangler.toml의 [[d1_databases]] 바인딩에서 제공됨
export function getDB(env: Env) {
    return drizzle(env.DB, { schema })
}

// 타입 정의
export type DB = ReturnType<typeof getDB>

// Re-export schema for convenience
export * from './schema'
