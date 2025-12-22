import { sqliteTable, text, integer, real, type SQLiteTableWithColumns } from 'drizzle-orm/sqlite-core'
import { sql } from 'drizzle-orm'

export const posts: SQLiteTableWithColumns<any> = sqliteTable('posts', {
    id: integer('id').primaryKey({ autoIncrement: true }),
    site_name: text('site_name', { length: 50 }).notNull(),
    title: text('title').notNull(),
    content: text('content'),
    content_html: text('content_html'), // HTML with preserved structure
    content_hash: text('content_hash', { length: 64 }),
    source_url: text('source_url').notNull().unique(),
    created_at: text('created_at'), // ISO 8601 datetime string
    crawled_at: text('crawled_at').default(sql`CURRENT_TIMESTAMP`),
    related_post_id: integer('related_post_id').references((): any => posts.id)
})

export const images = sqliteTable('images', {
    id: integer('id').primaryKey({ autoIncrement: true }),
    post_id: integer('post_id')
        .notNull()
        .references(() => posts.id),
    media_type: text('media_type', { length: 10 }).default('image'),
    md5_hash: text('md5_hash', { length: 32 }),
    perceptual_hash: text('perceptual_hash', { length: 16 }),
    r2_key: text('r2_key').notNull(),
    r2_url: text('r2_url').notNull(),
    order_index: integer('order_index').default(0),
    uploaded_at: text('uploaded_at').default(sql`CURRENT_TIMESTAMP`),
    is_similar_match: integer('is_similar_match', { mode: 'boolean' }).default(false),
    duration_seconds: integer('duration_seconds'),
    frame_count: integer('frame_count'),
    original_size_bytes: integer('original_size_bytes'),
    optimized_size_bytes: integer('optimized_size_bytes'),
    original_format: text('original_format', { length: 10 }),
    optimized_format: text('optimized_format', { length: 10 })
})

export const users = sqliteTable('users', {
    id: integer('id').primaryKey({ autoIncrement: true }),
    supabase_id: text('supabase_id').notNull().unique(),
    email: text('email').notNull(),
    display_name: text('display_name'),
    avatar_url: text('avatar_url'),
    role: integer('role').default(1), // 0: guest, 1: user, 99: admin
    created_at: text('created_at').default(sql`CURRENT_TIMESTAMP`),
    last_login_at: text('last_login_at')
})

export const comments: SQLiteTableWithColumns<any> = sqliteTable('comments', {
    id: integer('id').primaryKey({ autoIncrement: true }),
    post_id: integer('post_id')
        .notNull()
        .references(() => posts.id),
    user_id: integer('user_id')
        .notNull()
        .references(() => users.id),
    parent_comment_id: integer('parent_comment_id').references(() => comments.id),
    content: text('content').notNull(),
    created_at: text('created_at').default(sql`CURRENT_TIMESTAMP`),
    updated_at: text('updated_at'),
    is_deleted: integer('is_deleted', { mode: 'boolean' }).default(false)
})

export const likes = sqliteTable('likes', {
    id: integer('id').primaryKey({ autoIncrement: true }),
    user_id: integer('user_id')
        .notNull()
        .references(() => users.id),
    post_id: integer('post_id').references(() => posts.id),
    comment_id: integer('comment_id').references(() => comments.id),
    created_at: text('created_at').default(sql`CURRENT_TIMESTAMP`)
})

export type Post = typeof posts.$inferSelect
export type NewPost = typeof posts.$inferInsert
export type Image = typeof images.$inferSelect
export type User = typeof users.$inferSelect
export type Comment = typeof comments.$inferSelect
