<script lang="ts">
	import './layout.css';
	import favicon from '$lib/assets/favicon.svg';
	import { invalidate } from '$app/navigation'
	import { onMount } from 'svelte'
	import type { LayoutData } from './$types'
	import { Button } from '$lib/components/ui/button'
	import { Input } from '$lib/components/ui/input'
	import AdSense from '$lib/components/ads/AdSense.svelte'
	import AdPost from '$lib/components/ads/AdPost.svelte'
	import { AD_CONFIG } from '$lib/config/ads'

	let { children, data }: { children: any; data: LayoutData } = $props();

	let { supabase, session, user } = $derived(data)

	onMount(() => {
		const { data: authData } = supabase.auth.onAuthStateChange((_, newSession) => {
			if (newSession?.expires_at !== session?.expires_at) {
				invalidate('supabase:auth')
			}
		})

		return () => authData.subscription.unsubscribe()
	})
</script>

<svelte:head><link rel="icon" href={favicon} /></svelte:head>

<div class="min-h-screen bg-background">
	<!-- Header -->
	<header class="border-b bg-card">
		<div class="mx-auto max-w-7xl px-4 py-4">
			<div class="flex items-center justify-between gap-4">
				<a href="/" class="text-2xl font-bold">유머 게시판</a>

				<!-- 검색바 -->
				<form method="GET" action="/search" class="hidden flex-1 max-w-md md:flex">
					<Input
						type="text"
						name="q"
						placeholder="검색..."
						class="w-full"
					/>
				</form>

				<nav class="flex items-center gap-4">
					{#if session}
						<span class="text-sm text-muted-foreground">
							{user?.email}
						</span>
						<form method="POST" action="/auth/signout">
							<Button type="submit" variant="outline" size="sm">
								로그아웃
							</Button>
						</form>
					{:else}
						<Button href="/auth/login" size="sm">
							로그인
						</Button>
					{/if}
				</nav>
			</div>
		</div>
	</header>

	<!-- 헤더 하단 배너 광고 -->
	{#if AD_CONFIG.adsense.enabled}
		<AdSense slot={AD_CONFIG.adsense.slots.header} format="horizontal" className="mx-auto max-w-7xl" />
	{:else if AD_CONFIG.adpost.enabled}
		<div class="mx-auto max-w-7xl px-4 py-2">
			<AdPost unitId={AD_CONFIG.adpost.units.header} width={728} height={90} />
		</div>
	{/if}

	<!-- Main Content -->
	<main class="mx-auto max-w-7xl px-4 py-8">
		{@render children()}
	</main>

	<!-- 푸터 상단 배너 광고 -->
	{#if AD_CONFIG.adsense.enabled}
		<AdSense slot={AD_CONFIG.adsense.slots.footer} format="horizontal" className="mx-auto max-w-7xl" />
	{:else if AD_CONFIG.adpost.enabled}
		<div class="mx-auto max-w-7xl px-4 py-2">
			<AdPost unitId={AD_CONFIG.adpost.units.footer} width={728} height={90} />
		</div>
	{/if}
</div>

