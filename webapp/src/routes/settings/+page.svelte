<script lang="ts">
	import type { PageData } from './$types'
	import { enhance } from '$app/forms'
	import { onMount } from 'svelte'
	import * as Card from '$lib/components/ui/card'
	import { Button } from '$lib/components/ui/button'
	import { Input } from '$lib/components/ui/input'
	import { Label } from '$lib/components/ui/label'
	import * as Select from '$lib/components/ui/select'
	import { Switch } from '$lib/components/ui/switch'
	import { Separator } from '$lib/components/ui/separator'
	import { Bell, Moon, Globe, Trash2, Shield } from '@lucide/svelte'

	let { data, form }: { data: PageData; form: any } = $props()

	// Settings state
	let displayName = $state(data.dbUser?.display_name || data.user?.email?.split('@')[0] || '')
	let emailNotifications = $state(true)
	let isDark = $state(false)
	let language = $state('ko')

	// Update displayName when data changes (e.g., after form submission)
	$effect(() => {
		if (data.dbUser?.display_name) {
			displayName = data.dbUser.display_name
		}
	})

	// Dark mode
	onMount(() => {
		const stored = localStorage.getItem('theme')
		if (stored) {
			isDark = stored === 'dark'
		} else {
			isDark = window.matchMedia('(prefers-color-scheme: dark)').matches
		}
	})

	function updateTheme() {
		if (isDark) {
			document.documentElement.classList.add('dark')
		} else {
			document.documentElement.classList.remove('dark')
		}
		localStorage.setItem('theme', isDark ? 'dark' : 'light')
	}

	function toggleDarkMode() {
		isDark = !isDark
		updateTheme()
	}
</script>

<svelte:head>
	<title>설정 - 유머 게시판</title>
	<meta name="description" content="계정 설정" />
</svelte:head>

