import { db } from '$lib/server/db'
import { posts, images, comments, users } from '$lib/server/schema'
import { eq, asc, sql } from 'drizzle-orm'
import { error, fail } from '@sveltejs/kit'
import type { PageServerLoad, Actions } from './$types'

export const load: PageServerLoad = async ({ params, locals }) => {
    const postId = parseInt(params.id)

    if (isNaN(postId)) {
        throw error(400, 'Invalid post ID')
    }

    // 게시글 조회
    const post = await db.select().from(posts).where(eq(posts.id, postId)).limit(1)

    if (!post || post.length === 0) {
        throw error(404, 'Post not found')
    }

    // 이미지 조회
    const postImages = await db
        .select()
        .from(images)
        .where(eq(images.post_id, postId))
        .orderBy(asc(images.order_index))

    // 댓글 조회 (사용자 정보 포함)
    let postComments: Array<{
        id: number
        post_id: number
        user_id: number
        parent_comment_id: number | null
        content: string
        created_at: string | null
        updated_at: string | null
        is_deleted: boolean | null
        user_email: string | null
        user_display_name: string | null
    }> = []
    try {
        postComments = await db
            .select({
                id: comments.id,
                post_id: comments.post_id,
                user_id: comments.user_id,
                parent_comment_id: comments.parent_comment_id,
                content: comments.content,
                created_at: comments.created_at,
                updated_at: comments.updated_at,
                is_deleted: comments.is_deleted,
                user_email: users.email,
                user_display_name: users.display_name
            })
            .from(comments)
            .leftJoin(users, eq(comments.user_id, users.id))
            .where(eq(comments.post_id, postId))
            .orderBy(comments.created_at)
    } catch (error) {
        console.log('Comments table not found, skipping comments:', error)
    }

    // 현재 사용자의 DB ID 조회
    const { user } = await locals.safeGetSession()
    let currentUserId: number | null = null
    if (user) {
        const dbUser = await db.select().from(users).where(eq(users.supabase_id, user.id)).limit(1)
        if (dbUser && dbUser.length > 0) {
            currentUserId = dbUser[0].id
        }
    }

    // 좋아요 정보 조회
    const { likes } = await import('$lib/server/schema')
    const likeCount = await db
        .select({ count: sql<number>`count(*)` })
        .from(likes)
        .where(eq(likes.post_id, postId))
        .then(result => result[0]?.count || 0)

    let userLiked = false
    if (currentUserId) {
        const userLike = await db
            .select()
            .from(likes)
            .where(sql`${likes.post_id} = ${postId} AND ${likes.user_id} = ${currentUserId}`)
            .limit(1)
        userLiked = userLike.length > 0
    }

    return {
        post: post[0],
        images: postImages,
        comments: postComments,
        currentUserId,
        likeCount,
        userLiked
    }
}

