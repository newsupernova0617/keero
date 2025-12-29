<script lang="ts">
	import { onMount } from 'svelte'
	import { Moon, Sun } from '@lucide/svelte'

	let isDark = $state(false)

	onMount(() => {
		// 시스템 설정 또는 저장된 설정 확인
		const stored = localStorage.getItem('theme')
		if (stored) {
			isDark = stored === 'dark'
		} else {
			// 시스템 설정 따르기
			isDark = window.matchMedia('(prefers-color-scheme: dark)').matches
		}
		
		// 초기 테마 적용
		updateTheme()
	})

	function updateTheme() {
		if (isDark) {
			document.documentElement.classList.add('dark')
		} else {
			document.documentElement.classList.remove('dark')
		}
		localStorage.setItem('theme', isDark ? 'dark' : 'light')
	}

	function toggleTheme() {
		isDark = !isDark
		updateTheme()
	}
</script>

<button
	onclick={toggleTheme}
	class="flex items-center gap-2 rounded-lg px-3 py-2 text-sm transition-colors hover:bg-accent"
	aria-label="다크모드 토글"
>
	{#if isDark}
		<Moon class="h-4 w-4" />
		<span class="hidden sm:inline">다크</span>
	{:else}
		<Sun class="h-4 w-4" />
		<span class="hidden sm:inline">라이트</span>
	{/if}
</button>
