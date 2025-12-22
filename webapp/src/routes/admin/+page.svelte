<script lang="ts">
	import type { PageData } from './$types'

	let { data }: { data: PageData } = $props()
</script>

<svelte:head>
	<title>ê´€ë¦¬ìž ?€?œë³´??/title>
</svelte:head>

<div class="space-y-6">
	<h2 class="text-2xl font-bold text-gray-900">?€?œë³´??/h2>

	<!-- ?µê³„ ì¹´ë“œ -->
	<div class="grid gap-6 md:grid-cols-3">
		<div class="rounded-lg border border-gray-200 bg-white p-6">
			<div class="text-sm font-medium text-gray-600">ì´?ê²Œì‹œê¸€</div>
			<div class="mt-2 text-3xl font-bold text-gray-900">{data.totalPosts}</div>
		</div>

		<div class="rounded-lg border border-gray-200 bg-white p-6">
			<div class="text-sm font-medium text-gray-600">ì´??¬ìš©??/div>
			<div class="mt-2 text-3xl font-bold text-gray-900">{data.totalUsers}</div>
		</div>

		<div class="rounded-lg border border-gray-200 bg-white p-6">
			<div class="text-sm font-medium text-gray-600">ì´??“ê?</div>
			<div class="mt-2 text-3xl font-bold text-gray-900">{data.totalComments}</div>
		</div>
	</div>

	<!-- ìµœê·¼ ê²Œì‹œê¸€ -->
	<div class="rounded-lg border border-gray-200 bg-white">
		<div class="border-b border-gray-200 px-6 py-4">
			<h3 class="text-lg font-semibold text-gray-900">ìµœê·¼ ê²Œì‹œê¸€</h3>
		</div>
		<div class="divide-y divide-gray-200">
			{#each data.recentPosts as post}
				<div class="px-6 py-4">
					<div class="flex items-center justify-between">
						<div class="flex-1">
							<a href="/post/{post.id}" class="font-medium text-gray-900 hover:text-blue-600">
								{post.title}
							</a>
							<div class="mt-1 flex items-center gap-2 text-sm text-gray-500">
								<span class="rounded bg-gray-100 px-2 py-1 text-xs">{post.site_name}</span>
								<span>{new Date(post.crawled_at).toLocaleString('ko-KR')}</span>
							</div>
						</div>
						<a
							href="/admin/posts?id={post.id}"
							class="text-sm text-blue-600 hover:underline"
						>
							ê´€ë¦?
						</a>
					</div>
				</div>
			{/each}
		</div>
	</div>
</div>
