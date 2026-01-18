<script lang="ts">
	import type { PageData } from './$types'
	import * as Card from '$lib/components/ui/card'
	import { Badge } from '$lib/components/ui/badge'
	import { Separator } from '$lib/components/ui/separator'
	import { TrendingUp, MessageSquare, ThumbsUp, Image, BarChart3, Trophy, Medal } from '@lucide/svelte'
	import { getBaseUrl, SITE_NAME } from '$lib/utils/seo'

	let { data }: { data: PageData } = $props()

	const baseUrl = getBaseUrl()

	// 사이트별 색상
	const siteColors: Record<string, string> = {
		'ppomppu': 'bg-orange-500',
		'fmkorea': 'bg-blue-500',
		'todayhumor': 'bg-green-500',
		'ruliweb': 'bg-purple-500',
		'humoruniv': 'bg-red-500',
	}

	function getSiteColor(siteName: string): string {
		return siteColors[siteName.toLowerCase()] || 'bg-gray-500'
	}

	function formatNumber(num: number): string {
		if (num >= 10000) {
			return (num / 10000).toFixed(1) + '만'
		} else if (num >= 1000) {
			return (num / 1000).toFixed(1) + '천'
		}
		return num.toString()
	}

	function getRankIcon(rank: number) {
		if (rank === 1) return { icon: Trophy, class: 'text-yellow-500' }
		if (rank === 2) return { icon: Medal, class: 'text-gray-400' }
		if (rank === 3) return { icon: Medal, class: 'text-amber-600' }
		return null
	}
</script>

<svelte:head>
	<title>통계 - {SITE_NAME}</title>
	<meta name="description" content="KEERO 유머 게시판의 주간/월간 베스트 게시글, 인기 순위, 사이트별 통계를 확인하세요." />
	
	<!-- Open Graph -->
	<meta property="og:site_name" content={SITE_NAME} />
	<meta property="og:title" content="통계 - KEERO" />
	<meta property="og:description" content="KEERO 유머 게시판의 주간/월간 베스트 게시글, 인기 순위, 사이트별 통계를 확인하세요." />
	<meta property="og:type" content="website" />
	<meta property="og:url" content="{baseUrl}/stats" />
	<meta property="og:image" content="{baseUrl}/og-default.png" />
	
	<!-- Twitter Card -->
	<meta name="twitter:card" content="summary" />
	<meta name="twitter:title" content="통계 - KEERO" />
	<meta name="twitter:description" content="KEERO 유머 게시판의 주간/월간 베스트 게시글, 인기 순위, 사이트별 통계를 확인하세요." />
	<meta name="twitter:image" content="{baseUrl}/og-default.png" />
	
	<!-- Canonical -->
	<link rel="canonical" href="{baseUrl}/stats" />
</svelte:head>

