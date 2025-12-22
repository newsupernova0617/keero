<script lang="ts">
	import { enhance } from '$app/forms'
	import { Button } from '$lib/components/ui/button'
	import { ThumbsUp } from '@lucide/svelte'

	let {
		likeCount,
		userLiked,
		session
	}: {
		likeCount: number
		userLiked: boolean
		session: any
	} = $props()
</script>

<form method="POST" action="?/toggleLike" use:enhance>
	<Button 
		type="submit"
		variant={userLiked ? 'default' : 'outline'} 
		size="sm" 
		class="gap-2"
		disabled={!session}
	>
		<ThumbsUp class="h-4 w-4 {userLiked ? 'fill-current' : ''}" />
		좋아요 {likeCount > 0 ? `(${likeCount})` : ''}
	</Button>
</form>
