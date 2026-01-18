<script lang="ts">
	import type { PageData } from './$types'
	import * as Card from '$lib/components/ui/card'
	import { Badge } from '$lib/components/ui/badge'
	import { Button } from '$lib/components/ui/button'
	import { Separator } from '$lib/components/ui/separator'
	import { ThumbsUp, MessageCircle, ExternalLink, TrendingUp, Calendar } from '@lucide/svelte'
	import { getBaseUrl, SITE_NAME } from '$lib/utils/seo'

	let { data }: { data: PageData } = $props()

	const baseUrl = getBaseUrl()

	// 순위 아이콘
	function getRankIcon(rank: number) {
		switch (rank) {
			case 1:
				return { icon: '🥇', class: 'text-yellow-500' }
			case 2:
				return { icon: '🥈', class: 'text-gray-400' }
			case 3:
				return { icon: '🥉', class: 'text-amber-600' }
			default:
				return { icon: `${rank}위`, class: 'text-muted-foreground' }
		}
	}

	// 날짜 포맷팅
	function formatDate(dateStr: string) {
		const date = new Date(dateStr)
		return date.toLocaleDateString('ko-KR', {
			year: 'numeric',
			month: 'long',
			day: 'numeric'
		})
	}

	function formatWeekRange(start: string, end: string) {
		const startDate = new Date(start)
		const endDate = new Date(end)
		return `${startDate.getMonth() + 1}월 ${startDate.getDate()}일 - ${endDate.getMonth() + 1}월 ${endDate.getDate()}일`
	}
</script>

<svelte:head>
	<title>이번 주 유머 하이라이트 - {SITE_NAME}</title>
	<meta
		name="description"
		content="{data.weekStart}부터 {data.weekEnd}까지 주간 베스트 유머 게시글 TOP 10과 인기 댓글"
	/>

	<!-- Open Graph -->
	<meta property="og:site_name" content={SITE_NAME} />
	<meta property="og:title" content="이번 주 유머 하이라이트 - {SITE_NAME}" />
	<meta
		property="og:description"
		content="{formatWeekRange(data.weekStart, data.weekEnd)} 주간 베스트 유머 게시글 TOP 10"
	/>
	<meta property="og:type" content="article" />
	<meta property="og:url" content="{baseUrl}/highlights/weekly" />
	<meta property="og:image" content="{baseUrl}/og-default.png" />
	<meta property="article:published_time" content={data.weekStart} />

	<!-- Twitter Card -->
	<meta name="twitter:card" content="summary_large_image" />
	<meta name="twitter:title" content="이번 주 유머 하이라이트 - {SITE_NAME}" />
	<meta
		name="twitter:description"
		content="{formatWeekRange(data.weekStart, data.weekEnd)} 주간 베스트 유머 게시글 TOP 10"
	/>
	<meta name="twitter:image" content="{baseUrl}/og-default.png" />

	<!-- Canonical -->
	<link rel="canonical" href="{baseUrl}/highlights/weekly" />

	<!-- JSON-LD -->
	<script type="application/ld+json">
		{JSON.stringify({
			'@context': 'https://schema.org',
			'@type': 'Article',
			headline: '이번 주 유머 하이라이트',
			datePublished: data.weekStart,
			author: {
				'@type': 'Organization',
				name: SITE_NAME
			},
			description: `${formatWeekRange(data.weekStart, data.weekEnd)} 주간 베스트 유머 게시글 TOP 10`
		})}
	</script>
</svelte:head>

