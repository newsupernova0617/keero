<script lang="ts">
	import type { PageData, ActionData } from './$types'
	import DataTable from '$lib/components/admin/database/DataTable.svelte'
	import RecordModal from '$lib/components/admin/database/RecordModal.svelte'
	import * as Card from '$lib/components/ui/card'
	import { Button } from '$lib/components/ui/button'
	import * as AlertDialog from '$lib/components/ui/alert-dialog'
	import { Badge } from '$lib/components/ui/badge'
	import { Plus, Trash2, ArrowLeft, Download } from '@lucide/svelte'
	import { enhance } from '$app/forms'
	import { goto, invalidateAll } from '$app/navigation'
	import { page } from '$app/stores'

	let { data, form }: { data: PageData; form: ActionData } = $props()

	let tableRef = $state<{ getSelectedRows: () => Record<string, unknown>[]; clearSelection: () => void } | null>(null)
	let modalOpen = $state(false)
	let modalMode = $state<'create' | 'edit' | 'view'>('view')
	let selectedRecord = $state<Record<string, unknown> | undefined>(undefined)
	let deleteDialogOpen = $state(false)
	let recordToDelete = $state<Record<string, unknown> | undefined>(undefined)
	let bulkDeleteDialogOpen = $state(false)
	let isSubmitting = $state(false)

	function handleCreate() {
		modalMode = 'create'
		selectedRecord = undefined
		modalOpen = true
	}

	function handleEdit(row: Record<string, unknown>) {
		modalMode = 'edit'
		selectedRecord = row
		modalOpen = true
	}

	function handleView(row: Record<string, unknown>) {
		modalMode = 'view'
		selectedRecord = row
		modalOpen = true
	}

	function handleDelete(row: Record<string, unknown>) {
		recordToDelete = row
		deleteDialogOpen = true
	}

	function handleBulkDelete() {
		const selected = tableRef?.getSelectedRows()
		if (!selected || selected.length === 0) {
			alert('삭제할 항목을 선택해주세요')
			return
		}
		bulkDeleteDialogOpen = true
	}

	async function handleModalSubmit(formData: Record<string, unknown>) {
		isSubmitting = true

		const form = new FormData()
		for (const [key, value] of Object.entries(formData)) {
			if (value !== null && value !== undefined) {
				form.append(key, String(value))
			}
		}

		try {
			const action = modalMode === 'create' ? '?/create' : '?/update'
			const response = await fetch('', {
				method: 'POST',
				body: form,
				headers: {
					'x-sveltekit-action': 'true'
				}
			})

			if (response.ok) {
				modalOpen = false
				await invalidateAll()
			} else {
				alert('작업에 실패했습니다')
			}
		} catch (error) {
			console.error('Submit error:', error)
			alert('작업에 실패했습니다')
		} finally {
			isSubmitting = false
		}
	}

	async function confirmDelete() {
		if (!recordToDelete) return

		isSubmitting = true
		const form = new FormData()
		form.append('id', String(recordToDelete.id))

		try {
			const response = await fetch('?/delete', {
				method: 'POST',
				body: form
			})

			if (response.ok) {
				deleteDialogOpen = false
				recordToDelete = undefined
				await invalidateAll()
			} else {
				alert('삭제에 실패했습니다')
			}
		} catch (error) {
			console.error('Delete error:', error)
			alert('삭제에 실패했습니다')
		} finally {
			isSubmitting = false
		}
	}

	async function confirmBulkDelete() {
		const selected = tableRef?.getSelectedRows()
		if (!selected || selected.length === 0) return

		isSubmitting = true
		const ids = selected.map((row) => row.id)
		const form = new FormData()
		form.append('ids', JSON.stringify(ids))

		try {
			const response = await fetch('?/bulkDelete', {
				method: 'POST',
				body: form
			})

			if (response.ok) {
				bulkDeleteDialogOpen = false
				tableRef?.clearSelection()
				await invalidateAll()
			} else {
				alert('삭제에 실패했습니다')
			}
		} catch (error) {
			console.error('Bulk delete error:', error)
			alert('삭제에 실패했습니다')
		} finally {
			isSubmitting = false
		}
	}

	function exportToCSV() {
		const csvContent = [
			// Header
			data.tableMetadata.columns.map((col) => col.label).join(','),
			// Rows
			...data.data.map((row) =>
				data.tableMetadata.columns.map((col) => {
					const value = row[col.key]
					if (value === null || value === undefined) return ''
					// Escape commas and quotes
					const str = String(value)
					if (str.includes(',') || str.includes('"') || str.includes('\n')) {
						return `"${str.replace(/"/g, '""')}"`
					}
					return str
				}).join(',')
			)
		].join('\n')

		const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
		const link = document.createElement('a')
		link.href = URL.createObjectURL(blob)
		link.download = `${data.tableMetadata.name}_${new Date().toISOString().split('T')[0]}.csv`
		link.click()
	}
