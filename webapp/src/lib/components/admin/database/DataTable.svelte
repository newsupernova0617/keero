<script lang="ts" generics="T extends Record<string, any>">
	import * as Table from '$lib/components/ui/table'
	import { Button } from '$lib/components/ui/button'
	import { Input } from '$lib/components/ui/input'
	import { Checkbox } from '$lib/components/ui/checkbox'
	import { Badge } from '$lib/components/ui/badge'
	import {
		ChevronUp,
		ChevronDown,
		ChevronsUpDown,
		Edit,
		Trash2,
		Eye,
		Search,
		X
	} from '@lucide/svelte'

	interface Column<T> {
		key: keyof T
		label: string
		sortable?: boolean
		type?: 'text' | 'number' | 'date' | 'boolean' | 'badge' | 'select' | 'textarea' | 'custom'
		render?: (value: any, row: T) => string
		width?: string
	}

	interface Props {
		data: T[]
		columns: Column<T>[]
		onEdit?: (row: T) => void
		onDelete?: (row: T) => void
		onView?: (row: T) => void
		selectable?: boolean
		searchable?: boolean
		pagination?: boolean
		pageSize?: number
		loading?: boolean
	}

	let {
		data = [],
		columns,
		onEdit,
		onDelete,
		onView,
		selectable = false,
		searchable = true,
		pagination = true,
		pageSize = 20,
		loading = false
	}: Props = $props()

	// State
	let searchQuery = $state('')
	let sortColumn = $state<keyof T | null>(null)
	let sortDirection = $state<'asc' | 'desc'>('asc')
	let currentPage = $state(1)
	let selectedRows = $state<Set<number>>(new Set())

	// Computed
	let filteredData = $derived.by(() => {
		if (!searchQuery) return data

		return data.filter((row) => {
			return columns.some((col) => {
				const value = row[col.key]
				if (value === null || value === undefined) return false
				return String(value).toLowerCase().includes(searchQuery.toLowerCase())
			})
		})
	})

	let sortedData = $derived.by(() => {
		if (!sortColumn) return filteredData

		return [...filteredData].sort((a, b) => {
			const col = sortColumn as keyof T
			const aVal = a[col]
			const bVal = b[col]

			if (aVal === null || aVal === undefined) return 1
			if (bVal === null || bVal === undefined) return -1

			let comparison = 0
			if (typeof aVal === 'number' && typeof bVal === 'number') {
				comparison = aVal - bVal
			} else {
				comparison = String(aVal).localeCompare(String(bVal))
			}

			return sortDirection === 'asc' ? comparison : -comparison
		})
	})

	let paginatedData = $derived.by(() => {
		if (!pagination) return sortedData

		const start = (currentPage - 1) * pageSize
		const end = start + pageSize
		return sortedData.slice(start, end)
	})

	let totalPages = $derived(Math.ceil(sortedData.length / pageSize))
	let allSelected = $derived(
		selectedRows.size > 0 && selectedRows.size === paginatedData.length
	)

	// Functions
	function handleSort(column: Column<T>) {
		if (!column.sortable) return

		if (sortColumn === column.key) {
			sortDirection = sortDirection === 'asc' ? 'desc' : 'asc'
		} else {
			sortColumn = column.key
			sortDirection = 'asc'
		}
	}

	function toggleSelectAll() {
		if (allSelected) {
			selectedRows.clear()
		} else {
			paginatedData.forEach((_, index) => {
				selectedRows.add((currentPage - 1) * pageSize + index)
			})
		}
		selectedRows = selectedRows
	}

	function toggleSelectRow(index: number) {
		const globalIndex = (currentPage - 1) * pageSize + index
		if (selectedRows.has(globalIndex)) {
			selectedRows.delete(globalIndex)
		} else {
			selectedRows.add(globalIndex)
		}
		selectedRows = selectedRows
	}

	function formatValue(value: any, column: Column<T>, row: T): string {
		if (column.render) {
			return column.render(value, row)
		}

		if (value === null || value === undefined) {
			return '-'
		}

		switch (column.type) {
			case 'date':
				return new Date(value).toLocaleString('ko-KR', {
					year: 'numeric',
					month: '2-digit',
					day: '2-digit',
					hour: '2-digit',
					minute: '2-digit'
				})
			case 'boolean':
				return value ? '✓' : '✗'
			case 'number':
				return typeof value === 'number' ? value.toLocaleString() : String(value)
			default:
				return String(value)
		}
	}

	function clearSearch() {
		searchQuery = ''
	}

	function goToPage(page: number) {
		if (page >= 1 && page <= totalPages) {
			currentPage = page
		}
	}

	// Export selected rows for parent component
	export function getSelectedRows(): T[] {
		return Array.from(selectedRows).map((index) => sortedData[index])
	}

	export function clearSelection() {
		selectedRows.clear()
		selectedRows = selectedRows
	}
</script>

