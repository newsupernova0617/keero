<script lang="ts">
	import type { PageData } from './$types'
	import { enhance } from '$app/forms'
	import { goto } from '$app/navigation'
	import { tick } from 'svelte'
	import DOMPurify from 'isomorphic-dompurify'
	import * as Card from '$lib/components/ui/card'
	import { Badge } from '$lib/components/ui/badge'
	import { Button } from '$lib/components/ui/button'
	import { Separator } from '$lib/components/ui/separator'
	import { Textarea } from '$lib/components/ui/textarea'
	import AdSense from '$lib/components/ads/AdSense.svelte'
import AdFit from '$lib/components/ads/AdFit.svelte'
	import { AD_CONFIG } from '$lib/config/ads'
	import Comment from '$lib/components/Comment.svelte'
	import { ArrowLeft, ExternalLink, ThumbsUp, Share2, MessageSquare } from '@lucide/svelte'
	import { onMount } from 'svelte'

	let { data }: { data: PageData } = $props()
	let { post, comments, session, currentUserId, likeCount, userLiked } = $derived(data)
	
	// 중복 제거 및 썸네일 필터링된 이미지 목록
	let images = $derived.by(() => {
		const rawImages = data.images || []
		const seen = new Set<string>()
		
		// 1차 필터: 중복 URL 제거
		const uniqueImages = rawImages.filter((img) => {
			const url = img.r2_url || ''
			if (seen.has(url)) return false
			seen.add(url)
			return true
		})
		
		// 비디오가 있는지 확인
		const hasVideo = uniqueImages.some(img => {
			const url = img.r2_url?.toLowerCase() || ''
			return url.endsWith('.mp4') || url.endsWith('.webm')
		})
		
		// 비디오가 있으면 jpg/png 이미지 제거 (펨코 썸네일)
		if (hasVideo) {
			return uniqueImages.filter(img => {
				const url = img.r2_url?.toLowerCase() || ''
				// 비디오만 남기기
				return url.endsWith('.mp4') || url.endsWith('.webm') || url.endsWith('.gif')
			})
		}
		
		return uniqueImages
	})
	
	// 비디오에 controls 속성 추가
	onMount(() => {
		document.querySelectorAll('video').forEach(video => {
			video.setAttribute('controls', '')
			video.style.maxWidth = '100%'
			video.style.height = 'auto'
		})
	})
	
	// HTML sanitize (placeholder 제거하고 텍스트만 표시)
	let sanitizedHtml = $derived.by(() => {
		if (!post.content_html) return ''
		
		// HTML sanitize - placeholder 태그 제거하고 텍스트만 남김
		let html = DOMPurify.sanitize(post.content_html, {
			ALLOWED_TAGS: ['p', 'br', 'b', 'strong', 'i', 'em', 'u', 's', 'a', 'div', 'span', 'blockquote', 'ul', 'ol', 'li', 'table', 'tbody', 'tr', 'td'],
			ALLOWED_ATTR: ['href', 'alt', 'title', 'class']
		})
		
		return html
	})

	let commentContent = $state('')
	let replyingTo = $state<number | null>(null)
	let replyContent = $state('')
	let editingComment = $state<number | null>(null)
	let editContent = $state('')
	
	// 좋아요 상태 관리
	let isLiking = $state(false)
	let currentLikeCount = $state(0)
	let currentUserLiked = $state(false)
	
	// 초기값 설정
	$effect(() => {
		currentLikeCount = data.likeCount
		currentUserLiked = data.userLiked
	})
	
	// 좋아요 토글 함수
	async function toggleLike() {
		if (!session) {
			window.location.href = '/auth/login'
			return
		}
		
		if (isLiking) return
		
		isLiking = true
		
		// 낙관적 업데이트 (Optimistic Update)
		const prevLiked = currentUserLiked
		const prevCount = currentLikeCount
		
		currentUserLiked = !currentUserLiked
		currentLikeCount = currentUserLiked ? currentLikeCount + 1 : currentLikeCount - 1
		
		try {
			const formData = new FormData()
			const response = await fetch('?/toggleLike', {
				method: 'POST',
				body: formData
			})
			
			if (!response.ok) {
				// 실패 시 롤백
				currentUserLiked = prevLiked
				currentLikeCount = prevCount
			}
		} catch (error) {
			console.error('좋아요 실패:', error)
			// 에러 시 롤백
			currentUserLiked = prevLiked
			currentLikeCount = prevCount
		} finally {
			isLiking = false
		}
	}

	// 댓글 트리 구조 생성
	function buildCommentTree(comments: any[]) {
		const commentMap = new Map()
		const rootComments: any[] = []

		comments.forEach((comment) => {
			commentMap.set(comment.id, { ...comment, replies: [] })
		})

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
	
	function toggleReply(commentId: number) {
		if (replyingTo === commentId) {
			replyingTo = null
			replyContent = ''
		} else {
			replyingTo = commentId
			replyContent = ''
		}
	}
	
	function toggleEdit(commentId: number, content: string) {
		editingComment = commentId
		editContent = content
	}
	
	function cancelEdit() {
		editingComment = null
		editContent = ''
	}
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

<div class="mx-auto max-w-4xl space-y-6">
	<!-- 뒤로 가기 -->
	<Button href="/" variant="ghost" size="sm" class="gap-2">
		<ArrowLeft class="h-4 w-4" />
		목록으로
	</Button>

	<!-- 게시글 카드 -->
	<Card.Root class="overflow-hidden">
		<!-- 헤더 -->
		<Card.Header class="space-y-3 bg-muted/50">
			<div class="flex items-start justify-between gap-4">
				<div class="flex-1 space-y-2">
					<Badge variant="secondary" class="w-fit">
						{post.site_name}
					</Badge>
					<Card.Title class="text-2xl leading-tight">
						{post.title}
					</Card.Title>
				</div>
			</div>

			<div class="flex flex-wrap items-center gap-3 text-sm text-muted-foreground">
				{#if post.created_at}
					<span>{new Date(post.created_at).toLocaleString('ko-KR')}</span>
				{/if}
				<Separator orientation="vertical" class="h-4" />
				<Button
					variant="ghost"
					size="sm"
					class="h-auto gap-2 p-0 hover:bg-transparent"
					onclick={() => window.open(post.source_url, '_blank', 'noopener,noreferrer')}
				>
					<ExternalLink class="h-4 w-4" />
					원문 보기
				</Button>
			</div>
		</Card.Header>

		<!-- 본문 -->
		<Card.Content class="p-6">
			<!-- HTML 본문 (이미지 포함) -->
			{#if post.content_html}
				<div class="prose prose-gray max-w-none dark:prose-invert">
					{@html sanitizedHtml}
				</div>
			{:else if post.content}
				<div class="prose prose-gray max-w-none dark:prose-invert">
					<p class="whitespace-pre-wrap">{post.content}</p>
				</div>
			{/if}
			
			<!-- 미디어 갤러리 (항상 표시) -->
			{#if images.length > 0}
				<div class="mt-6 space-y-4">
					{#each images as image, idx}
						{@const url = image.r2_url?.toLowerCase() || ''}
						{@const isVideo = url.endsWith('.mp4') || url.endsWith('.webm') || url.endsWith('.mov')}
						{@const isGif = url.endsWith('.gif')}
						
						{#if isVideo}
							<video
								src={image.r2_url}
								controls
								class="w-full max-w-2xl rounded-lg"
								preload="metadata"
							>
								<track kind="captions" />
							</video>
						{:else if isGif}
							<img
								src={image.r2_url}
								alt="움짤 {idx + 1}"
								class="w-full max-w-2xl rounded-lg"
								loading="lazy"
							/>
						{:else}
							<img
								src={image.r2_url}
								alt="이미지 {idx + 1}"
								class="w-full max-w-2xl rounded-lg"
								loading="lazy"
							/>
						{/if}
					{/each}
				</div>
			{/if}
		</Card.Content>

		<!-- 푸터 액션 -->
		<Card.Footer class="flex items-center justify-between border-t bg-muted/50 p-4">
			{#if post.crawled_at}
				<div class="text-xs text-muted-foreground">
					크롤링: {new Date(post.crawled_at).toLocaleString('ko-KR')}
				</div>
			{:else}
				<div class="text-xs text-muted-foreground">
					크롤링 정보 없음
				</div>
			{/if}

			<div class="flex gap-2">
				<Button 
					variant={currentUserLiked ? "default" : "outline"} 
					size="sm" 
					class="gap-2"
					onclick={toggleLike}
					disabled={isLiking}
				>
					<ThumbsUp class={currentUserLiked ? "h-4 w-4 fill-current" : "h-4 w-4"} />
					좋아요
					{#if currentLikeCount > 0}
						<span class="ml-1 font-semibold">{currentLikeCount}</span>
					{/if}
				</Button>
				<!-- 공유 버튼은 보류
				<Button variant="outline" size="sm" class="gap-2">
					<Share2 class="h-4 w-4" />
					공유
				</Button>
				-->
			</div>
		</Card.Footer>
	</Card.Root>

	<!-- 광고 영역 -->
	<div class="py-4">
		<div class="flex flex-col items-center gap-3">
			<!-- 광고 라벨 -->
			<div class="flex items-center gap-2">
				<div class="h-px w-12 bg-border"></div>
				<span class="text-xs font-medium text-muted-foreground">Advertisement</span>
				<div class="h-px w-12 bg-border"></div>
			</div>
			
			<!-- 광고 -->
			{#if AD_CONFIG.adsense.enabled}
				<AdSense slot={AD_CONFIG.adsense.slots.inArticle} format="horizontal" />
			{:else if AD_CONFIG.adfit.enabled}
				<AdFit unit={AD_CONFIG.adfit.units.inArticle} width={728} height={90} />
			{/if}
		</div>
	</div>

	<!-- 댓글 섹션 -->
	<Card.Root id="comments">
		<Card.Header>
			<Card.Title class="flex items-center gap-2">
				<MessageSquare class="h-5 w-5" />
				댓글
				<Badge variant="secondary">{comments?.length || 0}</Badge>
			</Card.Title>
		</Card.Header>

		<Card.Content class="space-y-6">
			<!-- 댓글 작성 폼 -->
			{#if session}
				<form 
					method="POST" 
					action="?/comment" 
					use:enhance={() => {
						return async ({ result }) => {
							if (result.type === 'success') {
								commentContent = ''
								
								// URL 해시로 댓글 섹션 이동
								await goto(`${window.location.pathname}#comments`, { 
									invalidateAll: true,
									replaceState: false
								})
								
								// DOM 업데이트 완료까지 대기
								await tick()
								await tick()
								
								// 댓글 섹션으로 스크롤
								const commentsEl = document.getElementById('comments')
								if (commentsEl) {
									commentsEl.scrollIntoView({ behavior: 'smooth', block: 'start' })
								}
							}
						}
					}}
					class="space-y-3"
				>
					<Textarea
						name="content"
						bind:value={commentContent}
						placeholder="댓글을 입력하세요... (Enter: 작성, Shift+Enter: 줄바꿈)"
						rows={3}
						onkeydown={(e) => {
							if (e.key === 'Enter' && !e.shiftKey) {
								e.preventDefault()
								if (!commentContent.trim()) return
								const form = e.currentTarget.closest('form')
								if (form) form.requestSubmit()
							}
						}}
					/>
					<div class="flex justify-end">
						<Button type="submit" size="sm">
							댓글 작성
						</Button>
					</div>
				</form>
			{:else}
				<Card.Root class="bg-muted/50">
					<Card.Content class="p-4 text-center">
						<p class="text-sm text-muted-foreground">
							댓글을 작성하려면 
							<Button href="/auth/login" variant="link" class="h-auto p-0">
								로그인
							</Button>
							이 필요합니다.
						</p>
					</Card.Content>
				</Card.Root>
			{/if}

			<Separator />

			<!-- 댓글 목록 -->
{#if commentTree.length > 0}
	<div class="space-y-4">
		{#each commentTree as comment}
			<Comment
				{comment}
				{currentUserId}
				{session}
				{replyingTo}
				{editingComment}
				bind:replyContent
				bind:editContent
				onToggleReply={toggleReply}
				onToggleEdit={toggleEdit}
				onCancelEdit={cancelEdit}
			/>
		{/each}
	</div>
{:else}
	<p class="text-center text-sm text-muted-foreground">첫 댓글을 작성해보세요!</p>
{/if}
		</Card.Content>
	</Card.Root>
</div>
