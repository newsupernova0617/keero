<script lang="ts">
	import { onMount } from 'svelte'

	interface Props {
		slot: string // 광고 ?�롯 ID
		format?: 'auto' | 'rectangle' | 'horizontal' | 'vertical'
		responsive?: boolean
		className?: string
	}

	let { slot, format = 'auto', responsive = true, className = '' }: Props = $props()

	let adContainer: HTMLElement

	onMount(() => {
		// AdSense ?�크립트 로드
		if (typeof window !== 'undefined' && !(window as any).adsbygoogle) {
			const script = document.createElement('script')
			script.src = 'https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-XXXXXXXXXXXXXXXX'
			script.async = true
			script.crossOrigin = 'anonymous'
			document.head.appendChild(script)
		}

		// 광고 초기??
		try {
			;((window as any).adsbygoogle = (window as any).adsbygoogle || []).push({})
		} catch (e) {
			console.error('AdSense error:', e)
		}
	})
</script>

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

<style>
	.ad-wrapper {
		margin: 1rem 0;
		text-align: center;
	}

	.adsbygoogle {
		display: block;
	}
</style>
