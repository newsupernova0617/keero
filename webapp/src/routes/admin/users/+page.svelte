<script lang="ts">
	import type { PageData } from './$types'

	let { data }: { data: PageData } = $props()
</script>

<svelte:head>
	<title>사용자 관리</title>
</svelte:head>

<div class="space-y-6">
	<h2 class="text-2xl font-bold text-gray-900">사용자 관리</h2>

	<div class="rounded-lg border border-gray-200 bg-white">
		<table class="w-full">
			<thead class="border-b border-gray-200 bg-gray-50">
				<tr>
					<th class="px-6 py-3 text-left text-xs font-medium uppercase text-gray-500">ID</th>
					<th class="px-6 py-3 text-left text-xs font-medium uppercase text-gray-500">
						이메일
					</th>
					<th class="px-6 py-3 text-left text-xs font-medium uppercase text-gray-500">
						이름
					</th>
					<th class="px-6 py-3 text-left text-xs font-medium uppercase text-gray-500">
						권한
					</th>
					<th class="px-6 py-3 text-left text-xs font-medium uppercase text-gray-500">
						가입일
					</th>
				</tr>
			</thead>
			<tbody class="divide-y divide-gray-200">
				{#each data.users as user}
					<tr>
						<td class="px-6 py-4 text-sm text-gray-900">{user.id}</td>
						<td class="px-6 py-4 text-sm text-gray-900">{user.email}</td>
						<td class="px-6 py-4 text-sm text-gray-600">{user.display_name || '-'}</td>
						<td class="px-6 py-4">
							<span
								class="rounded px-2 py-1 text-xs font-medium"
								class:bg-red-100={user.role === 99}
								class:text-red-800={user.role === 99}
								class:bg-gray-100={user.role !== 99}
								class:text-gray-800={user.role !== 99}
							>
								{user.role === 99 ? '관리자' : '사용자'}
							</span>
						</td>
						<td class="px-6 py-4 text-sm text-gray-600">
							{new Date(user.created_at).toLocaleDateString('ko-KR')}
						</td>
					</tr>
				{/each}
			</tbody>
		</table>
	</div>
</div>
