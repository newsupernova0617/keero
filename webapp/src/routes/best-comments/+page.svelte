<script lang="ts">
	import type { PageData } from './$types'
	import * as Card from '$lib/components/ui/card'
	import { Badge } from '$lib/components/ui/badge'
	import { Button } from '$lib/components/ui/button'
	import { ThumbsUp, MessageCircle, ExternalLink, TrendingUp } from '@lucide/svelte'
	import { getBaseUrl, SITE_NAME } from '$lib/utils/seo'

	let { data }: { data: PageData } = $props()

	const baseUrl = getBaseUrl()

	// 상대 시간 포맷팅
	function getRelativeTime(dateStr: string) {
		const date = new Date(dateStr)
		const now = new Date()
		const diff = now.getTime() - date.getTime()
		const days = Math.floor(diff / (1000 * 60 * 60 * 24))

		if (days === 0) return '오늘'
		if (days === 1) return '어제'
		if (days < 7) return `${days}일 전`
		if (days < 30) return `${Math.floor(days / 7)}주 전`
		if (days < 365) return `${Math.floor(days / 30)}개월 전`
		return `${Math.floor(days / 365)}년 전`
	}
</script>

<svelte:head>
	<title>커뮤니티 베스트 댓글 - {SITE_NAME}</title>
	<meta
		name="description"
		content="KEERO 커뮤니티에서 가장 많은 사랑을 받은 베스트 댓글 TOP 100. 재치있고 공감되는 댓글을 한눈에 확인하세요."
	/>

	<!-- Open Graph -->
	<meta property="og:site_name" content={SITE_NAME} />
	<meta property="og:title" content="커뮤니티 베스트 댓글 - {SITE_NAME}" />
	<meta
		property="og:description"
		content="KEERO 커뮤니티에서 가장 많은 사랑을 받은 베스트 댓글 TOP 100"
	/>
	<meta property="og:type" content="website" />
	<meta property="og:url" content="{baseUrl}/best-comments" />
	<meta property="og:image" content="{baseUrl}/og-default.png" />

	<!-- Twitter Card -->
	<meta name="twitter:card" content="summary_large_image" />
	<meta name="twitter:title" content="커뮤니티 베스트 댓글 - {SITE_NAME}" />
	<meta
		name="twitter:description"
		content="KEERO 커뮤니티에서 가장 많은 사랑을 받은 베스트 댓글 TOP 100"
	/>
	<meta name="twitter:image" content="{baseUrl}/og-default.png" />

	<!-- Canonical -->
	<link rel="canonical" href="{baseUrl}/best-comments" />
</svelte:head>

<div class="mx-auto max-w-5xl px-4 py-12">
	<!-- 헤더 -->
	<div class="mb-8 text-center">
		<h1 class="mb-4 text-4xl font-bold">💬 커뮤니티 베스트 댓글</h1>
		<p class="text-lg text-muted-foreground">
			가장 많은 사랑을 받은 재치있고 공감되는 댓글 모음
		</p>
	</div>

	<!-- 통계 -->
	<Card.Root class="mb-8 border-2">
		<Card.Header>
			<Card.Title class="flex items-center gap-2">
				<TrendingUp class="h-5 w-5" />
				댓글 통계
			</Card.Title>
		</Card.Header>
		<Card.Content>
			<div class="grid gap-4 md:grid-cols-3">
				<div class="text-center">
					<div class="text-3xl font-bold text-primary">{data.stats.totalComments}</div>
					<div class="text-sm text-muted-foreground">베스트 댓글</div>
				</div>
				<div class="text-center">
					<div class="text-3xl font-bold text-primary">{data.stats.totalLikes}</div>
					<div class="text-sm text-muted-foreground">총 좋아요</div>
				</div>
				<div class="text-center">
					<div class="text-3xl font-bold text-primary">{data.stats.avgLikes}</div>
					<div class="text-sm text-muted-foreground">평균 좋아요</div>
				</div>
			</div>
		</Card.Content>
	</Card.Root>

	<!-- 댓글 리스트 -->
	{#if data.comments.length === 0}
		<Card.Root>
			<Card.Content class="py-12 text-center">
				<MessageCircle class="mx-auto mb-4 h-12 w-12 text-muted-foreground" />
				<p class="text-muted-foreground">아직 베스트 댓글이 없습니다.</p>
			</Card.Content>
		</Card.Root>
	{:else}
		<div class="grid gap-4 md:grid-cols-2">
			{#each data.comments as comment, index (comment.id)}
				<Card.Root class="transition-all hover:border-primary/50 hover:shadow-lg">
					<Card.Content class="pt-6">
						<!-- 순위 배지 (TOP 10만) -->
						{#if index < 10}
							<div class="mb-3">
								<Badge variant="secondary" class="font-bold">
									{#if index === 0}
										🥇 1위
									{:else if index === 1}
										🥈 2위
									{:else if index === 2}
										🥉 3위
									{:else}
										#{index + 1}
									{/if}
								</Badge>
							</div>
						{/if}

						<!-- 댓글 내용 -->
						<div class="mb-4 rounded-lg bg-muted/50 p-4">
							<p class="leading-relaxed">{comment.content}</p>
						</div>

						<!-- 메타 정보 -->
						<div class="space-y-2 text-sm">
							<!-- 작성자 & 좋아요 -->
							<div class="flex items-center justify-between">
								<span class="font-medium text-muted-foreground">
									👤 {comment.displayName}
								</span>
								<div class="flex items-center gap-1 text-primary">
									<ThumbsUp class="h-4 w-4" />
									<span class="font-bold">{comment.likeCount}</span>
								</div>
							</div>

							<!-- 원본 게시글 -->
							<div class="flex items-start gap-2">
								<Badge variant="outline" class="flex-shrink-0">
									{comment.postSiteName}
								</Badge>
								<a
									href="/post/{comment.postId}"
									class="flex-1 truncate text-muted-foreground transition-colors hover:text-primary"
								>
									{comment.postTitle}
								</a>
							</div>

							<!-- 시간 -->
							<div class="text-xs text-muted-foreground">
								{comment.createdAt ? getRelativeTime(comment.createdAt) : '알 수 없음'}
							</div>
						</div>
					</Card.Content>
				</Card.Root>
			{/each}
		</div>
	{/if}

	<!-- 푸터 -->
	<div class="mt-12 text-center">
		<p class="mb-4 text-sm text-muted-foreground">
			좋아요를 많이 받은 댓글이 자동으로 선정됩니다
		</p>
		<Button href="/" variant="outline">
			홈으로 돌아가기
		</Button>
	</div>
</div>
