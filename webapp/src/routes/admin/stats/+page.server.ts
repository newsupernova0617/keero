import { requireAdmin } from '$lib/server/auth'
import { db } from '$lib/server/db'
import { posts, comments, users, likes, bookmarks } from '$lib/server/schema'
import { sql, desc, count } from 'drizzle-orm'
import type { PageServerLoad } from './$types'

export const load: PageServerLoad = async (event) => {
	await requireAdmin(event)

	// 사이트별 게시글 통계
	const postsBySite = await db
		.select({
			site_name: posts.site_name,
			count: count()
		})
		.from(posts)
		.groupBy(posts.site_name)
		.orderBy(desc(count()))

	// 최근 7일 게시글 수
	const recentPosts = await db
		.select({
			date: sql<string>`DATE(${posts.crawled_at})`,
			count: count()
		})
		.from(posts)
		.where(sql`DATE(${posts.crawled_at}) >= DATE('now', '-7 days')`)
		.groupBy(sql`DATE(${posts.crawled_at})`)
		.orderBy(sql`DATE(${posts.crawled_at})`)

	// 최근 7일 댓글 수
	const recentComments = await db
		.select({
			date: sql<string>`DATE(${comments.created_at})`,
			count: count()
		})
		.from(comments)
		.where(sql`DATE(${comments.created_at}) >= DATE('now', '-7 days')`)
		.groupBy(sql`DATE(${comments.created_at})`)
		.orderBy(sql`DATE(${comments.created_at})`)

	// 가장 활동적인 사용자 (댓글 수 기준)
	const mostActiveUsers = await db
		.select({
			user_id: users.id,
			email: users.email,
			display_name: users.display_name,
			comment_count: count()
		})
		.from(comments)
		.leftJoin(users, sql`${comments.user_id} = ${users.id}`)
		.groupBy(users.id, users.email, users.display_name)
		.orderBy(desc(count()))
		.limit(10)

	// 가장 인기있는 게시글 (좋아요 기준)
	const topPostsByLikes = await db
		.select({
			post_id: posts.id,
			title: posts.title,
			site_name: posts.site_name,
			like_count: count()
		})
		.from(likes)
		.leftJoin(posts, sql`${likes.post_id} = ${posts.id}`)
		.where(sql`${likes.post_id} IS NOT NULL`)
		.groupBy(posts.id, posts.title, posts.site_name)
		.orderBy(desc(count()))
		.limit(10)

	// 가장 많은 댓글이 달린 게시글
	const topPostsByComments = await db
		.select({
			post_id: posts.id,
			title: posts.title,
			site_name: posts.site_name,
			comment_count: count()
		})
		.from(comments)
		.leftJoin(posts, sql`${comments.post_id} = ${posts.id}`)
		.groupBy(posts.id, posts.title, posts.site_name)
		.orderBy(desc(count()))
		.limit(10)

	// 전체 통계
	const totalStats = {
		totalPosts: await db.select({ count: sql<number>`count(*)` }).from(posts).then(r => r[0]?.count || 0),
		totalComments: await db.select({ count: sql<number>`count(*)` }).from(comments).then(r => r[0]?.count || 0),
		totalUsers: await db.select({ count: sql<number>`count(*)` }).from(users).then(r => r[0]?.count || 0),
		totalLikes: await db.select({ count: sql<number>`count(*)` }).from(likes).then(r => r[0]?.count || 0),
		totalBookmarks: await db.select({ count: sql<number>`count(*)` }).from(bookmarks).then(r => r[0]?.count || 0)
	}

	return {
		postsBySite,
		recentPosts,
		recentComments,
		mostActiveUsers,
		topPostsByLikes,
		topPostsByComments,
		totalStats
	}
}
