<script lang="ts">
	import * as Dialog from '$lib/components/ui/dialog'
	import { Button } from '$lib/components/ui/button'
	import { Input } from '$lib/components/ui/input'
	import { Label } from '$lib/components/ui/label'
	import { Textarea } from '$lib/components/ui/textarea'
	import { Checkbox } from '$lib/components/ui/checkbox'
	import type { ColumnMetadata } from '$lib/server/tableMetadata'

	interface Props {
		open: boolean
		mode: 'create' | 'edit' | 'view'
		columns: ColumnMetadata[]
		data?: Record<string, any>
		onClose: () => void
		onSubmit: (data: Record<string, any>) => void
	}

	let { open = $bindable(), mode, columns, data = {}, onClose, onSubmit }: Props = $props()

	let formData = $state<Record<string, any>>({})

	$effect(() => {
		if (open) {
			formData = { ...data }
		}
	})

	function handleSubmit(e: Event) {
		e.preventDefault()
		onSubmit(formData)
	}

	function handleCheckboxChange(key: string, checked: boolean | 'indeterminate') {
		formData[key] = checked === true
	}
</script>

<Dialog.Root bind:open>
	<Dialog.Content class="max-w-2xl max-h-[80vh] overflow-y-auto">
		<Dialog.Header>
			<Dialog.Title>
				{#if mode === 'create'}
					새 레코드 생성
				{:else if mode === 'edit'}
					레코드 수정
				{:else}
					레코드 상세
				{/if}
			</Dialog.Title>
			<Dialog.Description>
				{#if mode === 'create'}
					새로운 레코드를 생성합니다.
				{:else if mode === 'edit'}
					레코드 정보를 수정합니다.
				{:else}
					레코드 상세 정보를 확인합니다.
				{/if}
			</Dialog.Description>
		</Dialog.Header>

		<form onsubmit={handleSubmit} class="space-y-4">
			{#each columns as column}
				{#if mode === 'create' && column.key === 'id'}
					<!-- Skip ID field in create mode -->
				{:else if mode !== 'create' && !column.editable && mode !== 'view'}
					<!-- Skip non-editable fields in edit mode -->
				{:else}
					<div class="space-y-2">
						<Label for={column.key}>
							{column.label}
							{#if column.required && mode !== 'view'}
								<span class="text-destructive">*</span>
							{/if}
						</Label>

						{#if column.type === 'textarea'}
							<Textarea
								id={column.key}
								bind:value={formData[column.key]}
								placeholder={column.placeholder}
								disabled={mode === 'view' || !column.editable}
								required={column.required && mode !== 'view'}
								rows={4}
							/>
						{:else if column.type === 'select' && column.options}
							<select
								id={column.key}
								bind:value={formData[column.key]}
								disabled={mode === 'view' || !column.editable}
								required={column.required && mode !== 'view'}
								class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
							>
								<option value="">선택하세요</option>
								{#each column.options as option}
									<option value={option.value}>{option.label}</option>
								{/each}
							</select>
						{:else if column.type === 'boolean'}
							<div class="flex items-center space-x-2">
								<Checkbox
									id={column.key}
									checked={!!formData[column.key]}
									onCheckedChange={(checked) => handleCheckboxChange(column.key, checked)}
									disabled={mode === 'view' || !column.editable}
								/>
								<label
									for={column.key}
									class="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
								>
									활성화
								</label>
							</div>
						{:else if column.type === 'number'}
							<Input
								id={column.key}
								type="number"
								bind:value={formData[column.key]}
								placeholder={column.placeholder}
								disabled={mode === 'view' || !column.editable}
								required={column.required && mode !== 'view'}
							/>
						{:else if column.type === 'date'}
							<Input
								id={column.key}
								type="datetime-local"
								bind:value={formData[column.key]}
								disabled={mode === 'view' || !column.editable}
								required={column.required && mode !== 'view'}
							/>
						{:else}
							<Input
								id={column.key}
								type="text"
								bind:value={formData[column.key]}
								placeholder={column.placeholder}
								disabled={mode === 'view' || !column.editable}
								required={column.required && mode !== 'view'}
								maxlength={column.maxLength}
							/>
						{/if}

						{#if column.maxLength && mode !== 'view'}
							<p class="text-xs text-muted-foreground">
								최대 {column.maxLength}자
							</p>
						{/if}
					</div>
				{/if}
			{/each}

			<Dialog.Footer>
				<Button type="button" variant="outline" onclick={onClose}>
					{mode === 'view' ? '닫기' : '취소'}
				</Button>
				{#if mode !== 'view'}
					<Button type="submit">
						{mode === 'create' ? '생성' : '저장'}
					</Button>
				{/if}
			</Dialog.Footer>
		</form>
	</Dialog.Content>
</Dialog.Root>
