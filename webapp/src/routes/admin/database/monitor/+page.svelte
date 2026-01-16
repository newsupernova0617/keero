<script lang="ts">
	import type { PageData, ActionData } from './$types'
	import * as Card from '$lib/components/ui/card'
	import * as Table from '$lib/components/ui/table'
	import { Button } from '$lib/components/ui/button'
	import { Badge } from '$lib/components/ui/badge'
	import {
		Activity,
		Database,
		HardDrive,
		Zap,
		BarChart3,
		RefreshCw,
		Settings
	} from '@lucide/svelte'
	import { enhance } from '$app/forms'
	import { invalidateAll } from '$app/navigation'

	let { data, form }: { data: PageData; form: ActionData } = $props()

	let isVacuuming = $state(false)
	let isAnalyzing = $state(false)
	let isOptimizing = $state(false)

	// 테이블 크기 차트용 데이터
	let chartData = $derived(
		data.tableStats
			.filter((t) => t.size > 0)
			.sort((a, b) => b.size - a.size)
			.slice(0, 10)
	)

	function getPercentage(size: number): number {
		const maxSize = Math.max(...chartData.map((t) => t.size))
		return (size / maxSize) * 100
	}
</script>

<svelte:head>
	<title>성능 모니터링 - Admin</title>
</svelte:head>

