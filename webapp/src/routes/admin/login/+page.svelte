<script lang="ts">
	import { enhance } from '$app/forms'
	import { Button } from '$lib/components/ui/button'
	import { Input } from '$lib/components/ui/input'
	import * as Card from '$lib/components/ui/card'
	import type { ActionData } from './$types'

	let { form }: { form: ActionData } = $props()
</script>

<svelte:head>
	<title>관리자 로그인</title>
</svelte:head>

<div class="flex min-h-screen items-center justify-center bg-muted/50 p-4">
	<Card.Root class="w-full max-w-md">
		<Card.Header>
			<Card.Title class="text-2xl">관리자 로그인</Card.Title>
			<Card.Description>관리자 비밀번호를 입력하세요</Card.Description>
		</Card.Header>
		
		<form method="POST" use:enhance>
			<Card.Content class="space-y-4">
				{#if form?.error}
					<div class="rounded-lg bg-destructive/10 p-3 text-sm text-destructive">
						{form.error}
					</div>
				{/if}
				
				<div class="space-y-2">
					<label for="password" class="text-sm font-medium">비밀번호</label>
					<Input
						id="password"
						name="password"
						type="password"
						placeholder="관리자 비밀번호 입력"
						required
						autofocus
					/>
				</div>
			</Card.Content>
			
			<Card.Footer>
				<Button type="submit" class="w-full">로그인</Button>
			</Card.Footer>
		</form>
	</Card.Root>
</div>
