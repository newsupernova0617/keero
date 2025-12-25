<script lang="ts">
	import type { PageData } from './$types'
	import { enhance } from '$app/forms'
	import * as Card from '$lib/components/ui/card'
	import { Button } from '$lib/components/ui/button'
	import { Badge } from '$lib/components/ui/badge'
	import * as Tabs from '$lib/components/ui/tabs'
	import { Flag, CheckCircle, XCircle, Trash2 } from '@lucide/svelte'

	let { data }: { data: PageData } = $props()

	const reasonLabels: Record<string, string> = {
		spam: '스팸',
		inappropriate: '부적절한 콘텐츠',
		harassment: '괴롭힘',
		misinformation: '허위 정보',
		other: '기타'
	}

	function getStatusBadge(status: string | null) {
		if (!status) {
			return { variant: 'secondary' as const, label: '알 수 없음' }
		}
		switch (status) {
			case 'pending':
				return { variant: 'default' as const, label: '대기중' }
			case 'resolved':
				return { variant: 'secondary' as const, label: '해결됨' }
			case 'rejected':
				return { variant: 'outline' as const, label: '거부됨' }
			default:
				return { variant: 'secondary' as const, label: status }
		}
	}

	const pendingReports = $derived(data.reports.filter(r => r.status === 'pending'))
	const resolvedReports = $derived(data.reports.filter(r => r.status === 'resolved'))
	const rejectedReports = $derived(data.reports.filter(r => r.status === 'rejected'))
</script>

<svelte:head>
	<title>신고 관리 - 관리자</title>
</svelte:head>

