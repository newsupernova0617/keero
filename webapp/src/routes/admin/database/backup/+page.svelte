<script lang="ts">
	import type { PageData, ActionData } from './$types'
	import * as Card from '$lib/components/ui/card'
	import * as Table from '$lib/components/ui/table'
	import { Button } from '$lib/components/ui/button'
	import * as AlertDialog from '$lib/components/ui/alert-dialog'
	import { Badge } from '$lib/components/ui/badge'
	import {
		HardDrive,
		Plus,
		Download,
		RotateCcw,
		Trash2,
		Database,
		AlertTriangle
	} from '@lucide/svelte'
	import { enhance } from '$app/forms'
	import { invalidateAll } from '$app/navigation'

	let { data, form }: { data: PageData; form: ActionData } = $props()

	let isCreating = $state(false)
	let deleteDialogOpen = $state(false)
	let restoreDialogOpen = $state(false)
	let selectedBackup = $state<string>('')

	function handleDeleteClick(filename: string) {
		selectedBackup = filename
		deleteDialogOpen = true
	}

	function handleRestoreClick(filename: string) {
		selectedBackup = filename
		restoreDialogOpen = true
	}

	async function confirmDelete() {
		const formElement = document.getElementById('delete-form') as HTMLFormElement
		if (formElement) {
			formElement.requestSubmit()
		}
	}

	async function confirmRestore() {
		const formElement = document.getElementById('restore-form') as HTMLFormElement
		if (formElement) {
			formElement.requestSubmit()
		}
	}
</script>

<svelte:head>
	<title>백업 관리 - Admin</title>
</svelte:head>