<div class="space-y-8">
	<!-- 헤더 -->
	<div>
		<h1 class="text-3xl font-bold tracking-tight flex items-center gap-3">
			<BarChart3 class="h-8 w-8 text-primary" />
			통계
		</h1>
		<p class="mt-2 text-muted-foreground">
			KEERO 유머 게시판의 인기 게시글과 활동 통계를 확인하세요.
		</p>
	</div>

	<!-- 전체 통계 카드 -->
	<div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-5">
		<Card.Root>
			<Card.Content class="p-6">
				<div class="flex items-center gap-4">
					<div class="rounded-full bg-primary/10 p-3">
						<BarChart3 class="h-6 w-6 text-primary" />
					</div>
					<div>
						<p class="text-sm text-muted-foreground">전체 게시글</p>
						<p class="text-2xl font-bold">{formatNumber(data.overview.totalPosts)}</p>
					</div>
				</div>
			</Card.Content>
		</Card.Root>

		<Card.Root>
			<Card.Content class="p-6">
				<div class="flex items-center gap-4">
					<div class="rounded-full bg-red-500/10 p-3">
						<ThumbsUp class="h-6 w-6 text-red-500" />
					</div>
					<div>
						<p class="text-sm text-muted-foreground">총 좋아요</p>
						<p class="text-2xl font-bold">{formatNumber(data.overview.totalLikes)}</p>
					</div>
				</div>
			</Card.Content>
		</Card.Root>

		<Card.Root>
			<Card.Content class="p-6">
				<div class="flex items-center gap-4">
					<div class="rounded-full bg-blue-500/10 p-3">
						<MessageSquare class="h-6 w-6 text-blue-500" />
					</div>
					<div>
						<p class="text-sm text-muted-foreground">총 댓글</p>
						<p class="text-2xl font-bold">{formatNumber(data.overview.totalComments)}</p>
					</div>
				</div>
			</Card.Content>
		</Card.Root>

		<Card.Root>
			<Card.Content class="p-6">
				<div class="flex items-center gap-4">
					<div class="rounded-full bg-green-500/10 p-3">
						<Image class="h-6 w-6 text-green-500" />
					</div>
					<div>
						<p class="text-sm text-muted-foreground">총 이미지</p>
						<p class="text-2xl font-bold">{formatNumber(data.overview.totalImages)}</p>
					</div>
				</div>
			</Card.Content>
		</Card.Root>

		<Card.Root>
			<Card.Content class="p-6">
				<div class="flex items-center gap-4">
					<div class="rounded-full bg-purple-500/10 p-3">
						<TrendingUp class="h-6 w-6 text-purple-500" />
					</div>
					<div>
						<p class="text-sm text-muted-foreground">최근 7일</p>
						<p class="text-2xl font-bold">+{formatNumber(data.overview.recentPosts)}</p>
					</div>
				</div>
			</Card.Content>
		</Card.Root>
	</div>

	<!-- 사이트별 통계 -->
	<Card.Root>
		<Card.Header>
			<Card.Title class="flex items-center gap-2">
				<BarChart3 class="h-5 w-5" />
				사이트별 게시글 수
			</Card.Title>
		</Card.Header>
		<Card.Content>
			<div class="space-y-3">
				{#each data.siteStats as stat, index}
					{@const percentage = Math.round((stat.total_posts / data.overview.totalPosts) * 100)}
					<div class="flex items-center gap-4">
						<div class="w-24 font-medium">{stat.site_name}</div>
						<div class="flex-1">
							<div class="h-4 w-full rounded-full bg-muted overflow-hidden">
								<div 
									class="h-full rounded-full transition-all duration-500 {getSiteColor(stat.site_name)}"
									style="width: {percentage}%"
								></div>
							</div>
						</div>
						<div class="w-20 text-right text-sm text-muted-foreground">
							{formatNumber(stat.total_posts)} ({percentage}%)
						</div>
					</div>
				{/each}
			</div>
		</Card.Content>
	</Card.Root>

	<Separator />

	<!-- 베스트 게시글 섹션 -->
	<div class="grid gap-6 lg:grid-cols-3">
		<!-- 주간 베스트 -->
		<Card.Root>
			<Card.Header>
				<Card.Title class="flex items-center gap-2">
					<Trophy class="h-5 w-5 text-yellow-500" />
					주간 베스트
				</Card.Title>
				<Card.Description>최근 7일간 좋아요가 많은 게시글</Card.Description>
			</Card.Header>
			<Card.Content>
				<div class="space-y-3">
					{#each data.weeklyBest as post, index}
						{@const rankInfo = getRankIcon(index + 1)}
						<a 
							href="/post/{post.id}"
							class="flex items-start gap-3 rounded-lg p-2 transition hover:bg-accent"
						>
							<div class="flex h-6 w-6 items-center justify-center text-sm font-bold text-muted-foreground">
								{#if rankInfo}
									<svelte:component this={rankInfo.icon} class="h-5 w-5 {rankInfo.class}" />
								{:else}
									{index + 1}
								{/if}
							</div>
							<div class="flex-1 min-w-0">
								<p class="line-clamp-1 text-sm font-medium">{post.title}</p>
								<div class="flex items-center gap-2 mt-1">
									<Badge variant="secondary" class="text-xs">{post.site_name}</Badge>
									<span class="text-xs text-muted-foreground flex items-center gap-1">
										<ThumbsUp class="h-3 w-3" />
										{post.like_count}
									</span>
								</div>
							</div>
						</a>
					{/each}
					{#if data.weeklyBest.length === 0}
						<p class="text-center text-sm text-muted-foreground py-4">
							아직 데이터가 없습니다
						</p>
					{/if}
				</div>
			</Card.Content>
		</Card.Root>

		<!-- 월간 베스트 -->
		<Card.Root>
			<Card.Header>
				<Card.Title class="flex items-center gap-2">
					<Medal class="h-5 w-5 text-amber-600" />
					월간 베스트
				</Card.Title>
				<Card.Description>최근 30일간 좋아요가 많은 게시글</Card.Description>
			</Card.Header>
			<Card.Content>
				<div class="space-y-3">
					{#each data.monthlyBest as post, index}
						{@const rankInfo = getRankIcon(index + 1)}
						<a 
							href="/post/{post.id}"
							class="flex items-start gap-3 rounded-lg p-2 transition hover:bg-accent"
						>
							<div class="flex h-6 w-6 items-center justify-center text-sm font-bold text-muted-foreground">
								{#if rankInfo}
									<svelte:component this={rankInfo.icon} class="h-5 w-5 {rankInfo.class}" />
								{:else}
									{index + 1}
								{/if}
							</div>
							<div class="flex-1 min-w-0">
								<p class="line-clamp-1 text-sm font-medium">{post.title}</p>
								<div class="flex items-center gap-2 mt-1">
									<Badge variant="secondary" class="text-xs">{post.site_name}</Badge>
									<span class="text-xs text-muted-foreground flex items-center gap-1">
										<ThumbsUp class="h-3 w-3" />
										{post.like_count}
									</span>
								</div>
							</div>
						</a>
					{/each}
					{#if data.monthlyBest.length === 0}
						<p class="text-center text-sm text-muted-foreground py-4">
							아직 데이터가 없습니다
						</p>
					{/if}
				</div>
			</Card.Content>
		</Card.Root>

		<!-- 댓글 활발 -->
		<Card.Root>
			<Card.Header>
				<Card.Title class="flex items-center gap-2">
					<MessageSquare class="h-5 w-5 text-blue-500" />
					활발한 토론
				</Card.Title>
				<Card.Description>최근 7일간 댓글이 많은 게시글</Card.Description>
			</Card.Header>
			<Card.Content>
				<div class="space-y-3">
					{#each data.mostDiscussed as post, index}
						{@const rankInfo = getRankIcon(index + 1)}
						<a 
							href="/post/{post.id}"
							class="flex items-start gap-3 rounded-lg p-2 transition hover:bg-accent"
						>
							<div class="flex h-6 w-6 items-center justify-center text-sm font-bold text-muted-foreground">
								{#if rankInfo}
									<svelte:component this={rankInfo.icon} class="h-5 w-5 {rankInfo.class}" />
								{:else}
									{index + 1}
								{/if}
							</div>
							<div class="flex-1 min-w-0">
								<p class="line-clamp-1 text-sm font-medium">{post.title}</p>
								<div class="flex items-center gap-2 mt-1">
									<Badge variant="secondary" class="text-xs">{post.site_name}</Badge>
									<span class="text-xs text-muted-foreground flex items-center gap-1">
										<MessageSquare class="h-3 w-3" />
										{post.comment_count}
									</span>
								</div>
							</div>
						</a>
					{/each}
					{#if data.mostDiscussed.length === 0}
						<p class="text-center text-sm text-muted-foreground py-4">
							아직 데이터가 없습니다
						</p>
					{/if}
				</div>
			</Card.Content>
		</Card.Root>
	</div>

	<!-- 마지막 업데이트 -->
	<div class="text-center text-sm text-muted-foreground">
		데이터는 실시간으로 업데이트됩니다
	</div>
</div>