<div class="space-y-6">
	<div>
		<h1 class="text-3xl font-bold tracking-tight">신고 관리</h1>
		<p class="text-muted-foreground">사용자가 제출한 신고를 관리합니다</p>
	</div>

	<Tabs.Root value="pending" class="w-full">
		<Tabs.List class="grid w-full grid-cols-3">
			<Tabs.Trigger value="pending">
				대기중 ({pendingReports.length})
			</Tabs.Trigger>
			<Tabs.Trigger value="resolved">
				해결됨 ({resolvedReports.length})
			</Tabs.Trigger>
			<Tabs.Trigger value="rejected">
				거부됨 ({rejectedReports.length})
			</Tabs.Trigger>
		</Tabs.List>

		<Tabs.Content value="pending" class="space-y-4">
			{#each pendingReports as report}
				<Card.Root>
					<Card.Header>
						<div class="flex items-start justify-between">
							<div class="space-y-1">
								<Card.Title class="flex items-center gap-2">
									<Flag class="h-4 w-4" />
									신고 #{report.id}
								</Card.Title>
								<Card.Description>
									{report.reporter_display_name || report.reporter_email}이(가) 
									{report.created_at ? new Date(report.created_at).toLocaleDateString('ko-KR') : 'N/A'}에 신고
								</Card.Description>
							</div>
							<Badge {...getStatusBadge(report.status)}>{getStatusBadge(report.status).label}</Badge>
						</div>
					</Card.Header>
					<Card.Content class="space-y-4">
						<div>
							<p class="text-sm font-medium">신고 사유</p>
							<Badge variant="secondary" class="mt-1">{reasonLabels[report.reason] || report.reason}</Badge>
							{#if report.description}
								<p class="mt-2 text-sm text-muted-foreground">{report.description}</p>
							{/if}
						</div>

						<div>
							<p class="text-sm font-medium mb-2">신고 대상</p>
							{#if report.post_id}
								<a 
									href="/post/{report.post_id}" 
									target="_blank"
									class="text-sm text-primary hover:underline"
								>
									📄 게시글: {report.post_title}
								</a>
							{:else if report.comment_id}
								<div class="rounded-lg bg-muted p-3">
									<p class="text-sm">💬 댓글: {report.comment_content}</p>
								</div>
							{/if}
						</div>
					</Card.Content>
					<Card.Footer class="flex gap-2">
						<form method="POST" action="?/resolve" use:enhance class="flex-1">
							<input type="hidden" name="report_id" value={report.id} />
							<Button type="submit" variant="outline" class="w-full">
								<CheckCircle class="mr-2 h-4 w-4" />
								해결됨으로 표시
							</Button>
						</form>
						<form method="POST" action="?/reject" use:enhance class="flex-1">
							<input type="hidden" name="report_id" value={report.id} />
							<Button type="submit" variant="outline" class="w-full">
								<XCircle class="mr-2 h-4 w-4" />
								거부
							</Button>
						</form>
						{#if report.comment_id}
							<form method="POST" action="?/deleteContent" use:enhance>
								<input type="hidden" name="report_id" value={report.id} />
								<Button 
									type="submit" 
									variant="destructive"
									onclick={(e) => { if (!confirm('정말 댓글을 삭제하시겠습니까?')) { e.preventDefault(); } }}
								>
									<Trash2 class="mr-2 h-4 w-4" />
									댓글 삭제
								</Button>
							</form>
						{/if}
					</Card.Footer>
				</Card.Root>
			{:else}
				<Card.Root>
					<Card.Content class="py-12 text-center text-muted-foreground">
						대기 중인 신고가 없습니다.
					</Card.Content>
				</Card.Root>
			{/each}
		</Tabs.Content>

		<Tabs.Content value="resolved" class="space-y-4">
			{#each resolvedReports as report}
				<Card.Root>
					<Card.Header>
						<div class="flex items-start justify-between">
							<div class="space-y-1">
								<Card.Title class="flex items-center gap-2">
									<Flag class="h-4 w-4" />
									신고 #{report.id}
								</Card.Title>
								<Card.Description>
									{reasonLabels[report.reason] || report.reason}
									{#if report.resolved_at}
										· {new Date(report.resolved_at).toLocaleDateString('ko-KR')} 해결됨
									{/if}
								</Card.Description>
							</div>
							<Badge {...getStatusBadge(report.status)}>{getStatusBadge(report.status).label}</Badge>
						</div>
					</Card.Header>
					<Card.Content>
						{#if report.post_id}
							<a href="/post/{report.post_id}" target="_blank" class="text-sm text-primary hover:underline">
								📄 {report.post_title}
							</a>
						{:else if report.comment_id}
							<p class="text-sm text-muted-foreground">💬 {report.comment_content}</p>
						{/if}
					</Card.Content>
				</Card.Root>
			{:else}
				<Card.Root>
					<Card.Content class="py-12 text-center text-muted-foreground">
						해결된 신고가 없습니다.
					</Card.Content>
				</Card.Root>
			{/each}
		</Tabs.Content>

		<Tabs.Content value="rejected" class="space-y-4">
			{#each rejectedReports as report}
				<Card.Root>
					<Card.Header>
						<div class="flex items-start justify-between">
							<div class="space-y-1">
								<Card.Title class="flex items-center gap-2">
									<Flag class="h-4 w-4" />
									신고 #{report.id}
								</Card.Title>
								<Card.Description>
									{reasonLabels[report.reason] || report.reason}
									{#if report.resolved_at}
										· {new Date(report.resolved_at).toLocaleDateString('ko-KR')} 거부됨
									{/if}
								</Card.Description>
							</div>
							<Badge {...getStatusBadge(report.status)}>{getStatusBadge(report.status).label}</Badge>
						</div>
					</Card.Header>
					<Card.Content>
						{#if report.post_id}
							<a href="/post/{report.post_id}" target="_blank" class="text-sm text-primary hover:underline">
								📄 {report.post_title}
							</a>
						{:else if report.comment_id}
							<p class="text-sm text-muted-foreground">💬 {report.comment_content}</p>
						{/if}
					</Card.Content>
				</Card.Root>
			{:else}
				<Card.Root>
					<Card.Content class="py-12 text-center text-muted-foreground">
						거부된 신고가 없습니다.
					</Card.Content>
				</Card.Root>
			{/each}
		</Tabs.Content>
	</Tabs.Root>
</div>
