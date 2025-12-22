<script lang="ts">
	import { onMount } from 'svelte'

	interface Props {
		unitId: string // ? ë“œ?¬ìŠ¤??? ë‹› ID
		width?: number
		height?: number
		className?: string
	}

	let { unitId, width = 300, height = 250, className = '' }: Props = $props()

	let adContainer: HTMLDivElement

	onMount(() => {
		// ?¤ì´ë²?? ë“œ?¬ìŠ¤???¤í¬ë¦½íŠ¸ ë¡œë“œ
		if (typeof window !== 'undefined' && !(window as any)._naverAdPost) {
			const script = document.createElement('script')
			script.src = 'https://ssl.pstatic.net/tveta/libs/ads/mobile/naverAdPost-1.0.0.js'
			script.async = true
			document.head.appendChild(script)
		}

		// ê´‘ê³  ì´ˆê¸°??
		try {
			if ((window as any)._naverAdPost) {
				;(window as any)._naverAdPost.push({
					unitId: unitId,
					width: width,
					height: height
				})
			}
		} catch (e) {
			console.error('AdPost error:', e)
		}
	})
</script>

<div class="ad-wrapper {className}">
	<div bind:this={adContainer} id="naverAdPost-{unitId}" style="width:{width}px;height:{height}px">
		<!-- ?¤ì´ë²?? ë“œ?¬ìŠ¤??ê´‘ê³  ?ì—­ -->
	</div>
</div>

<style>
	.ad-wrapper {
		margin: 1rem 0;
		text-align: center;
		display: flex;
		justify-content: center;
	}
</style>
