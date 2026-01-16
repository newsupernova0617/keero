<script lang="ts">
	import type { PageData, ActionData } from './$types'
	import * as Card from '$lib/components/ui/card'
	import { Button } from '$lib/components/ui/button'
	import { Textarea } from '$lib/components/ui/textarea'
	import * as Table from '$lib/components/ui/table'
	import * as AlertDialog from '$lib/components/ui/alert-dialog'
	import { Badge } from '$lib/components/ui/badge'
	import { Code, Play, Download, History, AlertTriangle, Database } from '@lucide/svelte'
	import { enhance } from '$app/forms'

	let { data, form }: { data: PageData; form: ActionData } = $props()

	let query = $state('')
	let mode = $state<'read' | 'write'>('read')
	let isExecuting = $state(false)
	let showWarningDialog = $state(false)
	let dangerousQuery = $state('')

	// 쿼리 히스토리 (localStorage)
	let queryHistory = $state<string[]>([])

	$effect(() => {
		if (typeof window !== 'undefined') {
			const saved = localStorage.getItem('sql-query-history')
			if (saved) {
				queryHistory = JSON.parse(saved)
			}
		}
	})

	function saveToHistory(q: string) {
		if (!q.trim()) return
		const newHistory = [q, ...queryHistory.filter((h) => h !== q)].slice(0, 20)
		queryHistory = newHistory
		if (typeof window !== 'undefined') {
			localStorage.setItem('sql-query-history', JSON.stringify(newHistory))
		}
	}

	function loadFromHistory(q: string) {
		query = q
	}

	function clearHistory() {
		queryHistory = []
		if (typeof window !== 'undefined') {
			localStorage.removeItem('sql-query-history')
		}
	}

	// 샘플 쿼리
	const sampleQueries = [
		{
			label: '최근 게시글 10개',
			query: 'SELECT id, title, site_name, created_at FROM posts ORDER BY created_at DESC LIMIT 10;'
		},
		{
			label: '사이트별 게시글 수',
			query: 'SELECT site_name, COUNT(*) as count FROM posts GROUP BY site_name ORDER BY count DESC;'
		},
		{
			label: '최근 댓글 10개',
			query:
				'SELECT c.id, c.content, u.display_name, p.title, c.created_at FROM comments c JOIN users u ON c.user_id = u.id JOIN posts p ON c.post_id = p.id ORDER BY c.created_at DESC LIMIT 10;'
		},
		{
			label: '사용자별 댓글 수',
			query:
				'SELECT u.display_name, COUNT(c.id) as comment_count FROM users u LEFT JOIN comments c ON u.id = c.user_id GROUP BY u.id ORDER BY comment_count DESC LIMIT 10;'
		},
		{
			label: '테이블 목록',
			query: "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;"
		}
	]

	function loadSampleQuery(sampleQuery: string) {
		query = sampleQuery
	}

	async function handleExecute() {
		if (!query.trim()) {
			alert('쿼리를 입력해주세요')
			return
		}

		saveToHistory(query)
		isExecuting = true
	}

	function handleWarningConfirm() {
		showWarningDialog = false
		// 위험한 쿼리를 확인된 모드로 재실행
		const formElement = document.querySelector('form[data-dangerous]') as HTMLFormElement
		if (formElement) {
			const modeInput = formElement.querySelector('input[name="mode"]') as HTMLInputElement
			modeInput.value = 'write-confirmed'
			formElement.requestSubmit()
		}
	}

	function exportToCSV() {
		if (!form?.results || form.results.length === 0) return

		const headers = Object.keys(form.results[0])
		const csvContent = [
			headers.join(','),
			...form.results.map((row) =>
				headers
					.map((header) => {
						const value = row[header]
						if (value === null || value === undefined) return ''
						const str = String(value)
						if (str.includes(',') || str.includes('"') || str.includes('\n')) {
							return `"${str.replace(/"/g, '""')}"`
						}
						return str
					})
					.join(',')
			)
		].join('\n')

		const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
		const link = document.createElement('a')
		link.href = URL.createObjectURL(blob)
		link.download = `query_result_${new Date().toISOString().split('T')[0]}.csv`
		link.click()
	}

	function exportToJSON() {
		if (!form?.results) return

		const blob = new Blob([JSON.stringify(form.results, null, 2)], {
			type: 'application/json'
		})
		const link = document.createElement('a')
		link.href = URL.createObjectURL(blob)
		link.download = `query_result_${new Date().toISOString().split('T')[0]}.json`
		link.click()
	}

	// 위험한 쿼리 경고 처리
	$effect(() => {
		if ((form as any)?.warning) {
			showWarningDialog = true
			dangerousQuery = (form as any).query || ''
		}
	})
