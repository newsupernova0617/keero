<script lang="ts">
	import { enhance } from '$app/forms'
	import { Button } from '$lib/components/ui/button'
	import { ThumbsUp } from '@lucide/svelte'

	let {
		commentId,
		likeCount = 0,
		userLiked = false,
		session
	}: {
		commentId: number
		likeCount?: number
		userLiked?: boolean
		session: any
	} = $props()
</script>

<form method="POST" action="?/toggleCommentLike" use:enhance class="inline">
	<input type="hidden" name="comment_id" value={commentId} />
	<Button 
		type="submit"
		variant="ghost"
		size="sm"
		class="h-auto gap-1 p-0 text-xs hover:bg-transparent"
		disabled={!session}
	>
		<ThumbsUp class="h-3 w-3 {userLiked ? 'fill-current' : ''}" />
		{#if likeCount > 0}
			<span>{likeCount}</span>
		{/if}
	</Button>
</form>
