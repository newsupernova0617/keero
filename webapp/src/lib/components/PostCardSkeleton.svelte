<script lang="ts">
	import * as Card from '$lib/components/ui/card'
	import { Skeleton } from '$lib/components/ui/skeleton'
</script>

<Card.Root class="overflow-hidden">
	<!-- Image Skeleton -->
	<Skeleton class="aspect-video w-full" />
	
	<!-- Content Skeleton -->
	<Card.Content class="p-4 space-y-3">
		<!-- Title -->
		<Skeleton class="h-6 w-3/4" />
		<Skeleton class="h-6 w-1/2" />
		
		<!-- Meta -->
		<div class="flex items-center gap-2">
			<Skeleton class="h-5 w-16" />
			<Skeleton class="h-4 w-24" />
			<Skeleton class="h-4 w-12" />
		</div>
	</Card.Content>
</Card.Root>
