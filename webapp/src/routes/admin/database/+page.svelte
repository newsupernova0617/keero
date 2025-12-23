<script lang="ts">
	import type { PageData, ActionData } from './$types'
	import * as Card from '$lib/components/ui/card'
	import * as Table from '$lib/components/ui/table'
	import { Badge } from '$lib/components/ui/badge'
	import { Button } from '$lib/components/ui/button'
	import { Database, Trash2, RefreshCw, AlertTriangle } from '@lucide/svelte'
	import { enhance } from '$app/forms'

	let { data, form }: { data: PageData; form: ActionData } = $props()
	let { stats, recentPosts, postsBySite } = $derived(data)

	let isDeleting = $state(false)
	let isCleaning = $state(false)
</script>

<svelte:head>
	<title>데이터베이스 관리 - Admin</title>
</svelte:head>

<div class="space-y-6">
	<div>
		<h1 class="text-3xl font-bold tracking-tight flex items-center gap-2">
			<Database class="h-8 w-8" />
			데이터베이스 관리
		</h1>
		<p class="text-muted-foreground">데이터베이스 통계 및 관리</p>
	</div>

	{#if form?.success}
		<div class="rounded-lg bg-green-50 dark:bg-green-950 p-4 border border-green-200 dark:border-green-800">
			<p class="text-sm text-green-800 dark:text-green-200">{form.message}</p>
		</div>
	{/if}

	<!-- 통계 카드 -->
	<div class="grid gap-4 md:grid-cols-3">
		<Card.Root>
			<Card.Header class="flex flex-row items-center justify-between space-y-0 pb-2">
				<Card.Title class="text-sm font-medium">게시글</Card.Title>
				<Database class="h-4 w-4 text-muted-foreground" />
			</Card.Header>
			<Card.Content>
				<div class="text-2xl font-bold">{stats.posts.total.toLocaleString()}</div>
				<p class="text-xs text-muted-foreground">{stats.posts.sites}개 사이트</p>
			</Card.Content>
		</Card.Root>

		<Card.Root>
			<Card.Header class="flex flex-row items-center justify-between space-y-0 pb-2">
				<Card.Title class="text-sm font-medium">댓글</Card.Title>
				<Database class="h-4 w-4 text-muted-foreground" />
			</Card.Header>
			<Card.Content>
				<div class="text-2xl font-bold">{stats.comments.total.toLocaleString()}</div>
				<p class="text-xs text-muted-foreground">사용자 댓글</p>
			</Card.Content>
		</Card.Root>

		<Card.Root>
			<Card.Header class="flex flex-row items-center justify-between space-y-0 pb-2">
				<Card.Title class="text-sm font-medium">사용자</Card.Title>
				<Database class="h-4 w-4 text-muted-foreground" />
			</Card.Header>
			<Card.Content>
				<div class="text-2xl font-bold">{stats.users.total.toLocaleString()}</div>
				<p class="text-xs text-muted-foreground">가입한 사용자</p>
			</Card.Content>
		</Card.Root>
	</div>

	<!-- 사이트별 게시글 수 -->
	<Card.Root>
		<Card.Header>
			<Card.Title>사이트별 게시글 통계</Card.Title>
			<Card.Description>각 사이트에서 크롤링된 게시글 수</Card.Description>
		</Card.Header>
		<Card.Content>
			<div class="grid gap-4 md:grid-cols-4">
				{#each postsBySite as site}
					<div class="flex items-center justify-between rounded-lg border p-4">
						<div>
							<p class="font-medium">{site.site_name}</p>
							<p class="text-2xl font-bold">{site.count.toLocaleString()}</p>
						</div>
					</div>
				{/each}
			</div>
		</Card.Content>
	</Card.Root>

	<!-- 최근 게시글 -->
	<Card.Root>
		<Card.Header>
			<Card.Title>최근 크롤링된 게시글</Card.Title>
			<Card.Description>최근 20개 게시글</Card.Description>
		</Card.Header>
		<Card.Content>
			<Table.Root>
				<Table.Header>
					<Table.Row>
						<Table.Head>제목</Table.Head>
						<Table.Head>사이트</Table.Head>
						<Table.Head>크롤링 시간</Table.Head>
						<Table.Head class="text-right">액션</Table.Head>
					</Table.Row>
				</Table.Header>
				<Table.Body>
					{#each recentPosts as post}
						<Table.Row>
							<Table.Cell class="font-medium">
								<a href="/post/{post.id}" class="hover:underline line-clamp-1">
									{post.title}
								</a>
							</Table.Cell>
							<Table.Cell>
								<Badge variant="secondary">{post.site_name}</Badge>
							</Table.Cell>
							<Table.Cell class="text-sm text-muted-foreground">
								{post.crawled_at ? new Date(post.crawled_at).toLocaleString('ko-KR') : 'N/A'}
							</Table.Cell>
							<Table.Cell class="text-right">
								<form method="POST" action="?/deletePost" use:enhance={() => {
									isDeleting = true
									return async ({ update }) => {
										await update()
										isDeleting = false
									}
								}}>
									<input type="hidden" name="postId" value={post.id} />
									<Button 
										type="submit" 
										variant="ghost" 
										size="sm"
										disabled={isDeleting}
									>
										<Trash2 class="h-4 w-4 text-destructive" />
									</Button>
								</form>
							</Table.Cell>
						</Table.Row>
					{/each}
				</Table.Body>
			</Table.Root>
		</Card.Content>
	</Card.Root>

	<!-- 데이터 관리 액션 -->
	<Card.Root>
		<Card.Header>
			<Card.Title>데이터 관리</Card.Title>
			<Card.Description>데이터베이스 유지보수 작업</Card.Description>
		</Card.Header>
		<Card.Content>
			<div class="space-y-4">
				<div class="flex items-center justify-between rounded-lg border p-4">
					<div class="space-y-1">
						<p class="font-medium">오래된 게시글 정리</p>
						<p class="text-sm text-muted-foreground">30일 이상 된 게시글을 삭제합니다</p>
					</div>
					<form method="POST" action="?/cleanOldPosts" use:enhance={() => {
						if (!confirm('30일 이상 된 게시글을 모두 삭제하시겠습니까?')) {
							return () => {}
						}
						isCleaning = true
						return async ({ update }) => {
							await update()
							isCleaning = false
						}
					}}>
						<Button type="submit" variant="destructive" disabled={isCleaning}>
							<AlertTriangle class="mr-2 h-4 w-4" />
							{isCleaning ? '정리 중...' : '정리하기'}
						</Button>
					</form>
				</div>

				<div class="flex items-center justify-between rounded-lg border p-4">
					<div class="space-y-1">
						<p class="font-medium">데이터베이스 새로고침</p>
						<p class="text-sm text-muted-foreground">최신 통계로 업데이트합니다</p>
					</div>
					<Button onclick={() => window.location.reload()} variant="outline">
						<RefreshCw class="mr-2 h-4 w-4" />
						새로고침
					</Button>
				</div>
			</div>
		</Card.Content>
	</Card.Root>
</div>
