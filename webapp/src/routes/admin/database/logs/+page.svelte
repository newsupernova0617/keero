<script lang="ts">
	import type { PageData } from './$types'
	import * as Card from '$lib/components/ui/card'
	import * as Table from '$lib/components/ui/table'
	import { Button } from '$lib/components/ui/button'
	import { Badge } from '$lib/components/ui/badge'
	import { Input } from '$lib/components/ui/input'
	import { FileSearch, Filter, ChevronLeft, ChevronRight } from '@lucide/svelte'
	import { goto } from '$app/navigation'
	import { page } from '$app/stores'

	let { data }: { data: PageData } = $props()

	let selectedAction = $state(data.filters.action)
	let selectedTable = $state(data.filters.tableName)

	function applyFilters() {
		const params = new URLSearchParams()
		if (selectedAction) params.set('action', selectedAction)
		if (selectedTable) params.set('table', selectedTable)
		params.set('page', '1')
		goto(`?${params.toString()}`)
	}

	function clearFilters() {
		selectedAction = ''
		selectedTable = ''
		goto('/admin/database/logs')
	}

	function goToPage(pageNum: number) {
		const params = new URLSearchParams($page.url.searchParams)
		params.set('page', String(pageNum))
		goto(`?${params.toString()}`)
	}

	function getActionBadgeVariant(action: string) {
		switch (action.toLowerCase()) {
			case 'create':
				return 'default'
			case 'update':
				return 'secondary'
			case 'delete':
				return 'destructive'
			case 'query':
				return 'outline'
			default:
				return 'secondary'
		}
	}

	function formatDate(dateStr: string): string {
		return new Date(dateStr).toLocaleString('ko-KR', {
			year: 'numeric',
			month: '2-digit',
			day: '2-digit',
			hour: '2-digit',
			minute: '2-digit',
			second: '2-digit'
		})
	}

	function truncate(str: string | null, maxLength: number): string {
		if (!str) return '-'
		if (str.length <= maxLength) return str
		return str.substring(0, maxLength) + '...'
	}
</script>

<svelte:head>
	<title>감사 로그 - Admin</title>
</svelte:head>

