<script lang="ts">
	import type { PageData } from './$types'

	let { data }: { data: PageData } = $props()
	let searchQuery = $derived(data.query || '')
</script>

<svelte:head>
	<title>
		{data.query ? `"${data.query}" 검색 결과` : '검색'} - 유머 게시판
	</title>
	<meta
		name="description"
		content={data.query
			? `"${data.query}" 검색 결과 ${data.results.length}개. 재미있는 유머와 웃긴 글을 찾아보세요.`
			: '유머 게시판에서 재미있는 글을 검색해보세요.'}
	/>
	<meta name="robots" content="noindex, follow" />
</svelte:head>

<div class="space-y-6">
	<!-- 검색 폼 -->
	<div class="rounded-lg border border-gray-200 bg-white p-6">
		<form method="GET" class="flex gap-2">
			<input
				type="text"
				name="q"
				bind:value={searchQuery}
				placeholder="검색어를 입력하세요..."
				class="flex-1 rounded-lg border border-gray-300 px-4 py-2 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
			/>
			<button
				type="submit"
				class="rounded-lg bg-blue-600 px-6 py-2 font-medium text-white transition hover:bg-blue-700"
			>
				검색
			</button>
		</form>
	</div>

	<!-- 검색 결과 -->
	{#if data.query}
		<div>
			<h1 class="mb-4 text-2xl font-bold text-gray-900">
				"{data.query}" 검색 결과 ({data.results.length}개)
			</h1>

			{#if data.results.length === 0}
				<div class="rounded-lg border border-gray-200 bg-white p-8 text-center">
					<p class="text-gray-500">검색 결과가 없습니다.</p>
				</div>
			{:else}
				<div class="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
					{#each data.results as post}
						<a
							href="/post/{post.id}"
							class="group overflow-hidden rounded-lg border border-gray-200 bg-white shadow-sm transition hover:shadow-md"
						>
							{#if post.thumbnail}
								<div class="aspect-video overflow-hidden bg-gray-100">
									<img
										src={post.thumbnail}
										alt={post.title}
										class="h-full w-full object-cover transition group-hover:scale-105"
									/>
								</div>
							{/if}

							<div class="p-4">
								<h2
									class="mb-2 line-clamp-2 text-lg font-semibold text-gray-900 group-hover:text-blue-600"
								>
									{post.title}
								</h2>

								<div class="flex items-center gap-2 text-sm text-gray-500">
									<span class="rounded bg-gray-100 px-2 py-1 text-xs font-medium">
										{post.site_name}
									</span>
									{#if post.created_at}
										<span>{new Date(post.created_at).toLocaleDateString('ko-KR')}</span>
									{/if}
									{#if post.image_count > 0}
										<span>🖼️ {post.image_count}</span>
									{/if}
								</div>
							</div>
						</a>
					{/each}
				</div>
			{/if}
		</div>
	{:else}
		<div class="rounded-lg border border-gray-200 bg-white p-8 text-center">
			<p class="text-gray-500">검색어를 입력해주세요.</p>
		</div>
	{/if}
</div>
