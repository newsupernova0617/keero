<script lang="ts">
	import type { PageData } from './$types'
	import { enhance } from '$app/forms'
	import DOMPurify from 'isomorphic-dompurify'
	import AdSense from '$lib/components/ads/AdSense.svelte'
	import AdPost from '$lib/components/ads/AdPost.svelte'
	import { AD_CONFIG } from '$lib/config/ads'

	let { data }: { data: PageData } = $props()
	let { post, images, comments, session } = $derived(data)
	
	// HTML sanitize
	let sanitizedHtml = $derived(
		post.content_html 
			? DOMPurify.sanitize(post.content_html, {
				ALLOWED_TAGS: ['p', 'br', 'b', 'strong', 'i', 'em', 'u', 's', 'a', 'img', 'div', 'span', 'blockquote', 'ul', 'ol', 'li'],
				ALLOWED_ATTR: ['href', 'src', 'alt', 'title']
			})
			: ''
	)

	// 이미지 lazy loading 상태
	let loadedImages = $state<Set<number>>(new Set())
	let commentContent = $state('')
	let replyingTo = $state<number | null>(null)

	function handleImageLoad(index: number) {
		// Svelte 5에서 Set을 반응형으로 업데이트하려면 새 인스턴스를 생성해야 함
		loadedImages = new Set(loadedImages).add(index)
	}

	// 댓글 트리 구조 생성
	function buildCommentTree(comments: any[]) {
		const commentMap = new Map()
		const rootComments: any[] = []

		// 먼저 모든 댓글을 맵에 저장
		comments.forEach((comment) => {
			commentMap.set(comment.id, { ...comment, replies: [] })
		})

		// 부모-자식 관계 설정
		comments.forEach((comment) => {
			const commentNode = commentMap.get(comment.id)
			if (comment.parent_comment_id) {
				const parent = commentMap.get(comment.parent_comment_id)
				if (parent) {
					parent.replies.push(commentNode)
				}
			} else {
				rootComments.push(commentNode)
			}
		})

		return rootComments
	}

	let commentTree = $derived(buildCommentTree(comments || []))
</script>