<div class="mx-auto max-w-5xl px-4 py-12">
	<!-- 헤더 -->
	<div class="mb-8 text-center">
		<div class="mb-2 flex items-center justify-center gap-2 text-sm text-muted-foreground">
			<Calendar class="h-4 w-4" />
			<span>{formatWeekRange(data.weekStart, data.weekEnd)}</span>
		</div>
		<h1 class="mb-4 text-4xl font-bold">📅 이번 주 유머 하이라이트</h1>
		<p class="text-lg text-muted-foreground">
			커뮤니티에서 가장 사랑받은 게시글 TOP 10
		</p>
	</div>

	<!-- 주간 통계 -->
	<Card.Root class="mb-8 border-2">
		<Card.Header>
			<Card.Title class="flex items-center gap-2">
				<TrendingUp class="h-5 w-5" />
				이번 주 통계
			</Card.Title>
		</Card.Header>
		<Card.Content>
			<div class="grid gap-4 md:grid-cols-4">
				<div class="text-center">
					<div class="text-3xl font-bold text-primary">{data.stats.totalPosts}</div>
					<div class="text-sm text-muted-foreground">게시글</div>
				</div>
				<div class="text-center">
					<div class="text-3xl font-bold text-primary">{data.stats.totalLikes}</div>
					<div class="text-sm text-muted-foreground">좋아요</div>
				</div>
				<div class="text-center">
					<div class="text-3xl font-bold text-primary">{data.stats.totalComments}</div>
					<div class="text-sm text-muted-foreground">댓글</div>
				</div>
				<div class="text-center">
					<div class="text-2xl font-bold text-primary">{data.stats.topSiteName}</div>
					<div class="text-sm text-muted-foreground">가장 활발한 사이트</div>
				</div>
			</div>
		</Card.Content>
	</Card.Root>

	<!-- TOP 10 게시글 -->
	<div class="space-y-6">
		{#each data.posts as post (post.id)}
			{@const rankInfo = getRankIcon(post.rank)}
			<Card.Root class="overflow-hidden border-2 transition-all hover:border-primary/50 hover:shadow-xl">
				<Card.Header class="bg-muted/30">
					<div class="flex items-start justify-between gap-4">
						<div class="flex-1">
							<div class="mb-2 flex items-center gap-3">
								<span class="text-3xl {rankInfo.class}">{rankInfo.icon}</span>
								<Badge variant="secondary" class="font-medium">{post.siteName}</Badge>
							</div>
							<Card.Title class="text-2xl">
								<a
									href="/post/{post.id}"
									class="transition-colors hover:text-primary"
								>
									{post.title}
								</a>
							</Card.Title>
						</div>
					</div>
				</Card.Header>

				<Card.Content class="pt-6">
					<!-- 에디터 코멘트 -->
					<div class="mb-4 rounded-lg border-l-4 border-primary bg-primary/5 p-4">
						<div class="mb-1 text-xs font-semibold uppercase text-primary">
							📝 에디터의 한마디
						</div>
						<p class="text-sm leading-relaxed">{post.editorComment}</p>
					</div>

					<!-- 베스트 댓글 -->
					{#if post.bestComments.length > 0}
						<div class="mb-4">
							<div class="mb-3 flex items-center gap-2 text-sm font-semibold">
								<MessageCircle class="h-4 w-4" />
								💬 베스트 댓글 TOP {post.bestComments.length}
							</div>
							<div class="space-y-2">
								{#each post.bestComments as comment, idx}
									<div class="rounded-lg border bg-card p-3">
										<div class="mb-1 flex items-center justify-between">
											<span class="text-xs font-medium text-muted-foreground">
												{comment.displayName}
											</span>
											<div class="flex items-center gap-1 text-xs text-muted-foreground">
												<ThumbsUp class="h-3 w-3" />
												{comment.likeCount}
											</div>
										</div>
										<p class="text-sm">{comment.content}</p>
									</div>
								{/each}
							</div>
						</div>
					{/if}

					<!-- 반응 통계 -->
					<div class="flex flex-wrap items-center gap-4 text-sm text-muted-foreground">
						<div class="flex items-center gap-1">
							<ThumbsUp class="h-4 w-4" />
							<span>좋아요 {post.likeCount}개</span>
						</div>
						<div class="flex items-center gap-1">
							<MessageCircle class="h-4 w-4" />
							<span>댓글 {post.commentCount}개</span>
						</div>
						<Separator orientation="vertical" class="h-4" />
						<a
							href={post.sourceUrl}
							target="_blank"
							rel="noopener noreferrer"
							class="flex items-center gap-1 text-primary hover:underline"
						>
							<ExternalLink class="h-4 w-4" />
							<span>원본 보기</span>
						</a>
					</div>
				</Card.Content>
			</Card.Root>
		{/each}
	</div>

	<!-- 푸터 -->
	<div class="mt-12 text-center">
		<p class="mb-4 text-sm text-muted-foreground">
			매주 월요일 새로운 하이라이트가 업데이트됩니다
		</p>
		<Button href="/" variant="outline">
			홈으로 돌아가기
		</Button>
	</div>
</div>