</script>

<svelte:head>
	<title>{data.tableMetadata.displayName} 관리 - Admin</title>
</svelte:head>

<div class="space-y-6">
	<!-- Header -->
	<div class="flex items-center justify-between">
		<div>
			<div class="flex items-center gap-2 mb-2">
				<Button href="/admin/database/tables" variant="ghost" size="sm">
					<ArrowLeft class="h-4 w-4 mr-2" />
					테이블 목록
				</Button>
			</div>
			<h1 class="text-3xl font-bold tracking-tight">
				{data.tableMetadata.displayName}
			</h1>
			<p class="text-muted-foreground">
				{data.tableMetadata.description}
				<span class="font-mono text-sm">({data.tableMetadata.name})</span>
			</p>
		</div>
		<div class="flex items-center gap-2">
			<Button variant="outline" onclick={exportToCSV}>
				<Download class="h-4 w-4 mr-2" />
				CSV 내보내기
			</Button>
			{#if data.tableMetadata.canDelete}
				<Button variant="destructive" onclick={handleBulkDelete}>
					<Trash2 class="h-4 w-4 mr-2" />
					선택 삭제
				</Button>
			{/if}
			{#if data.tableMetadata.canCreate}
				<Button onclick={handleCreate}>
					<Plus class="h-4 w-4 mr-2" />
					새 레코드
				</Button>
			{/if}
		</div>
	</div>

	<!-- Success/Error Messages -->
	{#if form?.success}
		<div class="rounded-lg bg-green-50 dark:bg-green-950 p-4 border border-green-200 dark:border-green-800">
			<p class="text-sm text-green-800 dark:text-green-200">{form.message}</p>
		</div>
	{:else if form?.error}
		<div class="rounded-lg bg-red-50 dark:bg-red-950 p-4 border border-red-200 dark:border-red-800">
			<p class="text-sm text-red-800 dark:text-red-200">{form.error}</p>
		</div>
	{/if}

	<!-- Table -->
	<Card.Root>
		<Card.Content class="pt-6">
			<DataTable
				bind:this={tableRef}
				data={data.data}
				columns={data.tableMetadata.columns}
				onEdit={data.tableMetadata.canEdit ? handleEdit : undefined}
				onDelete={data.tableMetadata.canDelete ? handleDelete : undefined}
				onView={handleView}
				selectable={data.tableMetadata.canDelete}
				searchable={true}
				pagination={true}
				pageSize={20}
			/>
		</Card.Content>
	</Card.Root>
</div>

<!-- Record Modal -->
<RecordModal
	bind:open={modalOpen}
	mode={modalMode}
	columns={data.tableMetadata.columns}
	data={selectedRecord}
	onClose={() => (modalOpen = false)}
	onSubmit={handleModalSubmit}
/>

<!-- Delete Confirmation Dialog -->
<AlertDialog.Root bind:open={deleteDialogOpen}>
	<AlertDialog.Content>
		<AlertDialog.Header>
			<AlertDialog.Title>레코드 삭제</AlertDialog.Title>
			<AlertDialog.Description>
				정말로 이 레코드를 삭제하시겠습니까? 이 작업은 되돌릴 수 없습니다.
				{#if recordToDelete}
					<div class="mt-2 p-2 bg-muted rounded text-sm">
						ID: {recordToDelete.id}
					</div>
				{/if}
			</AlertDialog.Description>
		</AlertDialog.Header>
		<AlertDialog.Footer>
			<AlertDialog.Cancel>취소</AlertDialog.Cancel>
			<AlertDialog.Action onclick={confirmDelete} disabled={isSubmitting}>
				{isSubmitting ? '삭제 중...' : '삭제'}
			</AlertDialog.Action>
		</AlertDialog.Footer>
	</AlertDialog.Content>
</AlertDialog.Root>

<!-- Bulk Delete Confirmation Dialog -->
<AlertDialog.Root bind:open={bulkDeleteDialogOpen}>
	<AlertDialog.Content>
		<AlertDialog.Header>
			<AlertDialog.Title>선택 항목 삭제</AlertDialog.Title>
			<AlertDialog.Description>
				정말로 선택한 {tableRef?.getSelectedRows()?.length || 0}개의 레코드를 삭제하시겠습니까?
				이 작업은 되돌릴 수 없습니다.
			</AlertDialog.Description>
		</AlertDialog.Header>
		<AlertDialog.Footer>
			<AlertDialog.Cancel>취소</AlertDialog.Cancel>
			<AlertDialog.Action onclick={confirmBulkDelete} disabled={isSubmitting}>
				{isSubmitting ? '삭제 중...' : '삭제'}
			</AlertDialog.Action>
		</AlertDialog.Footer>
	</AlertDialog.Content>
</AlertDialog.Root>