<div class="space-y-6">
	<div>
		<h1 class="text-3xl font-bold tracking-tight flex items-center gap-2">
			<FileSearch class="h-8 w-8" />
			감사 로그
		</h1>
		<p class="text-muted-foreground">데이터베이스 변경 이력 조회</p>
	</div>

	<!-- 필터 -->
	<Card.Root>
		<Card.Header>
			<div class="flex items-center justify-between">
				<div>
					<Card.Title>필터</Card.Title>
					<Card.Description>로그를 필터링하여 조회</Card.Description>
				</div>
				{#if selectedAction || selectedTable}
					<Button variant="outline" size="sm" onclick={clearFilters}>
						필터 초기화
					</Button>
				{/if}
			</div>
		</Card.Header>
		<Card.Content>
			<div class="grid gap-4 md:grid-cols-3">
				<div class="space-y-2">
					<label for="action" class="text-sm font-medium">액션</label>
					<select
						id="action"
						bind:value={selectedAction}
						class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
					>
						<option value="">전체</option>
						{#each data.actions as action}
							<option value={action}>{action}</option>
						{/each}
					</select>
				</div>

				<div class="space-y-2">
					<label for="table" class="text-sm font-medium">테이블</label>
					<select
						id="table"
						bind:value={selectedTable}
						class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
					>
						<option value="">전체</option>
						{#each data.tables as table}
							<option value={table}>{table}</option>
						{/each}
					</select>
				</div>

				<div class="space-y-2">
					<label class="text-sm font-medium">&nbsp;</label>
					<Button onclick={applyFilters} class="w-full">
						<Filter class="h-4 w-4 mr-2" />
						필터 적용
					</Button>
				</div>
			</div>
		</Card.Content>
	</Card.Root>

	<!-- 로그 테이블 -->
	<Card.Root>
		<Card.Header>
			<Card.Title>로그 목록</Card.Title>
			<Card.Description>
				총 {data.pagination.totalCount.toLocaleString()}개 · 페이지 {data.pagination.page} / {data.pagination.totalPages}
			</Card.Description>
		</Card.Header>
		<Card.Content>
			{#if data.logs.length === 0}
				<div class="text-center py-8 text-muted-foreground">
					<FileSearch class="h-12 w-12 mx-auto mb-4 opacity-50" />
					<p>로그가 없습니다</p>
				</div>
			{:else}
				<div class="rounded-md border overflow-x-auto">
					<Table.Root>
						<Table.Header>
							<Table.Row>
								<Table.Head class="w-20">ID</Table.Head>
								<Table.Head>액션</Table.Head>
								<Table.Head>테이블</Table.Head>
								<Table.Head>레코드 ID</Table.Head>
								<Table.Head>사용자</Table.Head>
								<Table.Head>변경 내용</Table.Head>
								<Table.Head>시간</Table.Head>
							</Table.Row>
						</Table.Header>
						<Table.Body>
							{#each data.logs as log}
								<Table.Row>
									<Table.Cell class="font-mono text-sm">{log.id}</Table.Cell>
									<Table.Cell>
										<Badge variant={getActionBadgeVariant(log.action)}>
											{log.action}
										</Badge>
									</Table.Cell>
									<Table.Cell>
										<Badge variant="outline">{log.tableName}</Badge>
									</Table.Cell>
									<Table.Cell class="font-mono text-sm">
										{log.recordId || '-'}
									</Table.Cell>
									<Table.Cell>
										{#if log.user_name}
											<div class="text-sm">
												<div class="font-medium">{log.user_name}</div>
												<div class="text-muted-foreground text-xs">{log.user_email}</div>
											</div>
										{:else}
											<span class="text-muted-foreground">시스템</span>
										{/if}
									</Table.Cell>
									<Table.Cell>
										{#if log.query}
											<code class="text-xs">{truncate(log.query, 50)}</code>
										{:else if log.newValue}
											<div class="text-xs space-y-1">
												{#if log.oldValue}
													<div class="text-muted-foreground">
														이전: {truncate(log.oldValue, 30)}
													</div>
												{/if}
												<div>새값: {truncate(log.newValue, 30)}</div>
											</div>
										{:else}
											<span class="text-muted-foreground">-</span>
										{/if}
									</Table.Cell>
									<Table.Cell class="text-sm whitespace-nowrap">
										{formatDate(log.createdAt)}
									</Table.Cell>
								</Table.Row>
							{/each}
						</Table.Body>
					</Table.Root>
				</div>

				<!-- 페이지네이션 -->
				{#if data.pagination.totalPages > 1}
					<div class="flex items-center justify-between mt-4">
						<div class="text-sm text-muted-foreground">
							{(data.pagination.page - 1) * data.pagination.pageSize + 1}-{Math.min(
								data.pagination.page * data.pagination.pageSize,
								data.pagination.totalCount
							)} / {data.pagination.totalCount}
						</div>
						<div class="flex items-center gap-2">
							<Button
								variant="outline"
								size="sm"
								disabled={data.pagination.page === 1}
								onclick={() => goToPage(data.pagination.page - 1)}
							>
								<ChevronLeft class="h-4 w-4" />
								이전
							</Button>
							<div class="flex items-center gap-1">
								{#each Array(Math.min(5, data.pagination.totalPages)) as _, i}
									{@const pageNum = Math.max(
										1,
										Math.min(
											data.pagination.totalPages - 4,
											data.pagination.page - 2
										)
									) + i}
									{#if pageNum <= data.pagination.totalPages}
										<Button
											variant={data.pagination.page === pageNum ? 'default' : 'outline'}
											size="sm"
											onclick={() => goToPage(pageNum)}
										>
											{pageNum}
										</Button>
									{/if}
								{/each}
							</div>
							<Button
								variant="outline"
								size="sm"
								disabled={data.pagination.page === data.pagination.totalPages}
								onclick={() => goToPage(data.pagination.page + 1)}
							>
								다음
								<ChevronRight class="h-4 w-4" />
							</Button>
						</div>
					</div>
				{/if}
			{/if}
		</Card.Content>
	</Card.Root>
</div>
