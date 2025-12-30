<script lang="ts">
	import { goto } from '$app/navigation'
	import type { PageData } from './$types'
	import * as Card from '$lib/components/ui/card'
	import { Button } from '$lib/components/ui/button'

	let { data }: { data: PageData } = $props()

	let { supabase, session } = $derived(data)

	// 이미 로그인되어 있으면 리다이렉트
	$effect(() => {
		if (session) {
			// URL에서 redirect 파라미터 확인
			const params = new URLSearchParams(window.location.search)
			const redirectTo = params.get('redirect') || '/'
			goto(redirectTo)
		}
	})

	async function signInWithGoogle() {
		const { error } = await supabase.auth.signInWithOAuth({
			provider: 'google',
			options: {
				redirectTo: `${location.origin}/auth/callback`
			}
		})
		if (error) console.error('Error logging in:', error.message)
	}

	async function signInWithKakao() {
		const { error } = await supabase.auth.signInWithOAuth({
			provider: 'kakao',
			options: {
				redirectTo: `${location.origin}/auth/callback`
			}
		})
		if (error) console.error('Error logging in:', error.message)
	}
</script>

<div class="flex min-h-screen items-center justify-center">
	<Card.Root class="w-full max-w-md">
		<Card.Header class="text-center">
			<Card.Title class="text-3xl">로그인</Card.Title>
			<Card.Description>소셜 계정으로 간편하게 로그인하세요</Card.Description>
		</Card.Header>

		<Card.Content class="space-y-4">
			<Button
				onclick={signInWithGoogle}
				variant="outline"
				class="w-full justify-center gap-3"
			>
				<svg class="h-5 w-5" viewBox="0 0 24 24">
					<path
						fill="currentColor"
						d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
					/>
					<path
						fill="currentColor"
						d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
					/>
					<path
						fill="currentColor"
						d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
					/>
					<path
						fill="currentColor"
						d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
					/>
				</svg>
				Google로 계속하기
			</Button>

			<Button
				onclick={signInWithKakao}
				class="w-full justify-center gap-3 bg-[#FEE500] text-[#000000] hover:bg-[#FDD835]"
			>
				<svg class="h-5 w-5" viewBox="0 0 24 24" fill="currentColor">
					<path
						d="M12 3C6.477 3 2 6.253 2 10.253c0 2.625 1.771 4.929 4.429 6.253-.184.68-.607 2.261-.697 2.607-.11.423.155.418.327.304.138-.092 2.181-1.456 3.118-2.082.611.088 1.239.133 1.879.133 5.523 0 10-3.253 10-7.253S17.523 3 12 3z"
					/>
				</svg>
				카카오로 계속하기
			</Button>

			<p class="text-center text-xs text-muted-foreground">
				로그인하면 <a href="/terms" class="underline">이용약관</a> 및
				<a href="/privacy" class="underline">개인정보처리방침</a>에 동의하는 것으로 간주됩니다.
			</p>
		</Card.Content>
	</Card.Root>
</div>
