<script lang="ts">
	import { X, ChevronLeft, ChevronRight } from '@lucide/svelte'
	import { Button } from '$lib/components/ui/button'

	let {
		images,
		initialIndex = 0
	}: {
		images: Array<{ r2_url: string; media_type?: string }>
		initialIndex?: number
	} = $props()

	let isOpen = $state(false)
	let currentIndex = $state(initialIndex)

	export function open(index: number = 0) {
		currentIndex = index
		isOpen = true
		document.body.style.overflow = 'hidden'
	}

	function close() {
		isOpen = false
		document.body.style.overflow = ''
	}

	function next() {
		currentIndex = (currentIndex + 1) % images.length
	}

	function prev() {
		currentIndex = (currentIndex - 1 + images.length) % images.length
	}

	function handleKeydown(e: KeyboardEvent) {
		if (!isOpen) return
		
		if (e.key === 'Escape') close()
		if (e.key === 'ArrowRight') next()
		if (e.key === 'ArrowLeft') prev()
	}
</script>

<svelte:window onkeydown={handleKeydown} />

{#if isOpen}
	<!-- Backdrop -->
	<div
		class="fixed inset-0 z-50 bg-black/90"
		onclick={close}
		role="button"
		tabindex="-1"
	></div>

	<!-- Gallery -->
	<div class="fixed inset-0 z-50 flex items-center justify-center p-4">
		<!-- Close Button -->
		<Button
			variant="ghost"
			size="icon"
			class="absolute right-4 top-4 text-white hover:bg-white/20"
			onclick={close}
		>
			<X class="h-6 w-6" />
		</Button>

		<!-- Previous Button -->
		{#if images.length > 1}
			<Button
				variant="ghost"
				size="icon"
				class="absolute left-4 text-white hover:bg-white/20"
				onclick={prev}
			>
				<ChevronLeft class="h-8 w-8" />
			</Button>
		{/if}

		<!-- Image -->
		<div class="relative max-h-[90vh] max-w-[90vw]">
			<img
				src={images[currentIndex].r2_url}
				alt="이미지 {currentIndex + 1}"
				class="max-h-[90vh] max-w-[90vw] object-contain"
				onclick={(e) => e.stopPropagation()}
			/>
			
			<!-- Image Counter -->
			{#if images.length > 1}
				<div class="absolute bottom-4 left-1/2 -translate-x-1/2 rounded-full bg-black/70 px-4 py-2 text-sm text-white">
					{currentIndex + 1} / {images.length}
				</div>
			{/if}
		</div>

		<!-- Next Button -->
		{#if images.length > 1}
			<Button
				variant="ghost"
				size="icon"
				class="absolute right-4 text-white hover:bg-white/20"
				onclick={next}
			>
				<ChevronRight class="h-8 w-8" />
			</Button>
		{/if}
	</div>
{/if}
