<script lang="ts">
	import { enhance } from '$app/forms'
	import { Button } from '$lib/components/ui/button'
	import { Textarea } from '$lib/components/ui/textarea'
	import * as Avatar from '$lib/components/ui/avatar'
	import { Reply, Edit, Trash2 } from '@lucide/svelte'

	let {
		comment,
		currentUserId,
		session,
		replyingTo,
		editingComment,
		replyContent = $bindable(),
		editContent = $bindable(),
		onToggleReply,
		onToggleEdit,
		onCancelEdit
	}: {
		comment: any
		currentUserId: number | null
		session: any
		replyingTo: number | null
		editingComment: number | null
		replyContent: string
		editContent: string
		onToggleReply: (id: number) => void
		onToggleEdit: (id: number, content: string) => void
		onCancelEdit: () => void
	} = $props()

	let isOwner = $derived(currentUserId !== null && comment.user_id === currentUserId)
	let isEditing = $derived(editingComment === comment.id)
	let isReplying = $derived(replyingTo === comment.id)
</script>

<div class="flex gap-3">
	<Avatar.Root class="h-10 w-10">
		<Avatar.Fallback class="bg-primary/10 text-primary">
			{comment.user_display_name?.[0] || '?'}
		</Avatar.Fallback>
	</Avatar.Root>
	
	<div class="flex-1 space-y-2">
		{#if isEditing}
			<!-- 수정 폼 -->
			<form method="POST" action="?/editComment" use:enhance class="space-y-2">
				<input type="hidden" name="comment_id" value={comment.id} />
				<Textarea
					name="content"
					bind:value={editContent}
					rows={3}
				/>
				<div class="flex justify-end gap-2">
					<Button
						type="button"
						variant="ghost"
						size="sm"
						onclick={onCancelEdit}
					>
						취소
					</Button>
					<Button type="submit" size="sm">
						수정 완료
					</Button>
				</div>
			</form>
		{:else}
			<!-- 댓글 내용 -->
			<div class="space-y-1">
				<div class="flex items-center gap-2">
					<span class="font-medium">{comment.user_display_name}</span>
					<span class="text-xs text-muted-foreground">
						{new Date(comment.created_at).toLocaleString('ko-KR')}
					</span>
					{#if comment.updated_at && comment.updated_at !== comment.created_at}
						<span class="text-xs text-muted-foreground">(수정됨)</span>
					{/if}
				</div>
				<p class="text-sm {comment.is_deleted ? 'text-muted-foreground italic' : ''}">
					{comment.content}
				</p>
			</div>
			
			<!-- 액션 버튼 -->
			{#if session && !comment.is_deleted}
				<div class="flex items-center gap-2">
					<!-- 답글 버튼 -->
					<Button
						variant="ghost"
						size="sm"
						class="h-auto gap-1 p-0 text-xs hover:bg-transparent"
						onclick={() => onToggleReply(comment.id)}
					>
						<Reply class="h-3 w-3" />
						{isReplying ? '취소' : '답글'}
					</Button>
					
					<!-- 수정/삭제 버튼 (본인만) -->
					{#if isOwner}
						<Button
							variant="ghost"
							size="sm"
							class="h-auto gap-1 p-0 text-xs hover:bg-transparent"
							onclick={() => onToggleEdit(comment.id, comment.content)}
						>
							<Edit class="h-3 w-3" />
							수정
						</Button>
						
						<form method="POST" action="?/deleteComment" use:enhance class="inline">
							<input type="hidden" name="comment_id" value={comment.id} />
							<Button
								type="submit"
								variant="ghost"
								size="sm"
								class="h-auto gap-1 p-0 text-xs text-destructive hover:bg-transparent hover:text-destructive"
								onclick={(e) => {
									if (!confirm('정말 삭제하시겠습니까?')) {
										e.preventDefault()
									}
								}}
							>
								<Trash2 class="h-3 w-3" />
								삭제
							</Button>
						</form>
					{/if}
				</div>
			{/if}
		{/if}
	</div>
</div>

<!-- 답글 작성 폼 -->
{#if isReplying}
	<form method="POST" action="?/comment" use:enhance class="ml-12 space-y-2">
		<input type="hidden" name="parent_comment_id" value={comment.id} />
		<Textarea
			name="content"
			bind:value={replyContent}
			placeholder="답글을 입력하세요..."
			rows={2}
		/>
		<div class="flex justify-end gap-2">
			<Button
				type="button"
				variant="ghost"
				size="sm"
				onclick={() => onToggleReply(comment.id)}
			>
				취소
			</Button>
			<Button type="submit" size="sm">
				답글 작성
			</Button>
		</div>
	</form>
{/if}

<!-- 대댓글 -->
{#if comment.replies && comment.replies.length > 0}
	<div class="ml-12 space-y-3 border-l-2 pl-4">
		{#each comment.replies as reply}
			<div class="flex gap-3">
				<Avatar.Root class="h-8 w-8">
					<Avatar.Fallback class="bg-muted text-xs">
						{reply.user_display_name?.[0] || '?'}
					</Avatar.Fallback>
				</Avatar.Root>
				
				<div class="flex-1 space-y-1">
					<div class="flex items-center gap-2">
						<span class="text-sm font-medium">{reply.user_display_name}</span>
						<span class="text-xs text-muted-foreground">
							{new Date(reply.created_at).toLocaleString('ko-KR')}
						</span>
						{#if reply.updated_at && reply.updated_at !== reply.created_at}
							<span class="text-xs text-muted-foreground">(수정됨)</span>
						{/if}
					</div>
					<p class="text-sm {reply.is_deleted ? 'text-muted-foreground italic' : ''}">
						{reply.content}
					</p>
				</div>
			</div>
		{/each}
	</div>
{/if}
