<script lang="ts">
	import type { PageData } from './$types'
	import * as Card from '$lib/components/ui/card'
	import { Badge } from '$lib/components/ui/badge'
	import { MessageSquare, ThumbsUp, Bookmark } from '@lucide/svelte'

	let { data }: { data: PageData } = $props()
	let { stats, recentComments, likedPosts, bookmarkedPosts } = $derived(data)
</script>

<svelte:head>
	<title>내 활동 - 유머 게시판</title>
</svelte:head>

<div class="space-y-6">
	<div>
		<h1 class="text-3xl font-bold tracking-tight">내 활동</h1>
		<p class="text-muted-foreground">내 댓글, 좋아요, 북마크를 확인하세요</p>
	</div>

	<!-- 통계 카드 -->
	<div class="grid gap-4 md:grid-cols-3">
		<Card.Root>
			<Card.Header class="flex flex-row items-center justify-between space-y-0 pb-2">
				<Card.Title class="text-sm font-medium">작성한 댓글</Card.Title>
				<MessageSquare class="h-4 w-4 text-muted-foreground" />
			</Card.Header>
			<Card.Content>
				<div class="text-2xl font-bold">{stats.totalComments}</div>
			</Card.Content>
		</Card.Root>

		<Card.Root>
			<Card.Header class="flex flex-row items-center justify-between space-y-0 pb-2">
				<Card.Title class="text-sm font-medium">좋아요한 게시글</Card.Title>
				<ThumbsUp class="h-4 w-4 text-muted-foreground" />
			</Card.Header>
			<Card.Content>
				<div class="text-2xl font-bold">{stats.totalLikes}</div>
			</Card.Content>
		</Card.Root>

		<Card.Root>
			<Card.Header class="flex flex-row items-center justify-between space-y-0 pb-2">
				<Card.Title class="text-sm font-medium">북마크</Card.Title>
				<Bookmark class="h-4 w-4 text-muted-foreground" />
			</Card.Header>
			<Card.Content>
				<div class="text-2xl font-bold">{stats.totalBookmarks}</div>
			</Card.Content>
		</Card.Root>
	</div>

	<div class="grid gap-4 md:grid-cols-2">
		<!-- 최근 댓글 -->
		<Card.Root>
			<Card.Header>
				<Card.Title>최근 댓글</Card.Title>
			</Card.Header>
			<Card.Content>
				{#if recentComments.length > 0}
					<div class="space-y-4">
						{#each recentComments as comment}
							<div class="space-y-1">
								<a 
									href="/post/{comment.post_id}" 
									class="text-sm font-medium hover:underline"
								>
									{comment.post_title}
								</a>
								<p class="line-clamp-2 text-sm text-muted-foreground">
									{comment.content}
								</p>
								<p class="text-xs text-muted-foreground">
									{comment.created_at ? new Date(comment.created_at).toLocaleString('ko-KR') : 'N/A'}
								</p>
							</div>
						{/each}
					</div>
				{:else}
					<p class="text-sm text-muted-foreground">작성한 댓글이 없습니다.</p>
				{/if}
			</Card.Content>
		</Card.Root>

		<!-- 좋아요한 게시글 -->
		<Card.Root>
			<Card.Header>
				<Card.Title>좋아요한 게시글</Card.Title>
			</Card.Header>
			<Card.Content>
				{#if likedPosts.length > 0}
					<div class="space-y-4">
						{#each likedPosts as post}
							<div class="space-y-1">
								<a 
									href="/post/{post.id}" 
									class="line-clamp-1 text-sm font-medium hover:underline"
								>
									{post.title}
								</a>
								<div class="flex items-center gap-2 text-xs text-muted-foreground">
									<Badge variant="secondary" class="text-xs">
										{post.site_name}
									</Badge>
									<span>{post.liked_at ? new Date(post.liked_at).toLocaleDateString('ko-KR') : 'N/A'}</span>
								</div>
							</div>
						{/each}
					</div>
				{:else}
					<p class="text-sm text-muted-foreground">좋아요한 게시글이 없습니다.</p>
				{/if}
			</Card.Content>
		</Card.Root>

		<!-- 북마크한 게시글 -->
		<Card.Root class="md:col-span-2">
			<Card.Header>
				<Card.Title>북마크한 게시글</Card.Title>
			</Card.Header>
			<Card.Content>
				{#if bookmarkedPosts.length > 0}
					<div class="grid gap-4 md:grid-cols-2">
						{#each bookmarkedPosts as post}
							<div class="space-y-1">
								<a 
									href="/post/{post.id}" 
									class="line-clamp-1 text-sm font-medium hover:underline"
								>
									{post.title}
								</a>
								<div class="flex items-center gap-2 text-xs text-muted-foreground">
									<Badge variant="secondary" class="text-xs">
										{post.site_name}
									</Badge>
									<span>{post.bookmarked_at ? new Date(post.bookmarked_at).toLocaleDateString('ko-KR') : 'N/A'}</span>
								</div>
							</div>
						{/each}
					</div>
				{:else}
					<p class="text-sm text-muted-foreground">북마크한 게시글이 없습니다.</p>
				{/if}
			</Card.Content>
		</Card.Root>
	</div>
</div>