<svelte:head>
	<title>{post.title} - 유머 게시판</title>
	<meta name="description" content={post.content?.substring(0, 160) || post.title} />
	<meta name="keywords" content="유머, {post.site_name}, 웃긴글, 재미" />

	<!-- Open Graph -->
	<meta property="og:title" content={post.title} />
	<meta property="og:description" content={post.content?.substring(0, 160) || post.title} />
	<meta property="og:type" content="article" />
	<meta property="og:url" content="https://yourdomain.com/post/{post.id}" />
	{#if images.length > 0}
		<meta property="og:image" content={images[0].r2_url} />
	{/if}
	<meta property="article:published_time" content={post.created_at} />
	<meta property="article:section" content="유머" />

	<!-- Twitter Card -->
	<meta name="twitter:card" content="summary_large_image" />
	<meta name="twitter:title" content={post.title} />
	<meta name="twitter:description" content={post.content?.substring(0, 160) || post.title} />
	{#if images.length > 0}
		<meta name="twitter:image" content={images[0].r2_url} />
	{/if}

	<!-- Canonical URL -->
	<link rel="canonical" href="https://yourdomain.com/post/{post.id}" />
</svelte:head>

<div class="mx-auto max-w-4xl">
	<!-- 뒤로 가기 -->
	<a href="/" class="mb-4 inline-flex items-center text-sm text-gray-600 hover:text-gray-900">
		← 목록으로
	</a>

	<!-- 게시글 헤더 -->
	<article class="overflow-hidden rounded-lg border border-gray-200 bg-white shadow-sm">
		<div class="border-b border-gray-200 bg-gray-50 px-6 py-4">
			<h1 class="text-2xl font-bold text-gray-900">{post.title}</h1>

			<div class="mt-2 flex items-center gap-3 text-sm text-gray-600">
				<span class="rounded bg-blue-100 px-2 py-1 text-xs font-medium text-blue-800">
					{post.site_name}
				</span>
				{#if post.created_at}
					<span>{new Date(post.created_at).toLocaleString('ko-KR')}</span>
				{/if}
				<button
					onclick={() => window.open(post.source_url, '_blank', 'noopener,noreferrer')}
					class="text-blue-600 hover:underline"
				>
					원문 보기 →
				</button>
			</div>
		</div>

		<!-- 게시글 본문 -->
		<div class="p-6">
			{#if post.content_html}
				<!-- HTML 렌더링 -->
				<div class="prose prose-gray max-w-none">
					{@html sanitizedHtml}
				</div>
			{:else}
				<!-- Fallback: 텍스트 + 이미지 갤러리 (기존 방식) -->
				{#if post.content}
					<div class="prose prose-gray max-w-none">
						<p class="whitespace-pre-wrap text-gray-700">{post.content}</p>
					</div>
				{/if}

				<!-- 이미지 갤러리 (content_html이 없을 때만) -->
				{#if images.length > 0}
					<div class="mt-6 space-y-4">
						{#each images as image, index}
							<div class="overflow-hidden rounded-lg border border-gray-200">
								<img
									src={image.r2_url}
									alt="게시글 이미지 {index + 1}"
									class="w-full"
									loading="lazy"
								/>
								{#if image.media_type === 'gif'}
									<div class="bg-gray-50 px-3 py-1 text-xs text-gray-600">
										GIF {image.duration_seconds ? `(${image.duration_seconds}초)` : ''}
									</div>
								{/if}
							</div>
						{/each}
					</div>
				{/if}
			{/if}
		</div>

		<!-- 게시글 푸터 -->
		<div class="border-t border-gray-200 bg-gray-50 px-6 py-4">
			<div class="flex items-center justify-between">
				<div class="text-sm text-gray-500">
					크롤링: {new Date(post.crawled_at).toLocaleString('ko-KR')}
				</div>

				<button
					class="rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white transition hover:bg-blue-700"
				>
					👍 좋아요
				</button>
			</div>
		</div>
	</article>

	<!-- 댓글 위 광고 -->
	{#if AD_CONFIG.adsense.enabled}
		<div class="mt-8">
			<AdSense slot={AD_CONFIG.adsense.slots.inArticle} format="rectangle" />
		</div>
	{:else if AD_CONFIG.adpost.enabled}
		<div class="mt-8 flex justify-center">
			<AdPost unitId={AD_CONFIG.adpost.units.inArticle} width={336} height={280} />
		</div>
	{/if}

	<!-- 댓글 섹션 -->
	<div class="mt-8 rounded-lg border border-gray-200 bg-white p-6">
		<h2 class="mb-4 text-xl font-bold text-gray-900">
			댓글 <span class="text-gray-500">({comments?.length || 0})</span>
		</h2>

		<!-- 댓글 작성 폼 -->
		{#if session}
			<form method="POST" action="?/comment" use:enhance class="mb-6">
				<textarea
					name="content"
					bind:value={commentContent}
					placeholder="댓글을 입력하세요..."
					class="w-full rounded-lg border border-gray-300 p-3 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
					rows="3"
				></textarea>
				<div class="mt-2 flex justify-end">
					<button
						type="submit"
						class="rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white transition hover:bg-blue-700"
					>
						댓글 작성
					</button>
				</div>
			</form>
		{:else}
			<div class="mb-6 rounded-lg bg-gray-50 p-4 text-center">
				<p class="text-gray-600">
					댓글을 작성하려면 <a href="/auth/login" class="text-blue-600 hover:underline"
						>로그인</a
					>이 필요합니다.
				</p>
			</div>
		{/if}

		<!-- 댓글 목록 -->
		{#if commentTree.length > 0}
			<div class="space-y-4">
				{#each commentTree as comment}
					<div class="border-b border-gray-100 pb-4 last:border-0">
						<div class="flex gap-3">
							<div class="flex-shrink-0">
								<div
									class="flex h-10 w-10 items-center justify-center rounded-full bg-blue-100 text-sm font-medium text-blue-600"
								>
									{comment.user_display_name?.[0] || '?'}
								</div>
							</div>
							<div class="flex-1">
								<div class="flex items-center gap-2">
									<span class="font-medium text-gray-900">{comment.user_display_name}</span>
									<span class="text-xs text-gray-500">
										{new Date(comment.created_at).toLocaleString('ko-KR')}
									</span>
								</div>
								<p class="mt-1 text-gray-700">{comment.content}</p>

								<!-- 대댓글 -->
								{#if comment.replies && comment.replies.length > 0}
									<div class="ml-8 mt-3 space-y-3">
										{#each comment.replies as reply}
											<div class="flex gap-3">
												<div class="flex-shrink-0">
													<div
														class="flex h-8 w-8 items-center justify-center rounded-full bg-gray-100 text-xs font-medium text-gray-600"
													>
														{reply.user_display_name?.[0] || '?'}
													</div>
												</div>
												<div class="flex-1">
													<div class="flex items-center gap-2">
														<span class="text-sm font-medium text-gray-900"
															>{reply.user_display_name}</span
														>
														<span class="text-xs text-gray-500">
															{new Date(reply.created_at).toLocaleString('ko-KR')}
														</span>
													</div>
													<p class="mt-1 text-sm text-gray-700">{reply.content}</p>
												</div>
											</div>
										{/each}
									</div>
								{/if}
							</div>
						</div>
					</div>
				{/each}
			</div>
		{:else}
			<p class="text-center text-gray-500">첫 댓글을 작성해보세요!</p>
		{/if}
	</div>
</div>

