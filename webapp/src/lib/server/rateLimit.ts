/**
 * Simple in-memory rate limiter
 * For production, consider using Redis or a dedicated rate limiting service
 */

interface RateLimitEntry {
	count: number
	resetAt: number
}

const rateLimitStore = new Map<string, RateLimitEntry>()

// Cleanup old entries every 5 minutes
setInterval(() => {
	const now = Date.now()
	for (const [key, entry] of rateLimitStore.entries()) {
		if (entry.resetAt < now) {
			rateLimitStore.delete(key)
		}
	}
}, 5 * 60 * 1000)

export interface RateLimitConfig {
	/** Maximum number of requests allowed */
	maxRequests: number
	/** Time window in seconds */
	windowSeconds: number
	/** Unique identifier for the rate limit (e.g., user ID, IP) */
	identifier: string
	/** Optional: Action name for logging */
	action?: string
}

export interface RateLimitResult {
	allowed: boolean
	remaining: number
	resetAt: number
	retryAfter?: number
}

/**
 * Check if a request is allowed under rate limiting rules
 * @param config - Rate limit configuration
 * @returns Rate limit result
 */
export function checkRateLimit(config: RateLimitConfig): RateLimitResult {
	const { maxRequests, windowSeconds, identifier, action } = config
	const now = Date.now()
	const windowMs = windowSeconds * 1000
	const key = `${action || 'default'}:${identifier}`

	let entry = rateLimitStore.get(key)

	// Create new entry if doesn't exist or expired
	if (!entry || entry.resetAt < now) {
		entry = {
			count: 0,
			resetAt: now + windowMs
		}
		rateLimitStore.set(key, entry)
	}

	// Increment count
	entry.count++

	const allowed = entry.count <= maxRequests
	const remaining = Math.max(0, maxRequests - entry.count)
	const retryAfter = allowed ? undefined : Math.ceil((entry.resetAt - now) / 1000)

	// Log rate limit violations
	if (!allowed) {
		console.warn(`[RATE_LIMIT] Exceeded:`, {
			timestamp: new Date().toISOString(),
			action: action || 'default',
			identifier,
			count: entry.count,
			maxRequests,
			retryAfter
		})
	}

	return {
		allowed,
		remaining,
		resetAt: entry.resetAt,
		retryAfter
	}
}

/**
 * Reset rate limit for a specific identifier
 * Useful for testing or manual override
 */
export function resetRateLimit(identifier: string, action?: string): void {
	const key = `${action || 'default'}:${identifier}`
	rateLimitStore.delete(key)
}

/**
 * Get current rate limit status without incrementing
 */
export function getRateLimitStatus(identifier: string, action?: string): RateLimitResult | null {
	const key = `${action || 'default'}:${identifier}`
	const entry = rateLimitStore.get(key)
	
	if (!entry) {
		return null
	}

	const now = Date.now()
	if (entry.resetAt < now) {
		return null
	}

	return {
		allowed: true,
		remaining: 0,
		resetAt: entry.resetAt
	}
}
