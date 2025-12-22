import { sqliteTable, text, integer } from 'drizzle-orm/sqlite-core'
import { sql } from 'drizzle-orm'

export const posts = sqliteTable('posts', {
    id: integer('id').primaryKey({ autoIncrement: true }),
    site_name: text('site_name').notNull(),
    title: text('title').notNull(),
    content: text('content'),
    content_html: text('content_html'),
    source_url: text('source_url').notNull().unique(),
    created_at: text('created_at').notNull(),
    crawled_at: text('crawled_at').default(sql`CURRENT_TIMESTAMP`),
    related_post_id: integer('related_post_id')
})

export const images = sqliteTable('images', {
    id: integer('id').primaryKey({ autoIncrement: true }),
    post_id: integer('post_id')
        .notNull()
        .references(() => posts.id),
    r2_url: text('r2_url').notNull(),
    original_url: text('original_url'),
    media_type: text('media_type'),
    width: integer('width'),
    height: integer('height'),
    file_size: integer('file_size'),
    duration_seconds: integer('duration_seconds'),
    order_index: integer('order_index').notNull().default(0)
})

export const users = sqliteTable('users', {
    id: integer('id').primaryKey({ autoIncrement: true }),
    supabase_id: text('supabase_id').notNull().unique(),
    email: text('email').notNull(),
    display_name: text('display_name'),
    avatar_url: text('avatar_url'),
    role: integer('role').default(1), // 0: guest, 1: user, 99: admin
    created_at: text('created_at').default(sql`CURRENT_TIMESTAMP`)
})

export const comments = sqliteTable('comments', {
    id: integer('id').primaryKey({ autoIncrement: true }),
    post_id: integer('post_id')
        .notNull()
        .references(() => posts.id),
    user_id: integer('user_id')
        .notNull()
        .references(() => users.id),
    parent_comment_id: integer('parent_comment_id'),
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

export const bookmarks = sqliteTable('bookmarks', {
    id: integer('id').primaryKey({ autoIncrement: true }),
    user_id: integer('user_id')
        .notNull()
        .references(() => users.id),
    post_id: integer('post_id')
        .notNull()
        .references(() => posts.id),
    created_at: text('created_at').default(sql`CURRENT_TIMESTAMP`)
})

export const reports = sqliteTable('reports', {
    id: integer('id').primaryKey({ autoIncrement: true }),
    user_id: integer('user_id')
        .notNull()
        .references(() => users.id),
    post_id: integer('post_id').references(() => posts.id),
    comment_id: integer('comment_id').references(() => comments.id),
    reason: text('reason').notNull(), // 'spam', 'inappropriate', 'harassment', 'other'
    description: text('description'),
    status: text('status').default('pending'), // 'pending', 'reviewed', 'resolved', 'rejected'
    created_at: text('created_at').default(sql`CURRENT_TIMESTAMP`),
    resolved_at: text('resolved_at'),
    resolved_by: integer('resolved_by').references(() => users.id)
})

export type Post = typeof posts.$inferSelect
export type NewPost = typeof posts.$inferInsert
export type Image = typeof images.$inferSelect
export type User = typeof users.$inferSelect
export type Comment = typeof comments.$inferSelect
export type Bookmark = typeof bookmarks.$inferSelect
export type Report = typeof reports.$inferSelect
