<script lang="ts">
	import type { PageData } from './$types'
	import * as Card from '$lib/components/ui/card'
	import { Badge } from '$lib/components/ui/badge'
	import { FileText, MessageSquare, Users, ThumbsUp, Bookmark, TrendingUp } from '@lucide/svelte'

	let { data }: { data: PageData } = $props()
</script>

<svelte:head>
	<title>통계 - 관리자</title>
</svelte:head>

<div class="space-y-6">
	<div>
		<h1 class="text-3xl font-bold tracking-tight">통계</h1>
		<p class="text-muted-foreground">시스템 전체 통계 및 분석</p>
	</div>

	<!-- 전체 통계 -->
	<div class="grid gap-4 md:grid-cols-5">
		<Card.Root>
			<Card.Header class="flex flex-row items-center justify-between space-y-0 pb-2">
				<Card.Title class="text-sm font-medium">게시글</Card.Title>
				<FileText class="h-4 w-4 text-muted-foreground" />
			</Card.Header>
			<Card.Content>
				<div class="text-2xl font-bold">{data.totalStats.totalPosts.toLocaleString()}</div>
			</Card.Content>
		</Card.Root>

		<Card.Root>
			<Card.Header class="flex flex-row items-center justify-between space-y-0 pb-2">
				<Card.Title class="text-sm font-medium">댓글</Card.Title>
				<MessageSquare class="h-4 w-4 text-muted-foreground" />
			</Card.Header>
			<Card.Content>
				<div class="text-2xl font-bold">{data.totalStats.totalComments.toLocaleString()}</div>
			</Card.Content>
		</Card.Root>

		<Card.Root>
			<Card.Header class="flex flex-row items-center justify-between space-y-0 pb-2">
				<Card.Title class="text-sm font-medium">사용자</Card.Title>
				<Users class="h-4 w-4 text-muted-foreground" />
			</Card.Header>
			<Card.Content>
				<div class="text-2xl font-bold">{data.totalStats.totalUsers.toLocaleString()}</div>
			</Card.Content>
		</Card.Root>

		<Card.Root>
			<Card.Header class="flex flex-row items-center justify-between space-y-0 pb-2">
				<Card.Title class="text-sm font-medium">좋아요</Card.Title>
				<ThumbsUp class="h-4 w-4 text-muted-foreground" />
			</Card.Header>
			<Card.Content>
				<div class="text-2xl font-bold">{data.totalStats.totalLikes.toLocaleString()}</div>
			</Card.Content>
		</Card.Root>

		<Card.Root>
			<Card.Header class="flex flex-row items-center justify-between space-y-0 pb-2">
				<Card.Title class="text-sm font-medium">북마크</Card.Title>
				<Bookmark class="h-4 w-4 text-muted-foreground" />
			</Card.Header>
			<Card.Content>
				<div class="text-2xl font-bold">{data.totalStats.totalBookmarks.toLocaleString()}</div>
			</Card.Content>
		</Card.Root>
	</div>

	<div class="grid gap-4 md:grid-cols-2">
		<!-- 사이트별 게시글 -->
		<Card.Root>
			<Card.Header>
				<Card.Title>사이트별 게시글</Card.Title>
			</Card.Header>
			<Card.Content>
				<div class="space-y-2">
					{#each data.postsBySite as site}
						<div class="flex items-center justify-between">
							<Badge variant="secondary">{site.site_name}</Badge>
							<span class="text-sm font-medium">{site.count.toLocaleString()}</span>
						</div>
					{/each}
				</div>
			</Card.Content>
		</Card.Root>

		<!-- 최근 7일 활동 -->
		<Card.Root>
			<Card.Header>
				<Card.Title>최근 7일 활동</Card.Title>
			</Card.Header>
			<Card.Content>
				<div class="space-y-3">
					<div>
						<p class="text-sm font-medium text-muted-foreground mb-2">게시글</p>
						<div class="space-y-1">
							{#each data.recentPosts as day}
								<div class="flex items-center justify-between text-sm">
									<span>{day.date}</span>
									<span class="font-medium">{day.count}개</span>
								</div>
							{/each}
						</div>
					</div>
					<div>
						<p class="text-sm font-medium text-muted-foreground mb-2">댓글</p>
						<div class="space-y-1">
							{#each data.recentComments as day}
								<div class="flex items-center justify-between text-sm">
									<span>{day.date}</span>
									<span class="font-medium">{day.count}개</span>
								</div>
							{/each}
						</div>
					</div>
				</div>
			</Card.Content>
		</Card.Root>

		<!-- 가장 활동적인 사용자 -->
		<Card.Root>
			<Card.Header>
				<Card.Title>활동적인 사용자 (댓글 기준)</Card.Title>
			</Card.Header>
			<Card.Content>
				<div class="space-y-2">
					{#each data.mostActiveUsers as user, i}
						<div class="flex items-center justify-between">
							<div class="flex items-center gap-2">
								<Badge variant={i < 3 ? 'default' : 'secondary'} class="w-6 h-6 flex items-center justify-center p-0">
									{i + 1}
								</Badge>
								<span class="text-sm">{user.display_name || user.email}</span>
							</div>
							<span class="text-sm font-medium">{user.comment_count}개</span>
						</div>
					{/each}
				</div>
			</Card.Content>
		</Card.Root>

		<!-- 인기 게시글 (좋아요) -->
		<Card.Root>
			<Card.Header>
				<Card.Title>인기 게시글 (좋아요)</Card.Title>
			</Card.Header>
			<Card.Content>
				<div class="space-y-2">
					{#each data.topPostsByLikes as post}
						<div class="space-y-1">
							<a 
								href="/post/{post.post_id}" 
								class="text-sm hover:underline line-clamp-1 block"
							>
								{post.title}
							</a>
							<div class="flex items-center gap-2">
								<Badge variant="secondary" class="text-xs">{post.site_name}</Badge>
								<span class="text-xs text-muted-foreground">❤️ {post.like_count}</span>
							</div>
						</div>
					{/each}
				</div>
			</Card.Content>
		</Card.Root>
	</div>

	<!-- 많은 댓글이 달린 게시글 -->
	<Card.Root>
		<Card.Header>
			<Card.Title>댓글이 많은 게시글</Card.Title>
		</Card.Header>
		<Card.Content>
			<div class="grid gap-4 md:grid-cols-2">
				{#each data.topPostsByComments as post}
					<div class="space-y-1">
						<a 
							href="/post/{post.post_id}" 
							class="text-sm hover:underline line-clamp-2 block"
						>
							{post.title}
						</a>
						<div class="flex items-center gap-2">
							<Badge variant="secondary" class="text-xs">{post.site_name}</Badge>
							<span class="text-xs text-muted-foreground">💬 {post.comment_count}</span>
						</div>
					</div>
				{/each}
			</div>
		</Card.Content>
	</Card.Root>
</div>
