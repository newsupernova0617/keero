<script lang="ts">
	import type { PageData } from './$types'
	import { enhance } from '$app/forms'
	import * as Card from '$lib/components/ui/card'
	import { Button } from '$lib/components/ui/button'
	import { Badge } from '$lib/components/ui/badge'

	let { data }: { data: PageData } = $props()
</script>

<svelte:head>
	<title>댓글 관리 - 관리자</title>
</svelte:head>

<div class="space-y-6">
	<div>
		<h1 class="text-3xl font-bold tracking-tight">댓글 관리</h1>
		<p class="text-muted-foreground">최근 댓글 100개를 관리합니다</p>
	</div>

	<Card.Root>
		<Card.Content class="p-0">
			<div class="overflow-x-auto">
				<table class="w-full">
					<thead class="border-b bg-muted/50">
						<tr>
							<th class="px-6 py-3 text-left text-xs font-medium uppercase text-muted-foreground">ID</th>
							<th class="px-6 py-3 text-left text-xs font-medium uppercase text-muted-foreground">사용자</th>
							<th class="px-6 py-3 text-left text-xs font-medium uppercase text-muted-foreground">게시글</th>
							<th class="px-6 py-3 text-left text-xs font-medium uppercase text-muted-foreground">내용</th>
							<th class="px-6 py-3 text-left text-xs font-medium uppercase text-muted-foreground">날짜</th>
							<th class="px-6 py-3 text-left text-xs font-medium uppercase text-muted-foreground">상태</th>
							<th class="px-6 py-3 text-left text-xs font-medium uppercase text-muted-foreground">작업</th>
						</tr>
					</thead>
					<tbody class="divide-y">
						{#each data.comments as comment}
							<tr class="hover:bg-muted/50">
								<td class="px-6 py-4 text-sm">{comment.id}</td>
								<td class="px-6 py-4 text-sm">
									<div class="flex flex-col">
										<span class="font-medium">{comment.user_display_name || comment.user_email || 'Unknown'}</span>
										<span class="text-xs text-muted-foreground">{comment.user_email}</span>
									</div>
								</td>
								<td class="px-6 py-4 max-w-xs">
									<a href="/post/{comment.post_id}" class="text-sm text-primary hover:underline line-clamp-2">
										{comment.post_title}
									</a>
								</td>
								<td class="px-6 py-4 max-w-md">
									<p class="text-sm line-clamp-3">{comment.content}</p>
								</td>
								<td class="px-6 py-4 text-sm text-muted-foreground whitespace-nowrap">
									{comment.created_at ? new Date(comment.created_at).toLocaleDateString('ko-KR') : 'N/A'}
								</td>
								<td class="px-6 py-4">
									{#if comment.is_deleted}
										<Badge variant="destructive">삭제됨</Badge>
									{:else}
										<Badge variant="secondary">활성</Badge>
									{/if}
								</td>
								<td class="px-6 py-4">
									{#if !comment.is_deleted}
										<form method="POST" action="?/delete" use:enhance>
											<input type="hidden" name="comment_id" value={comment.id} />
											<Button
												type="submit"
												variant="ghost"
												size="sm"
												class="text-destructive hover:text-destructive"
												onclick={(e) => { if (!confirm('정말 삭제하시겠습니까?')) { e.preventDefault(); } }}
											>
												삭제
											</Button>
										</form>
									{/if}
								</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>
		</Card.Content>
	</Card.Root>
</div>