export const actions: Actions = {
    // 댓글 작성
    comment: async ({ request, params, locals }) => {
        const { session, user } = await locals.safeGetSession()

        if (!session || !user) {
            return fail(401, { error: '로그인이 필요합니다.' })
        }

        const formData = await request.formData()
        const content = formData.get('content')?.toString()
        const parentCommentId = formData.get('parent_comment_id')?.toString()

        if (!content || content.trim().length === 0) {
            return fail(400, { error: '댓글 내용을 입력해주세요.' })
        }

        if (content.length > 1000) {
            return fail(400, { error: '댓글은 1000자를 초과할 수 없습니다.' })
        }

        const postId = parseInt(params.id)

        // 사용자 DB에서 조회 또는 생성
        let dbUser = await db.select().from(users).where(eq(users.supabase_id, user.id)).limit(1)

        if (!dbUser || dbUser.length === 0) {
            // 신규 사용자 생성
            const newUser = await db
                .insert(users)
                .values({
                    supabase_id: user.id,
                    email: user.email || '',
                    display_name: user.user_metadata?.name || user.email?.split('@')[0] || 'Anonymous',
                    avatar_url: user.user_metadata?.avatar_url
                })
                .returning()

            dbUser = newUser
        }

        // 댓글 저장
        await db.insert(comments).values({
            post_id: postId,
            user_id: dbUser[0].id,
            parent_comment_id: parentCommentId ? parseInt(parentCommentId) : null,
            content: content.trim()
        })

        return { success: true }
    },

    // 댓글 수정
    editComment: async ({ request, locals }) => {
        const { session, user } = await locals.safeGetSession()

        if (!session || !user) {
            return fail(401, { error: '로그인이 필요합니다.' })
        }

        const formData = await request.formData()
        const commentId = formData.get('comment_id')?.toString()
        const content = formData.get('content')?.toString()

        if (!commentId || !content || content.trim().length === 0) {
            return fail(400, { error: '잘못된 요청입니다.' })
        }

        if (content.length > 1000) {
            return fail(400, { error: '댓글은 1000자를 초과할 수 없습니다.' })
        }

        // 댓글 소유자 확인
        const comment = await db
            .select({ user_id: comments.user_id })
            .from(comments)
            .where(eq(comments.id, parseInt(commentId)))
            .limit(1)

        if (!comment || comment.length === 0) {
            return fail(404, { error: '댓글을 찾을 수 없습니다.' })
        }

        const dbUser = await db.select().from(users).where(eq(users.supabase_id, user.id)).limit(1)

        if (!dbUser || dbUser.length === 0 || comment[0].user_id !== dbUser[0].id) {
            return fail(403, { error: '댓글을 수정할 권한이 없습니다.' })
        }

        // 댓글 수정
        await db
            .update(comments)
            .set({
                content: content.trim(),
                updated_at: new Date().toISOString()
            })
            .where(eq(comments.id, parseInt(commentId)))

        return { success: true }
    },

    // 댓글 삭제
    deleteComment: async ({ request, locals }) => {
        const { session, user } = await locals.safeGetSession()

        if (!session || !user) {
            return fail(401, { error: '로그인이 필요합니다.' })
        }

        const formData = await request.formData()
        const commentId = formData.get('comment_id')?.toString()

        if (!commentId) {
            return fail(400, { error: '잘못된 요청입니다.' })
        }

        // 댓글 소유자 확인
        const comment = await db
            .select({ user_id: comments.user_id })
            .from(comments)
            .where(eq(comments.id, parseInt(commentId)))
            .limit(1)

        if (!comment || comment.length === 0) {
            return fail(404, { error: '댓글을 찾을 수 없습니다.' })
        }

        const dbUser = await db.select().from(users).where(eq(users.supabase_id, user.id)).limit(1)

        if (!dbUser || dbUser.length === 0 || comment[0].user_id !== dbUser[0].id) {
            return fail(403, { error: '댓글을 삭제할 권한이 없습니다.' })
        }

        // Soft delete
        await db
            .update(comments)
            .set({
                is_deleted: true,
                content: '삭제된 댓글입니다.'
            })
            .where(eq(comments.id, parseInt(commentId)))

        return { success: true }
    },

    // 좋아요 토글
    toggleLike: async ({ params, locals }) => {
        const { session, user } = await locals.safeGetSession()

        if (!session || !user) {
            return fail(401, { error: '로그인이 필요합니다.' })
        }

        const postId = parseInt(params.id)

        // 사용자 DB에서 조회 또는 생성
        let dbUser = await db.select().from(users).where(eq(users.supabase_id, user.id)).limit(1)

        if (!dbUser || dbUser.length === 0) {
            // 신규 사용자 생성
            const newUser = await db
                .insert(users)
                .values({
                    supabase_id: user.id,
                    email: user.email || '',
                    display_name: user.user_metadata?.name || user.email?.split('@')[0] || 'Anonymous',
                    avatar_url: user.user_metadata?.avatar_url
                })
                .returning()

            dbUser = newUser
        }

        const { likes } = await import('$lib/server/schema')

        // 이미 좋아요 했는지 확인
        const existingLike = await db
            .select()
            .from(likes)
            .where(sql`${likes.post_id} = ${postId} AND ${likes.user_id} = ${dbUser[0].id}`)
            .limit(1)

        if (existingLike.length > 0) {
            // 좋아요 취소
            await db
                .delete(likes)
                .where(sql`${likes.post_id} = ${postId} AND ${likes.user_id} = ${dbUser[0].id}`)
        } else {
            // 좋아요 추가
            await db.insert(likes).values({
                post_id: postId,
                user_id: dbUser[0].id
            })
        }

        return { success: true }
    }
}

