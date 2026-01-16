<script lang="ts">
	import type { PageData } from './$types'
	import * as Card from '$lib/components/ui/card'
	import { Button } from '$lib/components/ui/button'
	import { Badge } from '$lib/components/ui/badge'
	import {
		Database,
		FileText,
		Image,
		Users,
		MessageSquare,
		Heart,
		Bookmark,
		AlertTriangle,
		Star,
		FileSearch,
		Settings,
		ChevronRight
	} from '@lucide/svelte'

	let { data }: { data: PageData } = $props()

	const iconMap: Record<string, any> = {
		FileText,
		Image,
		Users,
		MessageSquare,
		Heart,
		Bookmark,
		AlertTriangle,
		Star,
		FileSearch,
		Settings
	}

	function getIcon(iconName: string) {
		return iconMap[iconName] || Database
	}
</script>

<svelte:head>
	<title>테이블 관리 - Admin</title>
</svelte:head>

<div class="space-y-6">
	<div>
		<h1 class="text-3xl font-bold tracking-tight flex items-center gap-2">
			<Database class="h-8 w-8" />
			테이블 관리
		</h1>
		<p class="text-muted-foreground">모든 데이터베이스 테이블 조회 및 관리</p>
	</div>

	<div class="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
		{#each data.tables as table}
			{@const Icon = getIcon(table.icon)}
			<Card.Root class="hover:shadow-lg transition-shadow">
				<Card.Header>
					<div class="flex items-start justify-between">
						<div class="flex items-center gap-3">
							<div class="p-2 rounded-lg bg-primary/10">
								<Icon class="h-6 w-6 text-primary" />
							</div>
							<div>
								<Card.Title class="text-lg">{table.displayName}</Card.Title>
								<p class="text-xs text-muted-foreground font-mono">{table.name}</p>
							</div>
						</div>
					</div>
				</Card.Header>
				<Card.Content>
					<p class="text-sm text-muted-foreground mb-4">{table.description}</p>
					
					<div class="flex items-center justify-between mb-4">
						<div class="text-2xl font-bold">{table.count.toLocaleString()}</div>
						<div class="text-sm text-muted-foreground">레코드</div>
					</div>

					<div class="flex flex-wrap gap-2 mb-4">
						{#if table.canCreate}
							<Badge variant="secondary" class="text-xs">생성 가능</Badge>
						{/if}
						{#if table.canEdit}
							<Badge variant="secondary" class="text-xs">수정 가능</Badge>
						{/if}
						{#if table.canDelete}
							<Badge variant="secondary" class="text-xs">삭제 가능</Badge>
						{/if}
					</div>

					<Button href="/admin/database/tables/{table.name}" class="w-full" variant="outline">
						관리하기
						<ChevronRight class="ml-2 h-4 w-4" />
					</Button>
				</Card.Content>
			</Card.Root>
		{/each}
	</div>
</div>
