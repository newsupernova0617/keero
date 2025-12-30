<script lang="ts">
	import { onMount } from 'svelte'
	import { PUBLIC_ADSENSE_ENABLED } from '$env/static/public'

	interface Props {
		slot: string // 광고 슬롯 ID
		format?: 'auto' | 'rectangle' | 'horizontal' | 'vertical'
		responsive?: boolean
		className?: string
	}

	let { slot, format = 'auto', responsive = true, className = '' }: Props = $props()

	let adContainer: HTMLElement
	
	// 환경변수로 AdSense 활성화 여부 확인
	const isAdSenseEnabled = PUBLIC_ADSENSE_ENABLED === '1'

	onMount(() => {
		// AdSense가 비활성화되어 있으면 로드하지 않음
		if (!isAdSenseEnabled) {
			console.log('AdSense is disabled (PUBLIC_ADSENSE_ENABLED=0)')
			return
		}

		// AdSense 스크립트 로드
		if (typeof window !== 'undefined' && !(window as any).adsbygoogle) {
			const script = document.createElement('script')
			script.src = 'https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-XXXXXXXXXXXXXXXX'
			script.async = true
			script.crossOrigin = 'anonymous'
			document.head.appendChild(script)
		}

		// 광고 초기화
		try {
			;((window as any).adsbygoogle = (window as any).adsbygoogle || []).push({})
		} catch (e) {
			console.error('AdSense error:', e)
		}
	})
</script>

{#if isAdSenseEnabled}
	<div class="ad-wrapper {className}">
		<ins
			bind:this={adContainer}
			class="adsbygoogle"
			style="display:block"
			data-ad-client="ca-pub-XXXXXXXXXXXXXXXX"
			data-ad-slot={slot}
			data-ad-format={format}
			data-full-width-responsive={responsive}
		></ins>
	</div>
{/if}

<style>
	.ad-wrapper {
		margin: 1rem 0;
		text-align: center;
	}

	.adsbygoogle {
		display: block;
	}
</style>
