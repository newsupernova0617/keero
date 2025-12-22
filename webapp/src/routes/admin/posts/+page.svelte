<script lang="ts">
	import type { PageData } from './$types'
	import { enhance } from '$app/forms'

	let { data }: { data: PageData } = $props()
</script>

<svelte:head>
	<title>ê²Œì‹œê¸€ ê´€ë¦?/title>
</svelte:head>

<div class="space-y-6">
	<h2 class="text-2xl font-bold text-gray-900">ê²Œì‹œê¸€ ê´€ë¦?/h2>

	<div class="rounded-lg border border-gray-200 bg-white">
		<table class="w-full">
			<thead class="border-b border-gray-200 bg-gray-50">
				<tr>
					<th class="px-6 py-3 text-left text-xs font-medium uppercase text-gray-500">ID</th>
					<th class="px-6 py-3 text-left text-xs font-medium uppercase text-gray-500">?œëª©</th>
					<th class="px-6 py-3 text-left text-xs font-medium uppercase text-gray-500">ì¶œì²˜</th>
					<th class="px-6 py-3 text-left text-xs font-medium uppercase text-gray-500">? ì§œ</th>
					<th class="px-6 py-3 text-left text-xs font-medium uppercase text-gray-500">
						?‘ì—…
					</th>
				</tr>
			</thead>
			<tbody class="divide-y divide-gray-200">
				{#each data.posts as post}
					<tr>
						<td class="px-6 py-4 text-sm text-gray-900">{post.id}</td>
						<td class="px-6 py-4">
							<a href="/post/{post.id}" class="text-sm text-blue-600 hover:underline">
								{post.title}
							</a>
						</td>
						<td class="px-6 py-4 text-sm text-gray-600">{post.site_name}</td>
						<td class="px-6 py-4 text-sm text-gray-600">
							{new Date(post.crawled_at).toLocaleDateString('ko-KR')}
						</td>
						<td class="px-6 py-4">
							<form method="POST" action="?/delete" use:enhance>
								<input type="hidden" name="post_id" value={post.id} />
								<button
									type="submit"
									class="text-sm text-red-600 hover:underline"
									onclick="return confirm('?•ë§ ?? œ?˜ì‹œê² ìŠµ?ˆê¹Œ?')"
								>
									?? œ
								</button>
							</form>
						</td>
					</tr>
				{/each}
			</tbody>
		</table>
	</div>
</div>
