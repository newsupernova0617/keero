import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { posts, images } from '$lib/server/schema';
import { env } from '$env/dynamic/private';
import { eq } from 'drizzle-orm';

/**
 * Crawler API - 게시글 저장 엔드포인트
 */
export const POST: RequestHandler = async ({ request, locals }) => {
    console.log('📥 Received POST request to /api/crawler/posts');
    const db = locals.db
	
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
		const { post: postData, images: imagesMetadata } = body;

		if (!postData || !postData.source_url) {
			return json({ error: 'Invalid request: missing post data' }, { status: 400 });
		}

		// 3. 중복 체크
		const existing = await db
			.select()
			.from(posts)
			.where(eq(posts.source_url, postData.source_url))
			.get();

		if (existing) {
			console.log(`⏩ Duplicate post skipped: ${postData.title}`);
			return json({ success: false, duplicate: true });
		}

		// 4. DB 저장 (Cloudflare D1 트랜잭션 수동 구현 - 트랜잭션 오류 회피)
		// 현재 Drizzle on D1의 transaction()이 일부 환경에서 begin 오류를 일으키는 경우가 있어 순차 실행으로 변경
		
		// 4-1. 게시글 저장
		const insertResult = await db.insert(posts).values({
			site_name: postData.site_name,
			title: postData.title,
			content: postData.content || '',
			content_html: postData.content_html || '',
			source_url: postData.source_url,
			created_at: postData.created_at || new Date().toISOString(),
			crawled_at: new Date().toISOString()
		}).returning({ id: posts.id });

		const postId = insertResult[0]?.id;

		// 4-2. 이미지 메타데이터 저장
		let imagesSaved = 0;
		if (imagesMetadata && imagesMetadata.length > 0 && postId) {
			for (const img of imagesMetadata) {
				await db.insert(images).values({
					post_id: postId,
					original_url: img.original_url || img.url,
					r2_url: img.url,
					r2_key: img.r2_key || '',
					order_index: img.order_index || 0
				}).run();
				imagesSaved++;
			}
		}

		console.log(`✅ Post saved: ${postData.title} (ID: ${postId}, Media: ${imagesSaved})`);

		return json({
			success: true,
			post_id: postId,
			images_saved: imagesSaved
		});

	} catch (error) {
		console.error('❌ API Error:', error);
		return json({ 
			error: 'Internal server error',
			message: error instanceof Error ? error.message : 'Unknown error'
		}, { status: 500 });
	}
};
