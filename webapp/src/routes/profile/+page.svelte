<script lang="ts">
	import type { PageData } from './$types'
	import * as Card from '$lib/components/ui/card'
	import { Badge } from '$lib/components/ui/badge'
	import { Button } from '$lib/components/ui/button'
	import * as Avatar from '$lib/components/ui/avatar'
	import { User, Mail, Calendar, Shield } from '@lucide/svelte'

	let { data }: { data: PageData } = $props()

	// 사용자 이름 첫 글자
	let initial = $derived(data.user?.email?.[0]?.toUpperCase() || 'U')
	
	// 가입일 포맷팅
	let joinDate = $derived(
		data.user?.created_at 
			? new Date(data.user.created_at).toLocaleDateString('ko-KR', {
				year: 'numeric',
				month: 'long',
				day: 'numeric'
			})
			: '알 수 없음'
	)
</script>

<svelte:head>
	<title>프로필 - 유머 게시판</title>
	<meta name="description" content="내 프로필 정보" />
</svelte:head>

<div class="mx-auto max-w-4xl space-y-6">
	<!-- Header -->
	<div class="flex items-center justify-between">
		<div>
			<h1 class="text-3xl font-bold tracking-tight">프로필</h1>
			<p class="mt-1 text-sm text-muted-foreground">
				내 계정 정보를 확인하세요
			</p>
		</div>
		<Button href="/settings" variant="outline">
			설정
		</Button>
	</div>

	<!-- Profile Card -->
	<Card.Root>
		<Card.Content class="pt-6">
			<div class="flex flex-col items-center gap-6 sm:flex-row sm:items-start">
				<!-- Avatar -->
				<Avatar.Root class="h-24 w-24">
					<Avatar.Fallback class="bg-primary text-4xl text-primary-foreground">
						{initial}
					</Avatar.Fallback>
				</Avatar.Root>

				<!-- User Info -->
				<div class="flex-1 space-y-4 text-center sm:text-left">
					<div>
						<h2 class="text-2xl font-bold">{data.user?.email?.split('@')[0]}</h2>
						<p class="text-sm text-muted-foreground">회원</p>
					</div>

					<div class="grid gap-3 sm:grid-cols-2">
						<!-- Email -->
						<div class="flex items-center gap-2 rounded-lg border p-3">
							<Mail class="h-4 w-4 text-muted-foreground" />
							<div class="flex-1 overflow-hidden">
								<p class="text-xs text-muted-foreground">이메일</p>
								<p class="truncate text-sm font-medium">{data.user?.email}</p>
							</div>
						</div>

						<!-- Join Date -->
						<div class="flex items-center gap-2 rounded-lg border p-3">
							<Calendar class="h-4 w-4 text-muted-foreground" />
							<div class="flex-1">
								<p class="text-xs text-muted-foreground">가입일</p>
								<p class="text-sm font-medium">{joinDate}</p>
							</div>
						</div>

						<!-- User ID -->
						<div class="flex items-center gap-2 rounded-lg border p-3">
							<User class="h-4 w-4 text-muted-foreground" />
							<div class="flex-1 overflow-hidden">
								<p class="text-xs text-muted-foreground">사용자 ID</p>
								<p class="truncate font-mono text-xs">{data.user?.id}</p>
							</div>
						</div>

						<!-- Role -->
						<div class="flex items-center gap-2 rounded-lg border p-3">
							<Shield class="h-4 w-4 text-muted-foreground" />
							<div class="flex-1">
								<p class="text-xs text-muted-foreground">권한</p>
								<Badge variant="secondary" class="mt-1">일반 사용자</Badge>
							</div>
						</div>
					</div>
				</div>
			</div>
		</Card.Content>
	</Card.Root>

	<!-- Activity Stats (준비 중) -->
	<Card.Root>
		<Card.Header>
			<Card.Title>활동 통계</Card.Title>
			<Card.Description>내 활동 내역을 확인하세요</Card.Description>
		</Card.Header>
		<Card.Content>
			<div class="grid gap-4 sm:grid-cols-3">
				<div class="rounded-lg border p-4 text-center">
					<p class="text-2xl font-bold">0</p>
					<p class="text-sm text-muted-foreground">작성한 댓글</p>
				</div>
				<div class="rounded-lg border p-4 text-center">
					<p class="text-2xl font-bold">0</p>
					<p class="text-sm text-muted-foreground">좋아요한 게시글</p>
				</div>
				<div class="rounded-lg border p-4 text-center">
					<p class="text-2xl font-bold">0</p>
					<p class="text-sm text-muted-foreground">북마크</p>
				</div>
			</div>
		</Card.Content>
	</Card.Root>
</div>
