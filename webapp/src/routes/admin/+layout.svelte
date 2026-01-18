<script lang="ts">
	import { enhance } from '$app/forms'
	import * as Card from '$lib/components/ui/card'
	import { Button } from '$lib/components/ui/button'
	import { Input } from '$lib/components/ui/input'
	import type { LayoutData } from './$types'

	let { data, children }: { data: LayoutData; children: any } = $props()
	
	let password = $state('')
	let error = $state('')
</script>

{#if !data.authenticated}
	<div class="flex min-h-screen items-center justify-center bg-muted/50">
		<Card.Root class="w-full max-w-md">
			<Card.Header class="text-center">
				<Card.Title class="text-2xl">🔒 Admin 인증</Card.Title>
				<Card.Description>관리자 비밀번호를 입력하세요</Card.Description>
			</Card.Header>

			<form method="POST" action="/admin" use:enhance={() => {
				return async ({ result }) => {
					if (result.type === 'failure') {
						error = '비밀번호가 올바르지 않습니다.'
						password = ''
					} else if (result.type === 'success') {
						// 페이지 새로고침
						window.location.reload()
					}
				}
			}}>
				<Card.Content class="space-y-4">
					<div class="space-y-2">
						<Input
							type="password"
							name="password"
							placeholder="비밀번호"
							bind:value={password}
							autofocus
							required
						/>
						{#if error}
							<p class="text-sm text-destructive">{error}</p>
						{/if}
					</div>

					<Button type="submit" class="w-full">
						인증
					</Button>
				</Card.Content>
			</form>
		</Card.Root>
	</div>
{:else}
	{@render children()}
{/if}
