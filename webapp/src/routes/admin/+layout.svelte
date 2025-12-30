<script lang="ts">
	import { goto } from '$app/navigation'
	import { onMount } from 'svelte'
	import * as Card from '$lib/components/ui/card'
	import { Button } from '$lib/components/ui/button'
	import { Input } from '$lib/components/ui/input'

	let password = $state('')
	let error = $state('')
	let isAuthenticated = $state(false)

	onMount(() => {
		// 세션 스토리지에서 인증 상태 확인
		const auth = sessionStorage.getItem('admin_auth')
		if (auth === 'true') {
			isAuthenticated = true
		}
	})

	async function handleSubmit() {
		error = ''

		// API로 비밀번호 검증
		const response = await fetch('/api/admin/verify-password', {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ password })
		})

		if (response.ok) {
			sessionStorage.setItem('admin_auth', 'true')
			isAuthenticated = true
		} else {
			error = '비밀번호가 올바르지 않습니다.'
			password = ''
		}
	}

	function handleKeydown(e: KeyboardEvent) {
		if (e.key === 'Enter') {
			handleSubmit()
		}
	}
</script>

{#if !isAuthenticated}
	<div class="flex min-h-screen items-center justify-center bg-muted/50">
		<Card.Root class="w-full max-w-md">
			<Card.Header class="text-center">
				<Card.Title class="text-2xl">🔒 Admin 인증</Card.Title>
				<Card.Description>관리자 비밀번호를 입력하세요</Card.Description>
			</Card.Header>

			<Card.Content class="space-y-4">
				<div class="space-y-2">
					<Input
						type="password"
						placeholder="비밀번호"
						bind:value={password}
						onkeydown={handleKeydown}
						autofocus
					/>
					{#if error}
						<p class="text-sm text-destructive">{error}</p>
					{/if}
				</div>

				<Button onclick={handleSubmit} class="w-full">
					인증
				</Button>
			</Card.Content>
		</Card.Root>
	</div>
{:else}
	<slot />
{/if}
