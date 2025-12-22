/**
 * 이미지 최적화 유틸리티
 */

/**
 * 이미지 URL에 쿼리 파라미터 추가 (Cloudflare R2 Image Resizing)
 */
export function optimizeImageUrl(url: string, options: {
	width?: number
	height?: number
	quality?: number
	format?: 'auto' | 'webp' | 'avif' | 'jpeg' | 'png'
} = {}) {
	const {
		width,
		height,
		quality = 85,
		format = 'auto'
	} = options

	// Cloudflare R2 이미지 최적화 파라미터
	const params = new URLSearchParams()
	
	if (width) params.append('width', width.toString())
	if (height) params.append('height', height.toString())
	params.append('quality', quality.toString())
	params.append('format', format)

	return `${url}?${params.toString()}`
}

/**
 * 썸네일 URL 생성
 */
export function getThumbnailUrl(url: string, size: 'small' | 'medium' | 'large' = 'medium') {
	const sizes = {
		small: 200,
		medium: 400,
		large: 800
	}

	return optimizeImageUrl(url, {
		width: sizes[size],
		format: 'webp',
		quality: 80
	})
}

/**
 * srcset 생성 (반응형 이미지)
 */
export function generateSrcSet(url: string, widths: number[] = [400, 800, 1200, 1600]) {
	return widths
		.map(width => `${optimizeImageUrl(url, { width, format: 'webp' })} ${width}w`)
		.join(', ')
}

/**
 * Lazy loading 이미지 속성
 */
export const lazyLoadingAttrs = {
	loading: 'lazy' as const,
	decoding: 'async' as const
}

/**
 * 이미지 프리로드 링크 생성
 */
export function preloadImage(url: string, as: 'image' = 'image') {
	return {
		rel: 'preload',
		as,
		href: url,
		type: 'image/webp'
	}
}

/**
 * 블러 플레이스홀더 생성 (LQIP - Low Quality Image Placeholder)
 */
export function getBlurPlaceholder(url: string) {
	return optimizeImageUrl(url, {
		width: 20,
		quality: 10,
		format: 'webp'
	})
}