</script>

<svelte:head>
	<title>SQL 쿼리 실행 - Admin</title>
</svelte:head>

<div class="space-y-6">
	<div>
		<h1 class="text-3xl font-bold tracking-tight flex items-center gap-2">
			<Code class="h-8 w-8" />
			SQL 쿼리 실행
		</h1>
		<p class="text-muted-foreground">데이터베이스에 직접 SQL 쿼리를 실행합니다</p>
	</div>

	<!-- 모드 선택 -->
	<Card.Root>
		<Card.Header>
			<Card.Title>실행 모드</Card.Title>
			<Card.Description>쿼리 실행 권한을 선택하세요</Card.Description>
		</Card.Header>
		<Card.Content>
			<div class="flex gap-4">
				<label class="flex items-center gap-2 cursor-pointer">
					<input type="radio" bind:group={mode} value="read" class="w-4 h-4" />
					<div>
						<div class="font-medium">읽기 전용</div>
						<div class="text-sm text-muted-foreground">SELECT 쿼리만 실행 가능</div>
					</div>
				</label>
				<label class="flex items-center gap-2 cursor-pointer">
					<input type="radio" bind:group={mode} value="write" class="w-4 h-4" />
					<div>
						<div class="font-medium text-destructive">쓰기 허용</div>
						<div class="text-sm text-muted-foreground">
							INSERT, UPDATE, DELETE 등 모든 쿼리 실행 가능
						</div>
					</div>
				</label>
			</div>
		</Card.Content>
	</Card.Root>

	<!-- 쿼리 입력 -->
	<Card.Root>
		<Card.Header>
			<div class="flex items-center justify-between">
				<div>
					<Card.Title>SQL 쿼리</Card.Title>
					<Card.Description>실행할 SQL 쿼리를 입력하세요</Card.Description>
				</div>
				<div class="flex gap-2">
					{#if queryHistory.length > 0}
						<Button variant="outline" size="sm" onclick={() => (showWarningDialog = true)}>
							<History class="h-4 w-4 mr-2" />
							히스토리
						</Button>
					{/if}
				</div>
			</div>
		</Card.Header>
		<Card.Content class="space-y-4">
			<form
				method="POST"
				action="?/execute"
				data-dangerous={(form as any)?.warning ? 'true' : 'false'}
				use:enhance={() => {
					isExecuting = true
					return async ({ update }) => {
						await update()
						isExecuting = false
					}
				}}
			>
				<input type="hidden" name="mode" value={mode} />
				<Textarea
					name="query"
					bind:value={query}
					placeholder="SELECT * FROM posts LIMIT 10;"
					rows={8}
					class="font-mono text-sm"
				/>
				<div class="flex items-center justify-between mt-4">
					<div class="text-sm text-muted-foreground">
						{#if mode === 'read'}
							<Badge variant="secondary">읽기 전용 모드</Badge>
						{:else}
							<Badge variant="destructive">쓰기 모드</Badge>
						{/if}
					</div>
					<Button type="submit" disabled={isExecuting || !query.trim()}>
						<Play class="h-4 w-4 mr-2" />
						{isExecuting ? '실행 중...' : '실행'}
					</Button>
				</div>
			</form>

			<!-- 샘플 쿼리 -->
			<div class="border-t pt-4">
				<p class="text-sm font-medium mb-2">샘플 쿼리:</p>
				<div class="flex flex-wrap gap-2">
					{#each sampleQueries as sample}
						<Button variant="outline" size="sm" onclick={() => loadSampleQuery(sample.query)}>
							{sample.label}
						</Button>
					{/each}
				</div>
			</div>
		</Card.Content>
	</Card.Root>

	<!-- 결과 -->
	{#if form?.success}
		<Card.Root>
			<Card.Header>
				<div class="flex items-center justify-between">
					<div>
						<Card.Title>실행 결과</Card.Title>
						<Card.Description>
							{#if form.results}
								{form.rowCount}개 행 조회됨 · {form.executionTime}ms
							{:else if form.changes !== undefined}
								{form.changes}개 행 영향받음 · {form.executionTime}ms
							{/if}
						</Card.Description>
					</div>
					{#if form.results && form.results.length > 0}
						<div class="flex gap-2">
							<Button variant="outline" size="sm" onclick={exportToCSV}>
								<Download class="h-4 w-4 mr-2" />
								CSV
							</Button>
							<Button variant="outline" size="sm" onclick={exportToJSON}>
								<Download class="h-4 w-4 mr-2" />
								JSON
							</Button>
						</div>
					{/if}
				</div>
			</Card.Header>
			<Card.Content>
				{#if form.results && form.results.length > 0}
					<div class="rounded-md border overflow-x-auto">
						<Table.Root>
							<Table.Header>
								<Table.Row>
									{#each Object.keys(form.results[0]) as header}
										<Table.Head>{header}</Table.Head>
									{/each}
								</Table.Row>
							</Table.Header>
							<Table.Body>
								{#each form.results as row}
									<Table.Row>
										{#each Object.values(row) as value}
											<Table.Cell class="font-mono text-sm">
												{value === null || value === undefined ? '-' : String(value)}
											</Table.Cell>
										{/each}
									</Table.Row>
								{/each}
							</Table.Body>
						</Table.Root>
					</div>
				{:else if form.message}
					<div class="rounded-lg bg-green-50 dark:bg-green-950 p-4 border border-green-200 dark:border-green-800">
						<p class="text-sm text-green-800 dark:text-green-200">{form.message}</p>
					</div>
				{/if}
			</Card.Content>
		</Card.Root>
	{:else if form?.error && !(form as any)?.warning}
		<Card.Root>
			<Card.Content class="pt-6">
				<div class="rounded-lg bg-red-50 dark:bg-red-950 p-4 border border-red-200 dark:border-red-800">
					<p class="text-sm text-red-800 dark:text-red-200 font-mono">{form.error}</p>
				</div>
			</Card.Content>
		</Card.Root>
	{/if}

	<!-- 쿼리 히스토리 -->
	{#if queryHistory.length > 0}
		<Card.Root>
			<Card.Header>
				<div class="flex items-center justify-between">
					<div>
						<Card.Title>쿼리 히스토리</Card.Title>
						<Card.Description>최근 실행한 쿼리 {queryHistory.length}개</Card.Description>
					</div>
					<Button variant="outline" size="sm" onclick={clearHistory}>
						히스토리 삭제
					</Button>
				</div>
			</Card.Header>
			<Card.Content>
				<div class="space-y-2">
					{#each queryHistory.slice(0, 10) as historyQuery, index}
						<button
							onclick={() => loadFromHistory(historyQuery)}
							class="w-full text-left p-3 rounded-lg border hover:bg-muted/50 transition-colors"
						>
							<div class="flex items-start gap-2">
								<span class="text-xs text-muted-foreground mt-1">{index + 1}.</span>
								<code class="text-sm flex-1 break-all">{historyQuery}</code>
							</div>
						</button>
					{/each}
				</div>
			</Card.Content>
		</Card.Root>
	{/if}
</div>

<!-- 위험한 쿼리 경고 다이얼로그 -->
<AlertDialog.Root bind:open={showWarningDialog}>
	<AlertDialog.Content>
		<AlertDialog.Header>
			<AlertDialog.Title class="flex items-center gap-2 text-destructive">
				<AlertTriangle class="h-5 w-5" />
				위험한 쿼리 감지
			</AlertDialog.Title>
			<AlertDialog.Description>
				<p class="mb-4">
					이 쿼리는 데이터를 영구적으로 변경하거나 삭제할 수 있습니다. 정말 실행하시겠습니까?
				</p>
				<div class="rounded-lg bg-muted p-3">
					<code class="text-sm">{dangerousQuery}</code>
				</div>
			</AlertDialog.Description>
		</AlertDialog.Header>
		<AlertDialog.Footer>
			<AlertDialog.Cancel>취소</AlertDialog.Cancel>
			<AlertDialog.Action onclick={handleWarningConfirm} class="bg-destructive text-destructive-foreground hover:bg-destructive/90">
				실행
			</AlertDialog.Action>
		</AlertDialog.Footer>
	</AlertDialog.Content>
</AlertDialog.Root>
