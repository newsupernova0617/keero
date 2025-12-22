<script lang="ts">
	import * as DropdownMenu from '$lib/components/ui/dropdown-menu'
	import { Button } from '$lib/components/ui/button'
	import * as Avatar from '$lib/components/ui/avatar'
	import { User, LogOut, Settings } from 'lucide-svelte'
	
	let { user }: { user: any } = $props()
	
	// 사용자 이름 첫 글자
	let initial = $derived(user?.email?.[0]?.toUpperCase() || 'U')
</script>

<DropdownMenu.Root>
	<DropdownMenu.Trigger asChild let:builder>
		<Button builders={[builder]} variant="ghost" class="relative h-10 w-10 rounded-full">
			<Avatar.Root class="h-10 w-10">
				<Avatar.Fallback class="bg-primary text-primary-foreground">
					{initial}
				</Avatar.Fallback>
			</Avatar.Root>
		</Button>
	</DropdownMenu.Trigger>
	<DropdownMenu.Content class="w-56" align="end">
		<DropdownMenu.Label>
			<div class="flex flex-col space-y-1">
				<p class="text-sm font-medium leading-none">내 계정</p>
				<p class="text-xs leading-none text-muted-foreground">
					{user?.email}
				</p>
			</div>
		</DropdownMenu.Label>
		<DropdownMenu.Separator />
		<DropdownMenu.Item href="/profile">
			<User class="mr-2 h-4 w-4" />
			<span>프로필</span>
		</DropdownMenu.Item>
		<DropdownMenu.Item href="/settings">
			<Settings class="mr-2 h-4 w-4" />
			<span>설정</span>
		</DropdownMenu.Item>
		<DropdownMenu.Separator />
		<DropdownMenu.Item asChild>
			<form method="POST" action="/auth/signout" class="w-full">
				<button type="submit" class="flex w-full items-center">
					<LogOut class="mr-2 h-4 w-4" />
					<span>로그아웃</span>
				</button>
			</form>
		</DropdownMenu.Item>
	</DropdownMenu.Content>
</DropdownMenu.Root>
