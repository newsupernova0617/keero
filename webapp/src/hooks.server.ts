import { PUBLIC_SUPABASE_ANON_KEY, PUBLIC_SUPABASE_URL } from '$env/static/public'
import { createServerClient } from '@supabase/ssr'
import type { Handle } from '@sveltejs/kit'

export const handle: Handle = async ({ event, resolve }) => {
    /**
     * Creates a Supabase client specific to this server request.
     *
     * The Supabase client gets the Auth token from the request cookies.
     */
    event.locals.supabase = createServerClient(PUBLIC_SUPABASE_URL, PUBLIC_SUPABASE_ANON_KEY, {
        cookies: {
            getAll: () => event.cookies.getAll(),
            /**
             * SvelteKit's cookies API requires `path` to be explicitly set in
             * the cookie options. Setting `path` to `/` replicates previous/
             * standard behavior.
             */
            setAll: (cookiesToSet) => {
                cookiesToSet.forEach(({ name, value, options }) => {
                    event.cookies.set(name, value, { ...options, path: '/' })
                })
            }
        }
    })

    /**
     * Unlike `supabase.auth.getSession()`, which returns the session _without_
     * validating the JWT, this function also calls `getUser()` to validate the
     * JWT before returning the session.
     */
    event.locals.safeGetSession = async () => {
        const {
            data: { session }
        } = await event.locals.supabase.auth.getSession()
        
        if (!session) {
            return { session: null, user: null }
        }

        const {
            data: { user },
            error
        } = await event.locals.supabase.auth.getUser()
        
        if (error || !user) {
            return { session: null, user: null }
        }

        /**
         * IMPORTANT: Do NOT spread `...session` or access `session.user`.
         * Accessing `session.user` on the object returned by `getSession` triggers a security warning log.
         * We verify the user via `getUser()` above and knowingly construct a new safe session object.
         */
        const { access_token, refresh_token, expires_in, expires_at, token_type } = session
        const newSession = {
            access_token,
            refresh_token,
            expires_in,
            expires_at,
            token_type,
            user // The verified user from getUser()
        }

        return { session: newSession, user }
    }

    return resolve(event, {
        filterSerializedResponseHeaders(name) {
            /**
             * Supabase libraries use the `content-range` and `x-supabase-api-version`
             * headers, so we need to tell SvelteKit to pass it through.
             */
            return name === 'content-range' || name === 'x-supabase-api-version'
        }
    })
}