<div class="space-y-4">
	<!-- Search Bar -->
	{#if searchable}
		<div class="flex items-center gap-2">
			<div class="relative flex-1 max-w-sm">
				<Search class="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
				<Input
					type="text"
					placeholder="검색..."
					bind:value={searchQuery}
					class="pl-9 pr-9"
				/>
				{#if searchQuery}
					<button
						onclick={clearSearch}
						class="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
					>
						<X class="h-4 w-4" />
					</button>
				{/if}
			</div>
			<div class="text-sm text-muted-foreground">
				{sortedData.length}개 항목
				{#if selectedRows.size > 0}
					<span class="text-primary font-medium">({selectedRows.size}개 선택됨)</span>
				{/if}
			</div>
		</div>
	{/if}

	<!-- Table -->
	<div class="rounded-md border">
		<Table.Root>
			<Table.Header>
				<Table.Row>
					{#if selectable}
						<Table.Head class="w-12">
							<Checkbox checked={allSelected} onCheckedChange={toggleSelectAll} />
						</Table.Head>
					{/if}
					{#each columns as column}
						<Table.Head
							class={column.sortable ? 'cursor-pointer select-none hover:bg-muted/50' : ''}
							style={column.width ? `width: ${column.width}` : ''}
							onclick={() => handleSort(column)}
						>
							<div class="flex items-center gap-2">
								<span>{column.label}</span>
								{#if column.sortable}
									{#if sortColumn === column.key}
										{#if sortDirection === 'asc'}
											<ChevronUp class="h-4 w-4" />
										{:else}
											<ChevronDown class="h-4 w-4" />
										{/if}
									{:else}
										<ChevronsUpDown class="h-4 w-4 opacity-50" />
									{/if}
								{/if}
							</div>
						</Table.Head>
					{/each}
					{#if onEdit || onDelete || onView}
						<Table.Head class="text-right w-32">액션</Table.Head>
					{/if}
				</Table.Row>
			</Table.Header>
			<Table.Body>
				{#if loading}
					<Table.Row>
						<Table.Cell colspan={columns.length + (selectable ? 1 : 0) + (onEdit || onDelete || onView ? 1 : 0)} class="text-center py-8">
							<div class="flex items-center justify-center gap-2">
								<div class="animate-spin rounded-full h-5 w-5 border-b-2 border-primary"></div>
								<span class="text-muted-foreground">로딩 중...</span>
							</div>
						</Table.Cell>
					</Table.Row>
				{:else if paginatedData.length === 0}
					<Table.Row>
						<Table.Cell colspan={columns.length + (selectable ? 1 : 0) + (onEdit || onDelete || onView ? 1 : 0)} class="text-center py-8">
							<div class="text-muted-foreground">
								{searchQuery ? '검색 결과가 없습니다' : '데이터가 없습니다'}
							</div>
						</Table.Cell>
					</Table.Row>
				{:else}
					{#each paginatedData as row, index}
						<Table.Row>
							{#if selectable}
								<Table.Cell>
									<Checkbox
										checked={selectedRows.has((currentPage - 1) * pageSize + index)}
										onCheckedChange={() => toggleSelectRow(index)}
									/>
								</Table.Cell>
							{/if}
							{#each columns as column}
								<Table.Cell>
									{#if column.type === 'badge'}
										<Badge variant="secondary">{formatValue(row[column.key], column, row)}</Badge>
									{:else}
										<span class={column.type === 'number' ? 'font-mono' : ''}>
											{formatValue(row[column.key], column, row)}
										</span>
									{/if}
								</Table.Cell>
							{/each}
							{#if onEdit || onDelete || onView}
								<Table.Cell class="text-right">
									<div class="flex items-center justify-end gap-1">
										{#if onView}
											<Button variant="ghost" size="sm" onclick={() => onView?.(row)}>
												<Eye class="h-4 w-4" />
											</Button>
										{/if}
										{#if onEdit}
											<Button variant="ghost" size="sm" onclick={() => onEdit?.(row)}>
												<Edit class="h-4 w-4" />
											</Button>
										{/if}
										{#if onDelete}
											<Button
												variant="ghost"
												size="sm"
												onclick={() => onDelete?.(row)}
												class="text-destructive hover:text-destructive"
											>
												<Trash2 class="h-4 w-4" />
											</Button>
										{/if}
									</div>
								</Table.Cell>
							{/if}
						</Table.Row>
					{/each}
				{/if}
			</Table.Body>
		</Table.Root>
	</div>

	<!-- Pagination -->
	{#if pagination && totalPages > 1}
		<div class="flex items-center justify-between">
			<div class="text-sm text-muted-foreground">
				{(currentPage - 1) * pageSize + 1}-{Math.min(currentPage * pageSize, sortedData.length)} / {sortedData.length}
			</div>
			<div class="flex items-center gap-2">
				<Button
					variant="outline"
					size="sm"
					disabled={currentPage === 1}
					onclick={() => goToPage(currentPage - 1)}
				>
					이전
				</Button>
				<div class="flex items-center gap-1">
					{#if totalPages <= 7}
						{#each Array(totalPages) as _, i}
							<Button
								variant={currentPage === i + 1 ? 'default' : 'outline'}
								size="sm"
								onclick={() => goToPage(i + 1)}
							>
								{i + 1}
							</Button>
						{/each}
					{:else}
						<Button
							variant={currentPage === 1 ? 'default' : 'outline'}
							size="sm"
							onclick={() => goToPage(1)}
						>
							1
						</Button>
						{#if currentPage > 3}
							<span class="px-2">...</span>
						{/if}
						{#each Array(5) as _, i}
							{@const page = Math.max(2, Math.min(totalPages - 1, currentPage - 2 + i))}
							{#if page > 1 && page < totalPages}
								<Button
									variant={currentPage === page ? 'default' : 'outline'}
									size="sm"
									onclick={() => goToPage(page)}
								>
									{page}
								</Button>
							{/if}
						{/each}
						{#if currentPage < totalPages - 2}
							<span class="px-2">...</span>
						{/if}
						<Button
							variant={currentPage === totalPages ? 'default' : 'outline'}
							size="sm"
							onclick={() => goToPage(totalPages)}
						>
							{totalPages}
						</Button>
					{/if}
				</div>
				<Button
					variant="outline"
					size="sm"
					disabled={currentPage === totalPages}
					onclick={() => goToPage(currentPage + 1)}
				>
					다음
				</Button>
			</div>
		</div>
	{/if}
</div>
