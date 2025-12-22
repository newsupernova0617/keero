<script lang="ts">
	import { onMount } from 'svelte'

	interface Props {
		unit: string // ?�드???�닛 ID
		width?: number
		height?: number
		className?: string
	}

	let { unit, width = 320, height = 100, className = '' }: Props = $props()

	let adContainer: HTMLDivElement

	onMount(() => {
		// 카카???�드???�크립트 로드
		if (typeof window !== 'undefined' && !(window as any).kakaoPixel) {
			const script = document.createElement('script')
			script.src = 'https://t1.daumcdn.net/kas/static/ba.min.js'
			script.async = true
			document.head.appendChild(script)
		}

		// 광고 초기??
		try {
			if (adContainer) {
				const ins = document.createElement('ins')
				ins.className = 'kakao_ad_area'
				ins.style.display = 'none'
				ins.setAttribute('data-ad-unit', unit)
				ins.setAttribute('data-ad-width', width.toString())
				ins.setAttribute('data-ad-height', height.toString())
				adContainer.appendChild(ins)

				const adScript = document.createElement('script')
				adScript.type = 'text/javascript'
				adScript.src = '//t1.daumcdn.net/kas/static/ba.min.js'
				adScript.async = true
				adContainer.appendChild(adScript)
			}
		} catch (e) {
			console.error('AdFit error:', e)
		}
	})
</script>

<div class="ad-wrapper {className}">
	<div bind:this={adContainer} class="adfit-container">
		<!-- 카카???�드??광고 ?�역 -->
	</div>
</div>

<style>
	.ad-wrapper {
		margin: 1rem 0;
		text-align: center;
		display: flex;
		justify-content: center;
	}

	.adfit-container {
		width: 100%;
		max-width: 320px;
	}
</style>
