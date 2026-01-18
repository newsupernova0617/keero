/**
 * R2 이미지 업로드 유틸리티 (Cloudflare Native)
 */
import { env } from '$env/dynamic/private'

/**
 * 이미지를 R2에 업로드
 * 
 * @param bucket R2Bucket 인스턴스 (platform.env.R2)
 * @param imageUrl 원본 이미지 URL
 * @returns { r2Url, r2Key } R2 URL과 키
 */
export async function uploadImageToR2(bucket: R2Bucket, imageUrl: string): Promise<{
	r2Url: string
	r2Key: string
}> {
	try {
		// 1. 이미지 다운로드
		const response = await fetch(imageUrl, {
			headers: {
				'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
			}
		})
		
		if (!response.ok) {
			throw new Error(`Failed to fetch image: ${response.status}`)
		}

		const buffer = await response.arrayBuffer()
		const contentType = response.headers.get('content-type') || 'image/jpeg'

		// 2. 파일 확장자 및 해시 생성 (Web Crypto 사용)
		let ext = 'jpg'
		if (contentType.includes('png')) ext = 'png'
		else if (contentType.includes('gif')) ext = 'gif'
		else if (contentType.includes('webp')) ext = 'webp'
		else if (contentType.includes('mp4')) ext = 'mp4'
		else if (contentType.includes('webm')) ext = 'webm'

		const hashBuffer = await crypto.subtle.digest('SHA-256', buffer)
		const hashArray = Array.from(new Uint8Array(hashBuffer))
		const hash = hashArray.map(b => b.toString(16).padStart(2, '0')).join('')
		
		const r2Key = `images/${hash.substring(0, 2)}/${hash.substring(2, 4)}/${hash}.${ext}`

		// 3. R2 업로드 (권장: Native R2Bucket API 사용)
		await bucket.put(r2Key, buffer, {
			httpMetadata: { contentType: contentType }
		})

		// 4. R2 공개 URL 생성
		const publicUrl = env.R2_PUBLIC_URL
		if (!publicUrl) {
			throw new Error('R2_PUBLIC_URL not configured')
		}

		const r2Url = `${publicUrl}/${r2Key}`

		return { r2Url, r2Key }
	} catch (error) {
		console.error(`❌ R2 upload failed for ${imageUrl}:`, error)
		throw error
	}
}
