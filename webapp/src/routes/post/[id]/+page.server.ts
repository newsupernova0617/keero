import { db } from '$lib/server/db'
import { posts, images, comments, users } from '$lib/server/schema'
import { eq, isNull, sql, asc } from 'drizzle-orm'
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
    let postComments: any[] = []
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

    return {
        post: post[0],
        images: postImages,
        comments: postComments
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
    }
}

