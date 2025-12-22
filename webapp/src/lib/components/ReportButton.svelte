<script lang="ts">
	import { enhance } from '$app/forms'
	import * as Dialog from '$lib/components/ui/dialog'
	import { Button } from '$lib/components/ui/button'
	import { Label } from '$lib/components/ui/label'
	import { Textarea } from '$lib/components/ui/textarea'
	import * as Select from '$lib/components/ui/select'
	import { Flag } from '@lucide/svelte'

	let {
		postId,
		commentId,
		session
	}: {
		postId?: number
		commentId?: number
		session: any
	} = $props()

	let open = $state(false)
	let reason = $state('spam')
	let description = $state('')

	const reasons = [
		{ value: 'spam', label: '스팸' },
		{ value: 'inappropriate', label: '부적절한 콘텐츠' },
		{ value: 'harassment', label: '괴롭힘' },
		{ value: 'misinformation', label: '허위 정보' },
		{ value: 'other', label: '기타' }
	]
</script>

<Dialog.Root bind:open>
	<Dialog.Trigger>
		<Button
			variant="ghost"
			size="sm"
			class="h-auto gap-1 p-0 text-xs text-muted-foreground hover:bg-transparent hover:text-destructive"
			disabled={!session}
		>
			<Flag class="h-3 w-3" />
			신고
		</Button>
	</Dialog.Trigger>
	<Dialog.Content>
		<Dialog.Header>
			<Dialog.Title>신고하기</Dialog.Title>
			<Dialog.Description>
				부적절한 콘텐츠를 신고해주세요. 관리자가 검토합니다.
			</Dialog.Description>
		</Dialog.Header>

		<form method="POST" action="?/report" use:enhance class="space-y-4">
			{#if postId}
				<input type="hidden" name="post_id" value={postId} />
			{/if}
			{#if commentId}
				<input type="hidden" name="comment_id" value={commentId} />
			{/if}

			<div class="space-y-2">
				<Label>신고 사유</Label>
				<Select.Root type="single">
					<Select.Trigger class="w-full">
						<Select.Value placeholder="사유를 선택하세요" />
					</Select.Trigger>
					<Select.Content>
						{#each reasons as r}
							<Select.Item value={r.value}>{r.label}</Select.Item>
						{/each}
					</Select.Content>
				</Select.Root>
				<input type="hidden" name="reason" bind:value={reason} />
			</div>

			<div class="space-y-2">
				<Label for="description">상세 설명 (선택)</Label>
				<Textarea
					id="description"
					name="description"
					bind:value={description}
					placeholder="신고 사유를 자세히 설명해주세요..."
					rows={4}
				/>
			</div>

			<Dialog.Footer>
				<Button type="button" variant="outline" onclick={() => open = false}>
					취소
				</Button>
				<Button type="submit" variant="destructive">
					신고하기
				</Button>
			</Dialog.Footer>
		</form>
	</Dialog.Content>
</Dialog.Root>
