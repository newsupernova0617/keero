<script lang="ts">
	import { onMount } from 'svelte'

	interface Props {
		unitId: string // 애드포스트 유닛 ID
		width?: number
		height?: number
		className?: string
	}

	let { unitId, width = 300, height = 250, className = '' }: Props = $props()

	let adContainer: HTMLDivElement

	onMount(() => {
		// 네이버 애드포스트 스크립트 로드
		if (typeof window !== 'undefined' && !(window as any)._naverAdPost) {
			const script = document.createElement('script')
			script.src = 'https://ssl.pstatic.net/tveta/libs/ads/mobile/naverAdPost-1.0.0.js'
			script.async = true
			document.head.appendChild(script)
		}

		// 광고 초기화
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
		<!-- 네이버 애드포스트 광고 영역 -->
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
