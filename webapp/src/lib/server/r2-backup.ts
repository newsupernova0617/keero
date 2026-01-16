/**
 * R2 백업 유틸리티
 * 데이터베이스 백업을 Cloudflare R2에 저장/관리
 */

import { S3Client, PutObjectCommand, ListObjectsV2Command, GetObjectCommand, DeleteObjectCommand } from '@aws-sdk/client-s3'
import { env } from '$env/dynamic/private'
import { readFileSync } from 'fs'

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

export interface BackupFile {
	key: string
	filename: string
	size: number
	lastModified: Date
	url: string
}

/**
 * 백업 파일을 R2에 업로드
 */
export async function uploadBackupToR2(localPath: string, filename: string): Promise<BackupFile> {
	try {
		const client = getS3Client()
		const bucketName = env.R2_BUCKET_NAME

		if (!bucketName) {
			throw new Error('R2_BUCKET_NAME not configured')
		}

		// 파일 읽기
		const fileBuffer = readFileSync(localPath)
		const r2Key = `backups/${filename}`

		// R2 업로드
		await client.send(
			new PutObjectCommand({
				Bucket: bucketName,
				Key: r2Key,
				Body: fileBuffer,
				ContentType: 'application/x-sqlite3',
				Metadata: {
					'upload-time': new Date().toISOString(),
					'original-name': filename
				}
			})
		)

		// 공개 URL 생성
		const publicUrl = env.R2_PUBLIC_URL || ''
		const url = publicUrl ? `${publicUrl}/${r2Key}` : ''

		return {
			key: r2Key,
			filename,
			size: fileBuffer.length,
			lastModified: new Date(),
			url
		}
	} catch (error) {
		console.error('R2 backup upload failed:', error)
		throw error
	}
}

/**
 * R2에서 백업 파일 목록 조회
 */
export async function listBackupsFromR2(): Promise<BackupFile[]> {
	try {
		const client = getS3Client()
		const bucketName = env.R2_BUCKET_NAME

		if (!bucketName) {
			throw new Error('R2_BUCKET_NAME not configured')
		}

		const response = await client.send(
			new ListObjectsV2Command({
				Bucket: bucketName,
				Prefix: 'backups/',
				MaxKeys: 100
			})
		)

		const publicUrl = env.R2_PUBLIC_URL || ''

		return (response.Contents || [])
			.filter((item) => item.Key && item.Key.endsWith('.db'))
			.map((item) => ({
				key: item.Key!,
				filename: item.Key!.replace('backups/', ''),
				size: item.Size || 0,
				lastModified: item.LastModified || new Date(),
				url: publicUrl ? `${publicUrl}/${item.Key}` : ''
			}))
			.sort((a, b) => b.lastModified.getTime() - a.lastModified.getTime())
	} catch (error) {
		console.error('R2 backup list failed:', error)
		return []
	}
}

/**
 * R2에서 백업 파일 다운로드
 */
export async function downloadBackupFromR2(filename: string): Promise<Buffer> {
	try {
		const client = getS3Client()
		const bucketName = env.R2_BUCKET_NAME

		if (!bucketName) {
			throw new Error('R2_BUCKET_NAME not configured')
		}

		const r2Key = `backups/${filename}`

		const response = await client.send(
			new GetObjectCommand({
				Bucket: bucketName,
				Key: r2Key
			})
		)

		if (!response.Body) {
			throw new Error('No data received from R2')
		}

		// Stream을 Buffer로 변환
		const chunks: Uint8Array[] = []
		for await (const chunk of response.Body as AsyncIterable<Uint8Array>) {
			chunks.push(chunk)
		}

		return Buffer.concat(chunks)
	} catch (error) {
		console.error('R2 backup download failed:', error)
		throw error
	}
}

/**
 * R2에서 백업 파일 삭제
 */
export async function deleteBackupFromR2(filename: string): Promise<void> {
	try {
		const client = getS3Client()
		const bucketName = env.R2_BUCKET_NAME

		if (!bucketName) {
			throw new Error('R2_BUCKET_NAME not configured')
		}

		const r2Key = `backups/${filename}`

		await client.send(
			new DeleteObjectCommand({
				Bucket: bucketName,
				Key: r2Key
			})
		)
	} catch (error) {
		console.error('R2 backup delete failed:', error)
		throw error
	}
}
