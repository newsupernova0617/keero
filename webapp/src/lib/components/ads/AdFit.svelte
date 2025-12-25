<script lang="ts">
	import { onMount } from 'svelte'

	let { unit, width = 728, height = 90 }: { unit: string; width?: number; height?: number } = $props()

	let adContainer: HTMLElement

	onMount(() => {
		try {
			// 카카오 애드핏 스크립트 로드
			if (typeof window !== 'undefined' && !(window as any).adfit) {
				const script = document.createElement('script')
				script.src = 'https://t1.daumcdn.net/kas/static/ba.min.js'
				script.async = true
				document.head.appendChild(script)

				script.onload = () => {
					initAd()
				}
			} else {
				initAd()
			}
		} catch (e) {
			console.error('AdFit error:', e)
		}
	})

	function initAd() {
		// 광고 초기화는 스크립트가 자동으로 처리
	}
</script>

<ins
	bind:this={adContainer}
	class="kakao_ad_area"
	style="display:none; width:100%; max-width:{width}px;"
	data-ad-unit={unit}
	data-ad-width={width}
	data-ad-height={height}
></ins>
