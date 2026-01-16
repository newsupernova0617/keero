<script lang="ts">
	import { onMount } from 'svelte'
	import { browser } from '$app/environment'
	import { env } from '$env/dynamic/public'

	// 환경 변수에서 GA ID 가져오기
	const gaId = env.PUBLIC_GA_MEASUREMENT_ID

	onMount(() => {
		if (!browser || !gaId) return

		// gtag 함수 정의
		;(window as any).dataLayer = (window as any).dataLayer || []
		function gtag(...args: any[]) {
			;(window as any).dataLayer.push(arguments)
		}
		;(window as any).gtag = gtag

		gtag('js', new Date())
		gtag('config', gaId)

		// GA 스크립트 동적 로드
		const script = document.createElement('script')
		script.async = true
		script.src = `https://www.googletagmanager.com/gtag/js?id=${gaId}`
		document.head.appendChild(script)
	})
</script>

<!-- 
	사용법:
	1. .env 파일에 PUBLIC_GA_MEASUREMENT_ID=G-XXXXXXXXXX 추가
	2. +layout.svelte에서 이 컴포넌트 import 후 사용
	
	예시:
	<script>
		import GoogleAnalytics from '$lib/components/GoogleAnalytics.svelte'
	</script>
	
	<GoogleAnalytics />
-->
