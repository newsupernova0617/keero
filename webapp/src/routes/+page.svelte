<script lang="ts">
	import type { PageData } from './$types'
	import * as Card from '$lib/components/ui/card'
	import { Badge } from '$lib/components/ui/badge'
	import { Button } from '$lib/components/ui/button'
	import AdSense from '$lib/components/ads/AdSense.svelte'
	import AdPost from '$lib/components/ads/AdPost.svelte'
	import AdFit from '$lib/components/ads/AdFit.svelte'
	import { AD_CONFIG, AD_RULES } from '$lib/config/ads'
	// import SiteFilter from '$lib/components/SiteFilter.svelte'
	import PostCardSkeleton from '$lib/components/PostCardSkeleton.svelte'
	import EmptyState from '$lib/components/EmptyState.svelte'
	import { Image } from '@lucide/svelte'
	import { getBaseUrl, getDefaultOgImage, SITE_NAME } from '$lib/utils/seo'

	let { data }: { data: PageData } = $props()
	
	// let selectedSite = $state('all')
	let isLoading = $state(false)
	
	// 필터링된 게시글
	// let filteredPosts = $derived(
	// 	selectedSite === 'all' 
	// 		? data.posts 
	// 		: data.posts.filter(post => post.site_name === selectedSite)
	// )
	let filteredPosts = $derived(data.posts)
	
	// function handleFilterChange(site: string) {
	// 	selectedSite = site
	// }
	
	const baseUrl = getBaseUrl()
	const ogImage = getDefaultOgImage()
</script>

<svelte:head>
	<title>유머 게시판 - 재미있는 유머, 웃긴 글 모음</title>
	<meta
		name="description"
		content="FMKorea, 루리웹 등에서 엄선한 재미있는 유머와 웃긴 글을 한곳에서 만나보세요. 매일 업데이트되는 최신 유머 게시글."
	/>
	<meta name="keywords" content="유머, 웃긴글, 재미, 커뮤니티, FMKorea, 루리웹, 베스트글" />

	<!-- Open Graph -->
	<meta property="og:site_name" content={SITE_NAME} />
	<meta property="og:title" content="유머 게시판 - 재미있는 유머, 웃긴 글 모음" />
	<meta
		property="og:description"
		content="FMKorea, 루리웹 등에서 엄선한 재미있는 유머와 웃긴 글을 한곳에서 만나보세요."
	/>
	<meta property="og:type" content="website" />
	<meta property="og:url" content={baseUrl} />
	<meta property="og:image" content={ogImage} />
	<meta property="og:image:width" content="1200" />
	<meta property="og:image:height" content="630" />

	<!-- Twitter Card -->
	<meta name="twitter:card" content="summary_large_image" />
	<meta name="twitter:title" content="유머 게시판 - 재미있는 유머, 웃긴 글 모음" />
	<meta
		name="twitter:description"
		content="FMKorea, 루리웹 등에서 엄선한 재미있는 유머와 웃긴 글을 한곳에서 만나보세요."
	/>
	<meta name="twitter:image" content={ogImage} />

	<!-- 추가 SEO -->
	<link rel="canonical" href={baseUrl} />
	
	<!-- JSON-LD 구조화 데이터 -->
	<script type="application/ld+json">
		{JSON.stringify({
			"@context": "https://schema.org",
			"@type": "WebSite",
			"name": SITE_NAME,
			"url": baseUrl,
			"description": "FMKorea, 루리웹, 오늘의유머 등에서 엄선한 재미있는 유머와 웃긴 글을 한곳에서 만나보세요.",
			"potentialAction": {
				"@type": "SearchAction",
				"target": `${baseUrl}/search?q={search_term_string}`,
				"query-input": "required name=search_term_string"
			}
		})}
	</script>
</svelte:head>

