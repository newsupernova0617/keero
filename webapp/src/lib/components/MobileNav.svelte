<script lang="ts">
	import * as Sheet from '$lib/components/ui/sheet'
	import { Button } from '$lib/components/ui/button'
	import { Separator } from '$lib/components/ui/separator'
	import { Menu, Home, Search, LogIn, LogOut, User } from '@lucide/svelte'
	
	let { session, user }: { session: any; user: any } = $props()
	let open = $state(false)
</script>

<Sheet.Root bind:open>
	<Sheet.Trigger>
		{#snippet child({ props })}
			<Button {...props} variant="ghost" size="icon" class="md:hidden">
				<Menu class="h-5 w-5" />
				<span class="sr-only">메뉴 열기</span>
			</Button>
		{/snippet}
	</Sheet.Trigger>
	<Sheet.Content side="left" class="w-[300px] sm:w-[400px]">
		<Sheet.Header>
			<Sheet.Title>메뉴</Sheet.Title>
		</Sheet.Header>
		
		<div class="mt-6 flex flex-col gap-4">
			<!-- Navigation Links -->
			<a
				href="/"
				onclick={() => (open = false)}
				class="flex items-center gap-3 rounded-lg px-3 py-2 text-sm transition-colors hover:bg-accent"
			>
				<Home class="h-4 w-4" />
				홈
			</a>
			
			<a
				href="/search"
				onclick={() => (open = false)}
				class="flex items-center gap-3 rounded-lg px-3 py-2 text-sm transition-colors hover:bg-accent"
			>
				<Search class="h-4 w-4" />
				검색
			</a>

			<Separator />

			<!-- User Section -->
			{#if session}
				<div class="flex items-center gap-3 px-3 py-2">
					<User class="h-4 w-4" />
					<span class="text-sm text-muted-foreground">{user?.email}</span>
				</div>
				
				<form method="POST" action="/auth/signout">
					<button
						type="submit"
						class="flex w-full items-center gap-3 rounded-lg px-3 py-2 text-sm transition-colors hover:bg-accent"
					>
						<LogOut class="h-4 w-4" />
						로그아웃
					</button>
				</form>
			{:else}
				<a
					href="/auth/login"
					onclick={() => (open = false)}
					class="flex items-center gap-3 rounded-lg px-3 py-2 text-sm transition-colors hover:bg-accent"
				>
					<LogIn class="h-4 w-4" />
					로그인
				</a>
			{/if}
		</div>
	</Sheet.Content>
</Sheet.Root>
