<script lang="ts">
	import type { PageData } from './$types'
	import * as Card from '$lib/components/ui/card'
	import { Badge } from '$lib/components/ui/badge'
	import AdSense from '$lib/components/ads/AdSense.svelte'
	import AdPost from '$lib/components/ads/AdPost.svelte'
	import { AD_CONFIG, AD_RULES } from '$lib/config/ads'

	let { data }: { data: PageData } = $props()
</script>

<svelte:head>
	<title>유머 게시판 - 재미있는 유머, 웃긴 글 모음</title>
	<meta
		name="description"
		content="FMKorea, 루리웹 등에서 엄선한 재미있는 유머와 웃긴 글을 한곳에서 만나보세요. 매일 업데이트되는 최신 유머 게시글."
	/>
	<meta name="keywords" content="유머, 웃긴글, 재미, 커뮤니티, FMKorea, 루리웹, 베스트글" />

	<!-- Open Graph -->
	<meta property="og:title" content="유머 게시판 - 재미있는 유머, 웃긴 글 모음" />
	<meta
		property="og:description"
		content="FMKorea, 루리웹 등에서 엄선한 재미있는 유머와 웃긴 글을 한곳에서 만나보세요."
	/>
	<meta property="og:type" content="website" />
	<meta property="og:url" content="https://yourdomain.com/" />
	<meta property="og:image" content="https://yourdomain.com/og-image.png" />

	<!-- Twitter Card -->
	<meta name="twitter:card" content="summary_large_image" />
	<meta name="twitter:title" content="유머 게시판 - 재미있는 유머, 웃긴 글 모음" />
	<meta
		name="twitter:description"
		content="FMKorea, 루리웹 등에서 엄선한 재미있는 유머와 웃긴 글을 한곳에서 만나보세요."
	/>
	<meta name="twitter:image" content="https://yourdomain.com/og-image.png" />

	<!-- 추가 SEO -->
	<link rel="canonical" href="https://yourdomain.com/" />
</svelte:head>

<div class="space-y-6">
	<h1 class="text-3xl font-bold">최신 게시글</h1>

	{#if data.posts.length === 0}
		<Card.Root>
			<Card.Content class="p-8 text-center">
				<p class="text-muted-foreground">아직 크롤링된 게시글이 없습니다.</p>
			</Card.Content>
		</Card.Root>
	{:else}
		<div class="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
			{#each data.posts as post, index}
				<!-- 게시글 카드 -->
				<a href="/post/{post.id}" class="group">
					<Card.Root class="overflow-hidden transition-shadow hover:shadow-lg">
						{#if post.thumbnail}
							<div class="aspect-video overflow-hidden bg-muted">
								<img
									src={post.thumbnail}
									alt={post.title}
									class="h-full w-full object-cover transition-transform group-hover:scale-105"
								/>
							</div>
						{/if}

						<Card.Content class="p-4">
							<Card.Title class="mb-2 line-clamp-2 text-lg group-hover:text-primary">
								{post.title}
							</Card.Title>

							<div class="flex flex-wrap items-center gap-2 text-sm text-muted-foreground">
								<Badge variant="secondary">
									{post.site_name}
								</Badge>
								{#if post.created_at}
									<span>{new Date(post.created_at).toLocaleDateString('ko-KR')}</span>
								{/if}
								{#if post.image_count > 0}
									<span>🖼️ {post.image_count}</span>
								{/if}
							</div>
						</Card.Content>
					</Card.Root>
				</a>

				<!-- 피드 내 광고 (N개마다) -->
				{#if (index + 1) % AD_RULES.feedInterval === 0 && index < data.posts.length - 1}
					<div class="col-span-full">
						{#if AD_CONFIG.adsense.enabled}
							<AdSense slot={AD_CONFIG.adsense.slots.inFeed} format="auto" />
						{:else if AD_CONFIG.adpost.enabled}
							<AdPost unitId={AD_CONFIG.adpost.units.inFeed} width={728} height={90} />
						{/if}
					</div>
				{/if}
			{/each}
		</div>
	{/if}
</div>