<div class="space-y-6">
	<div>
		<h1 class="text-3xl font-bold tracking-tight flex items-center gap-2">
			<Activity class="h-8 w-8" />
			성능 모니터링
		</h1>
		<p class="text-muted-foreground">데이터베이스 성능 및 최적화</p>
	</div>

	<!-- Success/Error Messages -->
	{#if form?.success}
		<div
			class="rounded-lg bg-green-50 dark:bg-green-950 p-4 border border-green-200 dark:border-green-800"
		>
			<p class="text-sm text-green-800 dark:text-green-200">{form.message}</p>
		</div>
	{:else if form?.error}
		<div
			class="rounded-lg bg-red-50 dark:bg-red-950 p-4 border border-red-200 dark:border-red-800"
		>
			<p class="text-sm text-red-800 dark:text-red-200">{form.error}</p>
		</div>
	{/if}

	<!-- 전체 통계 -->
	<div class="grid gap-4 md:grid-cols-4">
		<Card.Root>
			<Card.Header class="flex flex-row items-center justify-between space-y-0 pb-2">
				<Card.Title class="text-sm font-medium">DB 크기</Card.Title>
				<HardDrive class="h-4 w-4 text-muted-foreground" />
			</Card.Header>
			<Card.Content>
				<div class="text-2xl font-bold">{data.dbSizeFormatted}</div>
				<p class="text-xs text-muted-foreground">전체 데이터베이스</p>
			</Card.Content>
		</Card.Root>

		<Card.Root>
			<Card.Header class="flex flex-row items-center justify-between space-y-0 pb-2">
				<Card.Title class="text-sm font-medium">테이블 수</Card.Title>
				<Database class="h-4 w-4 text-muted-foreground" />
			</Card.Header>
			<Card.Content>
				<div class="text-2xl font-bold">{data.tableStats.length}</div>
				<p class="text-xs text-muted-foreground">총 테이블</p>
			</Card.Content>
		</Card.Root>

		<Card.Root>
			<Card.Header class="flex flex-row items-center justify-between space-y-0 pb-2">
				<Card.Title class="text-sm font-medium">총 레코드</Card.Title>
				<BarChart3 class="h-4 w-4 text-muted-foreground" />
			</Card.Header>
			<Card.Content>
				<div class="text-2xl font-bold">{data.totalRows.toLocaleString()}</div>
				<p class="text-xs text-muted-foreground">모든 테이블</p>
			</Card.Content>
		</Card.Root>

		<Card.Root>
			<Card.Header class="flex flex-row items-center justify-between space-y-0 pb-2">
				<Card.Title class="text-sm font-medium">인덱스 수</Card.Title>
				<Zap class="h-4 w-4 text-muted-foreground" />
			</Card.Header>
			<Card.Content>
				<div class="text-2xl font-bold">{data.indexes.length}</div>
				<p class="text-xs text-muted-foreground">활성 인덱스</p>
			</Card.Content>
		</Card.Root>
	</div>

	<!-- 테이블별 크기 차트 -->
	<Card.Root>
		<Card.Header>
			<Card.Title>테이블별 크기</Card.Title>
			<Card.Description>상위 10개 테이블</Card.Description>
		</Card.Header>
		<Card.Content>
			<div class="space-y-3">
				{#each chartData as table}
					<div class="space-y-1">
						<div class="flex items-center justify-between text-sm">
							<span class="font-medium">{table.name}</span>
							<div class="flex items-center gap-2">
								<Badge variant="secondary">{table.rowCount.toLocaleString()} rows</Badge>
								<span class="text-muted-foreground">{table.sizeFormatted}</span>
							</div>
						</div>
						<div class="h-2 bg-muted rounded-full overflow-hidden">
							<div
								class="h-full bg-primary transition-all"
								style="width: {getPercentage(table.size)}%"
							></div>
						</div>
					</div>
				{/each}
			</div>
		</Card.Content>
	</Card.Root>

	<!-- 테이블 상세 통계 -->
	<Card.Root>
		<Card.Header>
			<Card.Title>테이블 상세 통계</Card.Title>
			<Card.Description>모든 테이블의 레코드 수 및 크기</Card.Description>
		</Card.Header>
		<Card.Content>
			<div class="rounded-md border">
				<Table.Root>
					<Table.Header>
						<Table.Row>
							<Table.Head>테이블명</Table.Head>
							<Table.Head class="text-right">레코드 수</Table.Head>
							<Table.Head class="text-right">크기</Table.Head>
						</Table.Row>
					</Table.Header>
					<Table.Body>
						{#each data.tableStats.sort((a, b) => b.rowCount - a.rowCount) as table}
							<Table.Row>
								<Table.Cell class="font-mono">{table.name}</Table.Cell>
								<Table.Cell class="text-right">{table.rowCount.toLocaleString()}</Table.Cell>
								<Table.Cell class="text-right">
									<Badge variant="secondary">{table.sizeFormatted}</Badge>
								</Table.Cell>
							</Table.Row>
						{/each}
					</Table.Body>
				</Table.Root>
			</div>
		</Card.Content>
	</Card.Root>

	<!-- 인덱스 정보 -->
	<Card.Root>
		<Card.Header>
			<Card.Title>인덱스 정보</Card.Title>
			<Card.Description>{data.indexes.length}개의 인덱스</Card.Description>
		</Card.Header>
		<Card.Content>
			<div class="rounded-md border">
				<Table.Root>
					<Table.Header>
						<Table.Row>
							<Table.Head>인덱스명</Table.Head>
							<Table.Head>테이블</Table.Head>
						</Table.Row>
					</Table.Header>
					<Table.Body>
						{#each data.indexes as index}
							<Table.Row>
								<Table.Cell class="font-mono text-sm">{index.name}</Table.Cell>
								<Table.Cell>
									<Badge variant="outline">{index.tbl_name}</Badge>
								</Table.Cell>
							</Table.Row>
						{/each}
					</Table.Body>
				</Table.Root>
			</div>
		</Card.Content>
	</Card.Root>

	<!-- PRAGMA 정보 -->
	<Card.Root>
		<Card.Header>
			<Card.Title>데이터베이스 설정</Card.Title>
			<Card.Description>SQLite PRAGMA 정보</Card.Description>
		</Card.Header>
		<Card.Content>
			<div class="grid gap-4 md:grid-cols-2">
				<div class="flex items-center justify-between p-3 rounded-lg border">
					<span class="text-sm font-medium">Page Size</span>
					<Badge variant="secondary">{data.pragmaInfo.pageSize} bytes</Badge>
				</div>
				<div class="flex items-center justify-between p-3 rounded-lg border">
					<span class="text-sm font-medium">Page Count</span>
					<Badge variant="secondary">{data.pragmaInfo.pageCount.toLocaleString()}</Badge>
				</div>
				<div class="flex items-center justify-between p-3 rounded-lg border">
					<span class="text-sm font-medium">Journal Mode</span>
					<Badge variant="secondary">{data.pragmaInfo.journalMode}</Badge>
				</div>
				<div class="flex items-center justify-between p-3 rounded-lg border">
					<span class="text-sm font-medium">Synchronous</span>
					<Badge variant="secondary">{data.pragmaInfo.synchronous}</Badge>
				</div>
			</div>
		</Card.Content>
	</Card.Root>

	<!-- 최적화 도구 -->
	<Card.Root>
		<Card.Header>
			<Card.Title>최적화 도구</Card.Title>
			<Card.Description>데이터베이스 성능 최적화</Card.Description>
		</Card.Header>
		<Card.Content>
			<div class="grid gap-4 md:grid-cols-3">
				<div class="space-y-2">
					<div class="font-medium">VACUUM</div>
					<p class="text-sm text-muted-foreground">
						데이터베이스를 재구성하여 공간을 회수하고 단편화를 제거합니다.
					</p>
					<form
						method="POST"
						action="?/vacuum"
						use:enhance={() => {
							isVacuuming = true
							return async ({ update }) => {
								await update()
								await invalidateAll()
								isVacuuming = false
							}
						}}
					>
						<Button type="submit" variant="outline" class="w-full" disabled={isVacuuming}>
							<RefreshCw class="h-4 w-4 mr-2" />
							{isVacuuming ? '실행 중...' : 'VACUUM 실행'}
						</Button>
					</form>
				</div>

				<div class="space-y-2">
					<div class="font-medium">ANALYZE</div>
					<p class="text-sm text-muted-foreground">
						쿼리 최적화를 위한 통계 정보를 수집합니다.
					</p>
					<form
						method="POST"
						action="?/analyze"
						use:enhance={() => {
							isAnalyzing = true
							return async ({ update }) => {
								await update()
								await invalidateAll()
								isAnalyzing = false
							}
						}}
					>
						<Button type="submit" variant="outline" class="w-full" disabled={isAnalyzing}>
							<BarChart3 class="h-4 w-4 mr-2" />
							{isAnalyzing ? '실행 중...' : 'ANALYZE 실행'}
						</Button>
					</form>
				</div>

				<div class="space-y-2">
					<div class="font-medium">OPTIMIZE</div>
					<p class="text-sm text-muted-foreground">
						전체 데이터베이스를 최적화합니다.
					</p>
					<form
						method="POST"
						action="?/optimize"
						use:enhance={() => {
							isOptimizing = true
							return async ({ update }) => {
								await update()
								await invalidateAll()
								isOptimizing = false
							}
						}}
					>
						<Button type="submit" variant="outline" class="w-full" disabled={isOptimizing}>
							<Settings class="h-4 w-4 mr-2" />
							{isOptimizing ? '실행 중...' : 'OPTIMIZE 실행'}
						</Button>
					</form>
				</div>
			</div>
		</Card.Content>
	</Card.Root>
</div>
