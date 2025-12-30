/**
 * R2 이미지 업로드 유틸리티
 */

import { S3Client, PutObjectCommand } from '@aws-sdk/client-s3'
import { env } from '$env/dynamic/private'
import crypto from 'crypto'

let s3Client: S3Client | null = null

function getS3Client(): S3Client {
	if (!s3Client) {
		const accountId = env.R2_ACCOUNT_ID
		const accessKeyId = env.R2_ACCESS_KEY_ID
		const secretAccessKey = env.R2_SECRET_ACCESS_KEY

		if (!accountId || !accessKeyId || !secretAccessKey) {
			throw new Error('R2 credentials not configured')
		}

		s3Client = new S3Client({
			region: 'auto',
			endpoint: `https://${accountId}.r2.cloudflarestorage.com`,
			credentials: {
				accessKeyId,
				secretAccessKey
			}
		})
	}

	return s3Client
}

/**
 * 이미지를 R2에 업로드
 * 
 * @param imageUrl 원본 이미지 URL
 * @returns { r2Url, r2Key } R2 URL과 키
 */
export async function uploadImageToR2(imageUrl: string): Promise<{
	r2Url: string
	r2Key: string
}> {
	try {
		// 1. 이미지 다운로드
		const response = await fetch(imageUrl)
		if (!response.ok) {
			throw new Error(`Failed to fetch image: ${response.status}`)
		}

		const buffer = await response.arrayBuffer()
		const contentType = response.headers.get('content-type') || 'image/jpeg'

		// 2. 파일 확장자 결정
		let ext = 'jpg'
		if (contentType.includes('png')) ext = 'png'
		else if (contentType.includes('gif')) ext = 'gif'
		else if (contentType.includes('webp')) ext = 'webp'
		else if (contentType.includes('mp4')) ext = 'mp4'
		else if (contentType.includes('webm')) ext = 'webm'

		// 3. R2 키 생성 (해시 기반)
		const hash = crypto.createHash('sha256').update(Buffer.from(buffer)).digest('hex')
		const r2Key = `images/${hash.substring(0, 2)}/${hash.substring(2, 4)}/${hash}.${ext}`

		// 4. R2 업로드
		const client = getS3Client()
		const bucketName = env.R2_BUCKET_NAME

		if (!bucketName) {
			throw new Error('R2_BUCKET_NAME not configured')
		}

		await client.send(
			new PutObjectCommand({
				Bucket: bucketName,
				Key: r2Key,
				Body: Buffer.from(buffer),
				ContentType: contentType
			})
		)

		// 5. R2 공개 URL 생성
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

/**
 * 여러 이미지를 병렬로 R2에 업로드
 */
export async function uploadImagesToR2(
	imageUrls: string[]
): Promise<Array<{ originalUrl: string; r2Url: string; r2Key: string }>> {
	const results = await Promise.allSettled(
		imageUrls.map(async (url) => {
			const { r2Url, r2Key } = await uploadImageToR2(url)
			return { originalUrl: url, r2Url, r2Key }
		})
	)

	return results
		.filter((r) => r.status === 'fulfilled')
		.map((r) => (r as PromiseFulfilledResult<{ originalUrl: string; r2Url: string; r2Key: string }>).value)
}
