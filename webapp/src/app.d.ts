import type { SupabaseClient, Session, User } from '@supabase/supabase-js'
import type { DB } from '$lib/server/db'

declare global {
	namespace App {
		interface Locals {
			supabase: SupabaseClient
			safeGetSession: () => Promise<{ session: Session | null; user: User | null }>
			db: DB
		}
		interface PageData {
			session: Session | null
			user: User | null
		}
		// interface Error {}
		interface Platform {
			env: {
				DB: D1Database
				R2: R2Bucket
			}
		}
	}
}

export { }
