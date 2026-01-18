/**
 * SEO 메타 태그 생성 유틸리티
 */

export interface SEOConfig {
	title: string
	description: string
	keywords?: string[]
	image?: string
	url?: string
	type?: 'website' | 'article'
	publishedTime?: string
	author?: string
}

export function generateSEOTags(config: SEOConfig) {
	const {
		title,
		description,
		keywords = [],
		image,
		url,
		type = 'website',
		publishedTime,
		author
	} = config

	const siteName = '유머 게시판'
	const fullTitle = `${title} - ${siteName}`

	return {
		title: fullTitle,
		meta: [
			{ name: 'description', content: description },
			{ name: 'keywords', content: keywords.join(', ') },
			
			// Open Graph
			{ property: 'og:title', content: fullTitle },
			{ property: 'og:description', content: description },
			{ property: 'og:type', content: type },
			{ property: 'og:site_name', content: siteName },
			...(url ? [{ property: 'og:url', content: url }] : []),
			...(image ? [{ property: 'og:image', content: image }] : []),
			...(publishedTime && type === 'article' ? [{ property: 'article:published_time', content: publishedTime }] : []),
			...(author && type === 'article' ? [{ property: 'article:author', content: author }] : []),
			
			// Twitter Card
			{ name: 'twitter:card', content: image ? 'summary_large_image' : 'summary' },
			{ name: 'twitter:title', content: fullTitle },
			{ name: 'twitter:description', content: description },
			...(image ? [{ name: 'twitter:image', content: image }] : []),
		]
	}
}

/**
 * 구조화된 데이터 (JSON-LD) 생성
 */
export function generateArticleSchema(config: {
	title: string
	description: string
	image?: string
	url: string
	publishedTime: string
	author?: string
}) {
	return {
		'@context': 'https://schema.org',
		'@type': 'Article',
		headline: config.title,
		description: config.description,
		image: config.image,
		url: config.url,
		datePublished: config.publishedTime,
		author: config.author ? {
			'@type': 'Person',
			name: config.author
		} : undefined
	}
}

/**
 * 사이트맵 URL 생성
 */
export function generateSitemapEntry(config: {
	url: string
	lastmod?: string
	changefreq?: 'always' | 'hourly' | 'daily' | 'weekly' | 'monthly' | 'yearly' | 'never'
	priority?: number
}) {
	return {
		url: config.url,
		lastmod: config.lastmod || new Date().toISOString(),
		changefreq: config.changefreq || 'daily',
		priority: config.priority || 0.5
	}
}

/**
 * 기본 URL 관리
 */
import { env } from '$env/dynamic/public'

export function getBaseUrl(): string {
    let baseUrl = env.PUBLIC_BASE_URL || 'https://keerosveltekit-production.up.railway.app'
    // https:// 프로토콜이 없으면 자동 추가
    if (baseUrl && !baseUrl.startsWith('http://') && !baseUrl.startsWith('https://')) {
        baseUrl = `https://${baseUrl}`
    }
    return baseUrl
}

export function getFullUrl(path: string): string {
    const baseUrl = getBaseUrl()
    const cleanPath = path.startsWith('/') ? path : `/${path}`
    return `${baseUrl}${cleanPath}`
}

export function getDefaultOgImage(): string {
    return getFullUrl('/og-default.png')
}

export const SITE_NAME = 'KEERO 유머 게시판'
export const SITE_DESCRIPTION = 'FMKorea, 루리웹, 오늘의유머 등에서 엄선한 재미있는 유머와 웃긴 글을 한곳에서 만나보세요. 매일 업데이트되는 최신 유머 게시글.'