<div class="mx-auto max-w-4xl space-y-6">
	<!-- Header -->
	<div>
		<h1 class="text-3xl font-bold tracking-tight">설정</h1>
		<p class="mt-1 text-sm text-muted-foreground">
			계정 및 앱 설정을 관리하세요
		</p>
	</div>

	<!-- Profile Settings -->
	<Card.Root>
		<Card.Header>
			<Card.Title>프로필 설정</Card.Title>
			<Card.Description>공개 프로필 정보를 수정하세요</Card.Description>
		</Card.Header>
		<form method="POST" action="?/updateProfile" use:enhance>
			<Card.Content class="space-y-4">
				{#if form?.success}
					<div class="rounded-lg bg-green-50 p-3 text-sm text-green-800">
						✓ {form.message}
					</div>
				{/if}
				{#if form?.error}
					<div class="rounded-lg bg-red-50 p-3 text-sm text-red-800">
						✗ {form.error}
					</div>
				{/if}

				<div class="space-y-2">
					<Label for="display-name">표시 이름</Label>
					<Input
						id="display-name"
						name="display_name"
						type="text"
						bind:value={displayName}
						placeholder="사용자 이름"
					/>
					<p class="text-xs text-muted-foreground">
						다른 사용자에게 표시될 이름입니다.
					</p>
				</div>

				<div class="space-y-2">
					<Label for="email">이메일</Label>
					<Input
						id="email"
						type="email"
						value={data.user?.email}
						disabled
						class="bg-muted"
					/>
					<p class="text-xs text-muted-foreground">
						이메일은 변경할 수 없습니다.
					</p>
				</div>

				<Button type="submit">
					변경사항 저장
				</Button>
			</Card.Content>
		</form>
	</Card.Root>

	<!-- Notification Settings -->
	<Card.Root>
		<Card.Header>
			<Card.Title class="flex items-center gap-2">
				<Bell class="h-5 w-5" />
				알림 설정
			</Card.Title>
			<Card.Description>알림 수신 방법을 설정하세요</Card.Description>
		</Card.Header>
		<Card.Content class="space-y-4">
			<div class="flex items-center justify-between">
				<div class="space-y-0.5">
					<Label>이메일 알림</Label>
					<p class="text-xs text-muted-foreground">
						새 댓글이나 답글이 달렸을 때 이메일을 받습니다.
					</p>
				</div>
				<Switch bind:checked={emailNotifications} disabled />
			</div>

			<Separator />

			<div class="flex items-center justify-between">
				<div class="space-y-0.5">
					<Label>브라우저 알림</Label>
					<p class="text-xs text-muted-foreground">
						실시간 브라우저 알림을 받습니다.
					</p>
				</div>
				<Switch disabled />
			</div>

			<p class="text-xs text-muted-foreground">
				💡 알림 기능은 준비 중입니다.
			</p>
		</Card.Content>
	</Card.Root>

	<!-- Appearance Settings -->
	<Card.Root>
		<Card.Header>
			<Card.Title class="flex items-center gap-2">
				<Moon class="h-5 w-5" />
				외관 설정
			</Card.Title>
			<Card.Description>앱의 외관을 커스터마이즈하세요</Card.Description>
		</Card.Header>
		<Card.Content class="space-y-4">
			<div class="flex items-center justify-between">
				<div class="space-y-0.5">
					<Label>다크 모드</Label>
					<p class="text-xs text-muted-foreground">
						어두운 테마를 사용합니다.
					</p>
				</div>
				<Switch bind:checked={isDark} onCheckedChange={toggleDarkMode} />
			</div>
		</Card.Content>
	</Card.Root>

	<!-- Language Settings -->
	<Card.Root>
		<Card.Header>
			<Card.Title class="flex items-center gap-2">
				<Globe class="h-5 w-5" />
				언어 설정
			</Card.Title>
			<Card.Description>표시 언어를 선택하세요</Card.Description>
		</Card.Header>
		<Card.Content>
			<div class="space-y-2">
				<Label>언어</Label>
				<Select.Root type="single" disabled>
					<Select.Trigger class="w-full">
						<span>한국어</span>
					</Select.Trigger>
					<Select.Content>
						<Select.Item value="ko">한국어</Select.Item>
						<Select.Item value="en">English</Select.Item>
					</Select.Content>
				</Select.Root>
				<p class="text-xs text-muted-foreground">
					💡 다국어 지원은 준비 중입니다.
				</p>
			</div>
		</Card.Content>
	</Card.Root>

	<!-- Privacy & Security -->
	<Card.Root>
		<Card.Header>
			<Card.Title class="flex items-center gap-2">
				<Shield class="h-5 w-5" />
				개인정보 및 보안
			</Card.Title>
			<Card.Description>계정 보안 설정을 관리하세요</Card.Description>
		</Card.Header>
		<Card.Content class="space-y-4">
			<div class="space-y-2">
				<h4 class="text-sm font-medium">연결된 계정</h4>
				<div class="rounded-lg border p-3">
					<p class="text-sm">
						{data.user?.app_metadata?.provider || 'Email'} 계정으로 로그인됨
					</p>
					<p class="text-xs text-muted-foreground">
						{data.user?.email}
					</p>
				</div>
			</div>

			<Separator />

			<div class="space-y-2">
				<h4 class="text-sm font-medium">비밀번호 변경</h4>
				<Button variant="outline" disabled>
					비밀번호 변경 (준비 중)
				</Button>
			</div>
		</Card.Content>
	</Card.Root>

	<!-- Danger Zone -->
	<Card.Root class="border-destructive">
		<Card.Header>
			<Card.Title class="flex items-center gap-2 text-destructive">
				<Trash2 class="h-5 w-5" />
				위험 구역
			</Card.Title>
			<Card.Description>계정 삭제 등 되돌릴 수 없는 작업입니다</Card.Description>
		</Card.Header>
		<Card.Content>
			<Button variant="destructive" disabled>
				계정 삭제 (준비 중)
			</Button>
			<p class="mt-2 text-xs text-muted-foreground">
				계정을 삭제하면 모든 데이터가 영구적으로 삭제됩니다.
			</p>
		</Card.Content>
	</Card.Root>
</div>