<div class="space-y-6">
	<div>
		<h1 class="text-3xl font-bold tracking-tight flex items-center gap-2">
			<HardDrive class="h-8 w-8" />
			백업 관리
		</h1>
		<p class="text-muted-foreground">데이터베이스 백업 생성 및 복원</p>
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

	<!-- 현재 데이터베이스 정보 -->
	<Card.Root>
		<Card.Header>
			<Card.Title>현재 데이터베이스</Card.Title>
			<Card.Description>활성 데이터베이스 정보</Card.Description>
		</Card.Header>
		<Card.Content>
			<div class="space-y-3">
				<div class="flex items-center justify-between">
					<span class="text-sm text-muted-foreground">파일 경로</span>
					<code class="text-sm">{data.dbInfo.path}</code>
				</div>
				<div class="flex items-center justify-between">
					<span class="text-sm text-muted-foreground">파일 크기</span>
					<Badge variant="secondary">{data.dbInfo.sizeFormatted}</Badge>
				</div>
				<div class="flex items-center justify-between">
					<span class="text-sm text-muted-foreground">마지막 수정</span>
					<span class="text-sm">
						{new Date(data.dbInfo.lastModified).toLocaleString('ko-KR')}
					</span>
				</div>
				<div class="flex items-center justify-between">
					<span class="text-sm text-muted-foreground">백업 저장소</span>
					<Badge variant="outline" class="gap-1">
						<HardDrive class="h-3 w-3" />
						Cloudflare R2
					</Badge>
				</div>
			</div>

			<div class="mt-6">
				<form
					method="POST"
					action="?/createBackup"
					use:enhance={() => {
						isCreating = true
						return async ({ update }) => {
							await update()
							await invalidateAll()
							isCreating = false
						}
					}}
				>
					<Button type="submit" disabled={isCreating} class="w-full">
						<Plus class="h-4 w-4 mr-2" />
						{isCreating ? '백업 생성 및 R2 업로드 중...' : '지금 백업 생성 (R2에 저장)'}
					</Button>
				</form>
			</div>
		</Card.Content>
	</Card.Root>

	<!-- 백업 파일 목록 -->
	<Card.Root>
		<Card.Header>
			<Card.Title>백업 파일 목록</Card.Title>
			<Card.Description>
				{data.backups.length}개의 백업 파일
			</Card.Description>
		</Card.Header>
		<Card.Content>
			{#if data.backups.length === 0}
				<div class="text-center py-8 text-muted-foreground">
					<Database class="h-12 w-12 mx-auto mb-4 opacity-50" />
					<p>백업 파일이 없습니다</p>
					<p class="text-sm">위의 버튼을 클릭하여 첫 백업을 생성하세요</p>
				</div>
			{:else}
				<div class="rounded-md border">
					<Table.Root>
						<Table.Header>
							<Table.Row>
								<Table.Head>파일명</Table.Head>
								<Table.Head>크기</Table.Head>
								<Table.Head>생성일</Table.Head>
								<Table.Head class="text-right">액션</Table.Head>
							</Table.Row>
						</Table.Header>
						<Table.Body>
							{#each data.backups as backup}
								<Table.Row>
									<Table.Cell class="font-mono text-sm">{backup.filename}</Table.Cell>
									<Table.Cell>
										<Badge variant="secondary">{backup.sizeFormatted}</Badge>
									</Table.Cell>
									<Table.Cell class="text-sm">{backup.lastModifiedFormatted}</Table.Cell>
									<Table.Cell class="text-right">
										<div class="flex items-center justify-end gap-2">
											<Button
												variant="outline"
												size="sm"
												onclick={() => handleRestoreClick(backup.filename)}
											>
												<RotateCcw class="h-4 w-4 mr-2" />
												복원
											</Button>
											<Button
												variant="ghost"
												size="sm"
												onclick={() => handleDeleteClick(backup.filename)}
												class="text-destructive hover:text-destructive"
											>
												<Trash2 class="h-4 w-4" />
											</Button>
										</div>
									</Table.Cell>
								</Table.Row>
							{/each}
						</Table.Body>
					</Table.Root>
				</div>
			{/if}
		</Card.Content>
	</Card.Root>

	<!-- 자동 백업 설정 (향후 구현) -->
	<Card.Root>
		<Card.Header>
			<Card.Title>자동 백업 설정</Card.Title>
			<Card.Description>정기적인 자동 백업 (향후 구현 예정)</Card.Description>
		</Card.Header>
		<Card.Content>
			<div class="text-sm text-muted-foreground">
				<p>자동 백업 기능은 향후 업데이트에서 제공될 예정입니다.</p>
				<p class="mt-2">현재는 수동으로 백업을 생성해주세요.</p>
			</div>
		</Card.Content>
	</Card.Root>
</div>

<!-- 삭제 확인 다이얼로그 -->
<AlertDialog.Root bind:open={deleteDialogOpen}>
	<AlertDialog.Content>
		<AlertDialog.Header>
			<AlertDialog.Title>백업 파일 삭제</AlertDialog.Title>
			<AlertDialog.Description>
				정말로 이 백업 파일을 삭제하시겠습니까? 이 작업은 되돌릴 수 없습니다.
				<div class="mt-2 p-2 bg-muted rounded text-sm font-mono">
					{selectedBackup}
				</div>
			</AlertDialog.Description>
		</AlertDialog.Header>
		<AlertDialog.Footer>
			<AlertDialog.Cancel>취소</AlertDialog.Cancel>
			<AlertDialog.Action onclick={confirmDelete}>삭제</AlertDialog.Action>
		</AlertDialog.Footer>
	</AlertDialog.Content>
</AlertDialog.Root>

<!-- 복원 확인 다이얼로그 -->
<AlertDialog.Root bind:open={restoreDialogOpen}>
	<AlertDialog.Content>
		<AlertDialog.Header>
			<AlertDialog.Title class="flex items-center gap-2 text-destructive">
				<AlertTriangle class="h-5 w-5" />
				백업 복원
			</AlertDialog.Title>
			<AlertDialog.Description>
				<p class="mb-4">
					백업을 복원하면 현재 데이터베이스가 선택한 백업으로 교체됩니다. 현재 데이터베이스는
					자동으로 백업됩니다.
				</p>
				<div class="p-3 bg-muted rounded">
					<p class="text-sm font-medium mb-1">복원할 백업:</p>
					<code class="text-sm">{selectedBackup}</code>
				</div>
				<p class="mt-4 text-sm font-medium text-destructive">
					이 작업은 신중하게 진행해야 합니다. 계속하시겠습니까?
				</p>
			</AlertDialog.Description>
		</AlertDialog.Header>
		<AlertDialog.Footer>
			<AlertDialog.Cancel>취소</AlertDialog.Cancel>
			<AlertDialog.Action
				onclick={confirmRestore}
				class="bg-destructive text-destructive-foreground hover:bg-destructive/90"
			>
				복원
			</AlertDialog.Action>
		</AlertDialog.Footer>
	</AlertDialog.Content>
</AlertDialog.Root>

<!-- Hidden forms for delete and restore -->
<form
	id="delete-form"
	method="POST"
	action="?/deleteBackup"
	use:enhance={() => {
		return async ({ update }) => {
			await update()
			await invalidateAll()
			deleteDialogOpen = false
		}
	}}
	style="display: none;"
>
	<input type="hidden" name="filename" value={selectedBackup} />
</form>

<form
	id="restore-form"
	method="POST"
	action="?/restoreBackup"
	use:enhance={() => {
		return async ({ update }) => {
			await update()
			await invalidateAll()
			restoreDialogOpen = false
		}
	}}
	style="display: none;"
>
	<input type="hidden" name="filename" value={selectedBackup} />
</form>
