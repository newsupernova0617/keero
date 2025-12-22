<script lang="ts">
	import { enhance } from '$app/forms'
	import { Button } from '$lib/components/ui/button'
	import { Bookmark } from '@lucide/svelte'

	let {
		postId,
		isBookmarked = false,
		session
	}: {
		postId: number
		isBookmarked?: boolean
		session: any
	} = $props()
</script>

<form method="POST" action="?/toggleBookmark" use:enhance>
	<input type="hidden" name="post_id" value={postId} />
	<Button 
		type="submit"
		variant={isBookmarked ? 'default' : 'outline'}
		size="sm"
		class="gap-2"
		disabled={!session}
	>
		<Bookmark class="h-4 w-4 {isBookmarked ? 'fill-current' : ''}" />
		{isBookmarked ? '북마크됨' : '북마크'}
	</Button>
</form>
