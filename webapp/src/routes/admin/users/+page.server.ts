import { db } from '$lib/server/db'
import { users, type User } from '$lib/server/schema'
import type { PageServerLoad } from './$types'

export const load: PageServerLoad = async () => {
    let allUsers: User[] = []

    try {
        allUsers = await db.select().from(users).orderBy(users.id)
    } catch (error) {
        console.error('Users fetch error:', error)
    }

    return {
        users: allUsers
    }
}
