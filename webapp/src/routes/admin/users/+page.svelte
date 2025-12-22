<script lang="ts">
	import type { PageData } from './$types'

	let { data }: { data: PageData } = $props()
</script>

<svelte:head>
	<title>?¬ìš©??ê´€ë¦?/title>
</svelte:head>

<div class="space-y-6">
	<h2 class="text-2xl font-bold text-gray-900">?¬ìš©??ê´€ë¦?/h2>

	<div class="rounded-lg border border-gray-200 bg-white">
		<table class="w-full">
			<thead class="border-b border-gray-200 bg-gray-50">
				<tr>
					<th class="px-6 py-3 text-left text-xs font-medium uppercase text-gray-500">ID</th>
					<th class="px-6 py-3 text-left text-xs font-medium uppercase text-gray-500">
						?´ë©”??
					</th>
					<th class="px-6 py-3 text-left text-xs font-medium uppercase text-gray-500">
						?´ë¦„
					</th>
					<th class="px-6 py-3 text-left text-xs font-medium uppercase text-gray-500">
						ê¶Œí•œ
					</th>
					<th class="px-6 py-3 text-left text-xs font-medium uppercase text-gray-500">
						ê°€?…ì¼
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
								{user.role === 99 ? 'ê´€ë¦¬ì' : '?¬ìš©??}
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
