<script lang="ts">
	import type { PageData } from './$types'
	import * as Card from '$lib/components/ui/card'
	import { Badge } from '$lib/components/ui/badge'
	import { Button } from '$lib/components/ui/button'
	import { FileText, MessageSquare, Users, TrendingUp, Database } from '@lucide/svelte'

	let { data }: { data: PageData } = $props()
	let { stats, recentPosts, recentComments } = $derived(data)
</script>

<svelte:head>
	<title>관리자 대시보드</title>
</svelte:head>

<div class="space-y-6">
	<div>
		<h1 class="text-3xl font-bold tracking-tight">관리자 대시보드</h1>
		<p class="text-muted-foreground">시스템 통계 및 최근 활동을 확인하세요</p>
	</div>

	<!-- 통계 카드 -->
	<div class="grid gap-4 md:grid-cols-3">
		<Card.Root>
			<Card.Header class="flex flex-row items-center justify-between space-y-0 pb-2">
				<Card.Title class="text-sm font-medium">전체 게시글</Card.Title>
				<FileText class="h-4 w-4 text-muted-foreground" />
			</Card.Header>
			<Card.Content>
				<div class="text-2xl font-bold">{stats.totalPosts.toLocaleString()}</div>
				<p class="text-xs text-muted-foreground">크롤링된 게시글</p>
			</Card.Content>
		</Card.Root>

		<Card.Root>
			<Card.Header class="flex flex-row items-center justify-between space-y-0 pb-2">
				<Card.Title class="text-sm font-medium">전체 댓글</Card.Title>
				<MessageSquare class="h-4 w-4 text-muted-foreground" />
			</Card.Header>
			<Card.Content>
				<div class="text-2xl font-bold">{stats.totalComments.toLocaleString()}</div>
				<p class="text-xs text-muted-foreground">사용자 댓글</p>
			</Card.Content>
		</Card.Root>

		<Card.Root>
			<Card.Header class="flex flex-row items-center justify-between space-y-0 pb-2">
				<Card.Title class="text-sm font-medium">전체 사용자</Card.Title>
				<Users class="h-4 w-4 text-muted-foreground" />
			</Card.Header>
			<Card.Content>
				<div class="text-2xl font-bold">{stats.totalUsers.toLocaleString()}</div>
				<p class="text-xs text-muted-foreground">가입한 사용자</p>
			</Card.Content>
		</Card.Root>
	</div>

	<div class="grid gap-4 md:grid-cols-2">
		<!-- 최근 게시글 -->
		<Card.Root>
			<Card.Header>
				<Card.Title>최근 게시글</Card.Title>
				<Card.Description>최근 크롤링된 게시글 5개</Card.Description>
			</Card.Header>
			<Card.Content>
				<div class="space-y-4">
					{#each recentPosts as post}
						<div class="flex items-start justify-between gap-4">
							<div class="flex-1 space-y-1">
								<a 
									href="/post/{post.id}" 
									class="line-clamp-1 font-medium hover:underline"
								>
									{post.title}
								</a>
								<div class="flex items-center gap-2 text-xs text-muted-foreground">
									<Badge variant="secondary" class="text-xs">
										{post.site_name}
									</Badge>
									<span>{new Date(post.created_at).toLocaleDateString('ko-KR')}</span>
								</div>
							</div>
						</div>
					{/each}
				</div>
			</Card.Content>
			<Card.Footer>
				<Button href="/admin/posts" variant="outline" class="w-full">
					모든 게시글 보기
				</Button>
			</Card.Footer>
		</Card.Root>

		<!-- 최근 댓글 -->
		<Card.Root>
			<Card.Header>
				<Card.Title>최근 댓글</Card.Title>
				<Card.Description>최근 작성된 댓글 5개</Card.Description>
			</Card.Header>
			<Card.Content>
				<div class="space-y-4">
					{#each recentComments as comment}
						<div class="space-y-1">
							<div class="flex items-center gap-2">
								<span class="text-sm font-medium">{comment.user_display_name}</span>
								<span class="text-xs text-muted-foreground">
									{comment.created_at ? new Date(comment.created_at).toLocaleDateString('ko-KR') : 'N/A'}
								</span>
							</div>
							<a 
								href="/post/{comment.post_id}" 
								class="line-clamp-2 text-sm text-muted-foreground hover:underline"
							>
								{comment.content}
							</a>
						</div>
					{/each}
				</div>
			</Card.Content>
			<Card.Footer>
				<Button href="/admin/comments" variant="outline" class="w-full">
					모든 댓글 보기
				</Button>
			</Card.Footer>
		</Card.Root>
	</div>

	<!-- 빠른 액션 -->
	<Card.Root>
		<Card.Header>
			<Card.Title>빠른 액션</Card.Title>
			<Card.Description>자주 사용하는 관리 기능</Card.Description>
		</Card.Header>
		<Card.Content>
			<div class="grid gap-4 md:grid-cols-5">
				<Button href="/admin/posts" variant="outline" class="h-auto flex-col gap-2 py-4">
					<FileText class="h-6 w-6" />
					게시글 관리
				</Button>
				<Button href="/admin/comments" variant="outline" class="h-auto flex-col gap-2 py-4">
					<MessageSquare class="h-6 w-6" />
					댓글 관리
				</Button>
				<Button href="/admin/users" variant="outline" class="h-auto flex-col gap-2 py-4">
					<Users class="h-6 w-6" />
					사용자 관리
				</Button>
				<Button href="/admin/database" variant="outline" class="h-auto flex-col gap-2 py-4">
					<Database class="h-6 w-6" />
					DB 관리
				</Button>
				<Button href="/admin/stats" variant="outline" class="h-auto flex-col gap-2 py-4">
					<TrendingUp class="h-6 w-6" />
					통계 보기
				</Button>
			</div>
		</Card.Content>
	</Card.Root>
</div>
