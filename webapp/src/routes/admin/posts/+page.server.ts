import { db } from '$lib/server/db'
import { posts } from '$lib/server/schema'
import { eq } from 'drizzle-orm'
import { fail } from '@sveltejs/kit'
import type { PageServerLoad, Actions } from './$types'

export const load: PageServerLoad = async () => {
    const allPosts = await db
        .select()
        .from(posts)
        .orderBy(posts.id)
        .limit(100)

    return {
        posts: allPosts
    }
}

export const actions: Actions = {
    delete: async ({ request }) => {
        const formData = await request.formData()
        const postId = parseInt(formData.get('post_id')?.toString() || '0')

        if (!postId) {
            return fail(400, { error: 'Invalid post ID' })
        }

        try {
            await db.delete(posts).where(eq(posts.id, postId))
            return { success: true }
        } catch (error) {
            return fail(500, { error: 'Failed to delete post' })
        }
    }
}
