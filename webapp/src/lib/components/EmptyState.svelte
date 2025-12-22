<script lang="ts">
	import * as Card from '$lib/components/ui/card'
	import { Button } from '$lib/components/ui/button'
	import { Inbox } from '@lucide/svelte'
	
	let { 
		title = '게시글???�습?�다',
		description = '?�직 ?�롤링된 게시글???�습?�다.',
		actionLabel,
		actionHref
	}: {
		title?: string
		description?: string
		actionLabel?: string
		actionHref?: string
	} = $props()
</script>

<Card.Root>
	<Card.Content class="flex flex-col items-center justify-center p-12 text-center">
		<div class="mb-4 rounded-full bg-muted p-4">
			<Inbox class="h-10 w-10 text-muted-foreground" />
		</div>
		<h3 class="mb-2 text-lg font-semibold">{title}</h3>
		<p class="mb-6 text-sm text-muted-foreground">
			{description}
		</p>
		{#if actionLabel && actionHref}
			<Button href={actionHref}>
				{actionLabel}
			</Button>
		{/if}
	</Card.Content>
</Card.Root>
