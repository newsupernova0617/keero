import { db } from '$lib/server/db'
import { posts, comments, likes, highlights, users } from '$lib/server/schema'
import { desc, sql, eq, and, isNull } from 'drizzle-orm'
import type { PageServerLoad } from './$types'

// 날짜 유틸리티 함수
function getMonday(date: Date): string {
	const d = new Date(date)
	const day = d.getDay()
	const diff = d.getDate() - day + (day === 0 ? -6 : 1) // 일요일이면 -6, 아니면 +1
	d.setDate(diff)
	d.setHours(0, 0, 0, 0)
	return d.toISOString().split('T')[0]
}

function getSunday(date: Date): string {
	const monday = getMonday(date)
	const d = new Date(monday)
	d.setDate(d.getDate() + 6)
	d.setHours(23, 59, 59, 999)
	return d.toISOString().split('T')[0]
}

// 에디터 코멘트 기본 템플릿
const defaultComments: Record<number, string> = {
	1: '🏆 이번 주 가장 많은 사랑을 받은 게시글입니다!',
	2: '🔥 댓글 반응이 뜨거웠던 화제의 글!',
	3: '💎 조용히 인기를 끌고 있는 숨은 보석 같은 글',
	4: '😂 웃음이 터져나오는 재미있는 글',
	5: '👏 많은 공감을 얻은 글',
	6: '✨ 이번 주 놓치면 안 될 글',
	7: '🎯 화제성 만점 게시글',
	8: '💬 댓글로 더욱 재미있어진 글',
	9: '🌟 주목할 만한 게시글',
	10: '📌 꼭 읽어봐야 할 글'
}

export const load: PageServerLoad = async () => {
	// 이번 주 시작일/종료일 계산
	const now = new Date()
	const weekStart = getMonday(now)
	const weekEnd = getSunday(now)

	// 주간 TOP 10 게시글 조회 (좋아요 수 기준)
	const weeklyTop10 = await db
		.select({
			id: posts.id,
			title: posts.title,
			siteName: posts.site_name,
			sourceUrl: posts.source_url,
			createdAt: posts.created_at,
			crawledAt: posts.crawled_at,
			likeCount: sql<number>`(SELECT COUNT(*) FROM ${likes} WHERE ${likes.post_id} = ${posts.id})`.as(
				'like_count'
			),
			commentCount: sql<number>`(SELECT COUNT(*) FROM ${comments} WHERE ${comments.post_id} = ${posts.id} AND ${comments.is_deleted} = 0)`.as(
				'comment_count'
			)
		})
		.from(posts)
		.where(
			and(
				sql`${posts.crawled_at} >= ${weekStart}`,
				sql`${posts.crawled_at} <= ${weekEnd}`,
				isNull(posts.related_post_id)
			)
		)
		.orderBy(desc(sql`like_count`))
		.limit(10)

	// 각 게시글의 베스트 댓글 3개 조회
	const postsWithComments = await Promise.all(
		weeklyTop10.map(async (post, index) => {
			// 베스트 댓글 조회 (좋아요 많은 순)
			const bestComments = await db
				.select({
					id: comments.id,
					content: comments.content,
					createdAt: comments.created_at,
					userName: users.display_name,
					userEmail: users.email,
					likeCount: sql<number>`(SELECT COUNT(*) FROM ${likes} WHERE ${likes.comment_id} = ${comments.id})`.as(
						'like_count'
					)
				})
				.from(comments)
				.leftJoin(users, eq(comments.user_id, users.id))
				.where(and(eq(comments.post_id, post.id), eq(comments.is_deleted, false)))
				.orderBy(desc(sql`like_count`))
				.limit(3)

			// 에디터 코멘트 조회 (DB에서 먼저, 없으면 기본 템플릿)
			const savedHighlight = await db
				.select()
				.from(highlights)
				.where(
					and(
						eq(highlights.weekStart, weekStart),
						eq(highlights.postId, post.id)
					)
				)
				.limit(1)

			const editorComment =
				savedHighlight[0]?.editorComment || defaultComments[index + 1] || '주목할 만한 게시글입니다'

			return {
				...post,
				rank: index + 1,
				editorComment,
				bestComments: bestComments.map((c) => ({
					...c,
					displayName: c.userName || c.userEmail?.split('@')[0] || '익명'
				}))
			}
		})
	)

	// 주간 통계
	const weekStats = {
		totalPosts: weeklyTop10.length,
		totalLikes: weeklyTop10.reduce((sum, p) => sum + (p.likeCount || 0), 0),
		totalComments: weeklyTop10.reduce((sum, p) => sum + (p.commentCount || 0), 0),
		topSite:
			weeklyTop10.length > 0
				? weeklyTop10.reduce((acc, post) => {
						acc[post.siteName] = (acc[post.siteName] || 0) + 1
						return acc
				  }, {} as Record<string, number>)
				: {}
	}

	const topSiteName =
		Object.entries(weekStats.topSite).sort((a, b) => b[1] - a[1])[0]?.[0] || '없음'

	return {
		weekStart,
		weekEnd,
		posts: postsWithComments,
		stats: {
			...weekStats,
			topSiteName
		}
	}
}
