import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { db } from '$lib/server/db';
import { posts, images } from '$lib/server/schema';
import { env } from '$env/dynamic/private';

/**
 * Crawler API - 게시글 저장 엔드포인트
 * 
 * POST /api/crawler/posts
 * 
 * Request Body:
 * {
 *   "post": {
 *     "site_name": "fmkorea",
 *     "title": "제목",
 *     "content": "본문",
 *     "content_html": "<div>...</div>",
 *     "source_url": "https://...",
 *     "created_at": "2025-12-27T..."
 *   },
 *   "images": [
 *     { "url": "https://image1.jpg", "order_index": 0 }
 *   ]
 * }
 */

export const POST: RequestHandler = async ({ request }) => {
	try {
		// 1. API Key 검증
		const apiKey = request.headers.get('X-API-Key');
		const expectedKey = env.CRAWLER_API_KEY;

		if (!expectedKey) {
			console.error('❌ CRAWLER_API_KEY not configured');
			return json({ error: 'Server configuration error' }, { status: 500 });
		}

		if (!apiKey || apiKey !== expectedKey) {
			console.warn('⚠️ Unauthorized API request');
			return json({ error: 'Unauthorized' }, { status: 401 });
		}

		// 2. 요청 데이터 파싱
		const body = await request.json();
		const { post: postData, images: imageUrls } = body;

		if (!postData || !postData.source_url) {
			return json({ error: 'Invalid request: missing post data' }, { status: 400 });
		}

		// 3. 트랜잭션으로 게시글 + 이미지 저장
		const result = await savePostWithImages(postData, imageUrls || []);

		if (!result.success) {
			if (result.duplicate) {
				return json({ 
					success: false, 
					duplicate: true,
					message: 'Post already exists' 
				}, { status: 200 });
			}
			return json({ error: result.error }, { status: 500 });
		}

		console.log(`✅ Post saved: ${postData.title} (ID: ${result.postId}, Images: ${result.imagesSaved})`);

		return json({
			success: true,
			post_id: result.postId,
			images_saved: result.imagesSaved
		});

	} catch (error) {
		console.error('❌ API Error:', error);
		return json({ 
			error: 'Internal server error',
			message: error instanceof Error ? error.message : 'Unknown error'
		}, { status: 500 });
	}
};

/**
 * 게시글 + 이미지 저장 (트랜잭션)
 */
async function savePostWithImages(
	postData: {
		site_name: string;
		title: string;
		content: string;
		content_html?: string;
		source_url: string;
		created_at?: string;
	},
	imageUrls: Array<{ url: string; order_index: number }>
): Promise<{
	success: boolean;
	duplicate?: boolean;
	postId?: number;
	imagesSaved?: number;
	error?: string;
}> {
	try {
		// 1. 이미지를 R2에 업로드 (트랜잭션 전에 수행)
		const uploadedImages: Array<{ originalUrl: string; r2Url: string; r2Key: string; orderIndex: number }> = [];
		
		if (imageUrls && imageUrls.length > 0) {
			console.log(`📤 Uploading ${imageUrls.length} images to R2...`);
			
			for (const img of imageUrls) {
				try {
					const { r2Url, r2Key } = await uploadImageToR2(img.url);
					uploadedImages.push({
						originalUrl: img.url,
						r2Url,
						r2Key,
						orderIndex: img.order_index
					});
					console.log(`  ✅ Uploaded: ${img.url.substring(0, 50)}...`);
				} catch (error) {
					console.error(`  ❌ Failed to upload ${img.url}:`, error);
					// 업로드 실패해도 계속 진행 (일부 이미지만 실패할 수 있음)
				}
			}
		}

		// 2. Drizzle 트랜잭션으로 DB 저장
		const result = db.transaction((tx) => {
			// 중복 체크
			const existing = tx
				.select()
				.from(posts)
				.where(eq(posts.source_url, postData.source_url))
				.get();

			if (existing) {
				return { duplicate: true };
			}

			// 게시글 저장
			const insertResult = tx.insert(posts).values({
				site_name: postData.site_name,
				title: postData.title,
				content: postData.content || '',
				content_html: postData.content_html || '',
				source_url: postData.source_url,
				created_at: postData.created_at || new Date().toISOString(),
				crawled_at: new Date().toISOString()
			}).run();

			const postId = Number(insertResult.lastInsertRowid);

			// 이미지 저장 (R2 URL 사용)
			let imagesSaved = 0;
			if (uploadedImages.length > 0) {
				for (const img of uploadedImages) {
					tx.insert(images).values({
						post_id: postId,
						original_url: img.originalUrl,
						r2_url: img.r2Url,  // ← R2 URL 저장
						r2_key: img.r2Key,
						order_index: img.orderIndex
					}).run();
					imagesSaved++;
				}
			}

			return { postId, imagesSaved };
		});

		if ('duplicate' in result) {
			return { success: false, duplicate: true };
		}

		return {
			success: true,
			postId: result.postId,
			imagesSaved: result.imagesSaved
		};

	} catch (error) {
		console.error('❌ Database error:', error);
		return {
			success: false,
			error: error instanceof Error ? error.message : 'Unknown database error'
		};
	}
}

// eq 함수 및 R2 유틸리티 import
import { eq } from 'drizzle-orm';
import { uploadImageToR2 } from '$lib/server/r2';