<div class="space-y-6">
	<!-- Header -->
	<div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
		<div>
			<h1 class="text-3xl font-bold tracking-tight">최신 게시글</h1>
			<p class="mt-1 text-sm text-muted-foreground">
				여러 커뮤니티의 재미있는 유머를 한눈에
			</p>
		</div>
		<Badge variant="secondary" class="w-fit">
			{filteredPosts.length}개의 게시글
		</Badge>
	</div>

	<!-- Site Filter -->
	<!-- <SiteFilter onFilterChange={handleFilterChange} /> -->

	<!-- Posts Grid -->
	{#if isLoading}
		<div class="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
			{#each Array(6) as _}
				<PostCardSkeleton />
			{/each}
		</div>
	{:else if filteredPosts.length === 0}
		<EmptyState 
			title="게시글이 없습니다"
			description="아직 크롤링된 게시글이 없습니다."
		/>
	{:else}
		<div class="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
			{#each filteredPosts as post, index}
				<!-- 게시글 카드 -->
				<a 
					href="/post/{post.id}" 
					class="group block cursor-pointer transition-transform hover:scale-[1.02]"
				>
					<Card.Root class="h-full overflow-hidden border-2 transition-all hover:border-primary/50 hover:shadow-xl">
						{#if post.thumbnail}
							<div class="relative aspect-video overflow-hidden bg-muted">
								<img
									src={post.thumbnail}
									alt={post.title}
									class="h-full w-full object-cover transition-transform duration-300 group-hover:scale-110"
									loading="lazy"
								/>
								{#if post.image_count > 1}
									<div class="absolute bottom-2 right-2 flex items-center gap-1 rounded-full bg-black/70 px-2 py-1 text-xs text-white backdrop-blur-sm">
										<Image class="h-3 w-3" />
										{post.image_count}
									</div>
								{/if}
							</div>
						{/if}

						<Card.Content class="p-4">
							<Card.Title class="mb-2 line-clamp-2 text-lg transition-colors group-hover:text-primary">
								{post.title}
							</Card.Title>

							<div class="flex flex-wrap items-center gap-2 text-sm text-muted-foreground">
								<Badge variant="secondary" class="font-medium">
									{post.site_name}
								</Badge>
								{#if post.created_at}
									<span class="text-xs">{new Date(post.created_at).toLocaleDateString('ko-KR')}</span>
								{/if}
							</div>
						</Card.Content>
					</Card.Root>
				</a>

				<!-- 피드 내 광고 (N개마다) -->
				{#if (index + 1) % AD_RULES.feedInterval === 0 && index < filteredPosts.length - 1}
					<div class="col-span-full flex justify-center py-6">
						{#if AD_CONFIG.adsense.enabled}
							<AdSense slot={AD_CONFIG.adsense.slots.inFeed} format="auto" />
						{:else if AD_CONFIG.adpost.enabled}
							<AdPost unitId={AD_CONFIG.adpost.units.inFeed} width={728} height={90} />
						{:else if AD_CONFIG.adfit.enabled}
							<AdFit unit={AD_CONFIG.adfit.units.mediumRectangle} width={300} height={250} />
						{/if}
					</div>
				{/if}
			{/each}
		</div>

	<!-- 페이지네이션 -->
	{#if data.pagination.totalPages > 1}
		<div class="mt-8 flex justify-center gap-2">
			<!-- 이전 페이지 -->
			{#if data.pagination.hasPrev}
				<Button 
					href="/?page={data.pagination.page - 1}" 
					variant="outline"
					size="sm"
				>
					이전
				</Button>
			{/if}

			<!-- 페이지 번호들 -->
			{#each Array.from({ length: Math.min(5, data.pagination.totalPages) }, (_, i) => {
				const totalPages = data.pagination.totalPages;
				const currentPage = data.pagination.page;
				let startPage = Math.max(1, currentPage - 2);
				let endPage = Math.min(totalPages, startPage + 4);
				
				if (endPage - startPage < 4) {
					startPage = Math.max(1, endPage - 4);
				}
				
				return startPage + i;
			}) as pageNum}
				{#if pageNum <= data.pagination.totalPages}
					<Button
						href="/?page={pageNum}"
						variant={pageNum === data.pagination.page ? "default" : "outline"}
						size="sm"
					>
						{pageNum}
					</Button>
				{/if}
			{/each}

			<!-- 다음 페이지 -->
			{#if data.pagination.hasNext}
				<Button 
					href="/?page={data.pagination.page + 1}" 
					variant="outline"
					size="sm"
				>
					다음
				</Button>
			{/if}
		</div>
	{/if}
{/if}
</div>
```
