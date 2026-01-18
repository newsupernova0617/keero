<script lang="ts">
	import './layout.css';
	import { invalidate } from '$app/navigation'
	import { onMount } from 'svelte'
	import type { LayoutData } from './$types'
	import { Button } from '$lib/components/ui/button'
	import { Input } from '$lib/components/ui/input'
	import { Search } from '@lucide/svelte'
	import AdSense from '$lib/components/ads/AdSense.svelte'
	import AdPost from '$lib/components/ads/AdPost.svelte'
	import AdFit from '$lib/components/ads/AdFit.svelte'
	import { AD_CONFIG } from '$lib/config/ads'
	import DarkModeToggle from '$lib/components/DarkModeToggle.svelte'
	import Footer from '$lib/components/Footer.svelte'
	import MobileNav from '$lib/components/MobileNav.svelte'
	import UserMenu from '$lib/components/UserMenu.svelte'
	import GoogleAnalytics from '$lib/components/GoogleAnalytics.svelte'

	let { children, data }: { children: any; data: LayoutData } = $props();

	let { supabase, session, user } = $derived(data)

	onMount(() => {
		const { data: authData } = supabase.auth.onAuthStateChange(async (event, _session) => {
			/**
			 * We only trust the user object from getUser().
			 * The _session object from onAuthStateChange is used only to trigger a re-validation
			 * when the auth state actually changes.
			 */
			if (event === 'SIGNED_IN' || event === 'SIGNED_OUT' || event === 'TOKEN_REFRESHED') {
				const { data: { user }, error } = await supabase.auth.getUser()
				
				if (error || !user) {
					if (session) invalidate('supabase:auth')
				} else {
					invalidate('supabase:auth')
				}
			}
		})

		return () => authData.subscription.unsubscribe()
	})
</script>

<!-- Google Analytics -->
<GoogleAnalytics />

<div class="flex min-h-screen flex-col bg-background">
	<!-- Header -->
	<header class="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
		<div class="mx-auto max-w-7xl px-4 py-4">
			<div class="flex items-center justify-between gap-4">
				<!-- Logo + Mobile Menu -->
				<div class="flex items-center gap-3">
					<MobileNav {session} {user} />
					<a href="/" class="flex items-center gap-2">
						<img src="/logo.png" alt="KEERO Logo" class="h-8 w-8 rounded-lg" />
						<span class="text-2xl font-bold bg-gradient-to-r from-primary to-primary/60 bg-clip-text text-transparent">
							KEERO
						</span>
					</a>
				</div>

				<!-- Desktop Search -->
				<form method="GET" action="/search" class="hidden flex-1 max-w-md md:flex">
					<div class="relative w-full">
						<Search class="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
						<Input
							type="text"
							name="q"
							placeholder="검색..."
							class="w-full pl-10"
						/>
					</div>
				</form>

				<!-- Desktop Navigation -->
				<nav class="hidden items-center gap-2 md:flex">
					<DarkModeToggle />
					
					{#if session}
						<UserMenu {user} />
					{:else}
						<Button href="/auth/login" size="sm">
							로그인
						</Button>
					{/if}
				</nav>
			</div>

			<!-- Mobile Search -->
			<form method="GET" action="/search" class="mt-4 md:hidden">
				<div class="relative w-full">
					<Search class="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
					<Input
						type="text"
						name="q"
						placeholder="검색..."
						class="w-full pl-10"
					/>
				</div>
			</form>
		</div>
	</header>

	<!-- Header Banner Ad -->
	{#if AD_CONFIG.adsense.enabled}
		<AdSense slot={AD_CONFIG.adsense.slots.header} format="horizontal" className="mx-auto max-w-7xl" />
	{:else if AD_CONFIG.adpost.enabled}
		<div class="mx-auto max-w-7xl px-4 py-2">
			<AdPost unitId={AD_CONFIG.adpost.units.header} width={728} height={90} />
		</div>
	{:else if AD_CONFIG.adfit.enabled}
		<!-- 데스크톱: 728x90 -->
		<div class="hidden md:flex mx-auto max-w-7xl px-4 py-2 justify-center">
			<AdFit unit={AD_CONFIG.adfit.units.headerDesktop} width={728} height={90} />
		</div>
		<!-- 모바일: 320x100 -->
		<div class="flex md:hidden justify-center px-4 py-2">
			<AdFit unit={AD_CONFIG.adfit.units.headerMobile} width={320} height={100} />
		</div>
	{/if}

	<!-- Main Content -->
	<main class="mx-auto w-full max-w-7xl flex-1 px-4 py-8">
		{@render children()}
	</main>

	<!-- Footer Banner Ad -->
	{#if AD_CONFIG.adsense.enabled}
		<AdSense slot={AD_CONFIG.adsense.slots.footer} format="horizontal" className="mx-auto max-w-7xl" />
	{:else if AD_CONFIG.adpost.enabled}
		<div class="mx-auto max-w-7xl px-4 py-2">
			<AdPost unitId={AD_CONFIG.adpost.units.footer} width={728} height={90} />
		</div>
	{:else if AD_CONFIG.adfit.enabled}
		<!-- 데스크톱: 300x250 (임시) -->
		<div class="hidden md:flex mx-auto max-w-7xl px-4 py-2 justify-center">
			<AdFit unit={AD_CONFIG.adfit.units.footerDesktop} width={300} height={250} />
		</div>
		<!-- 모바일: 300x250 (임시) -->
		<div class="flex md:hidden justify-center px-4 py-2">
			<AdFit unit={AD_CONFIG.adfit.units.footerMobile} width={300} height={250} />
		</div>
	{/if}

	<!-- Footer -->
	<Footer />
</div>
