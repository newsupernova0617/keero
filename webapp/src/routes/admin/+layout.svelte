<script lang="ts">
	import type { LayoutData } from './$types'

	let { children, data }: { children: any; data: LayoutData } = $props()
</script>

<div class="min-h-screen bg-gray-100">
	<!-- Admin Header -->
	<header class="border-b bg-white shadow-sm">
		<div class="mx-auto max-w-7xl px-4 py-4">
			<div class="flex items-center justify-between">
				<h1 class="text-2xl font-bold text-gray-900">ê´€ë¦¬ì ?˜ì´ì§€</h1>
				<a href="/" class="text-blue-600 hover:underline">???¬ì´?¸ë¡œ ?Œì•„ê°€ê¸?/a>
			</div>
		</div>
	</header>

	<div class="mx-auto max-w-7xl px-4 py-8">
		<div class="flex gap-6">
			<!-- Sidebar -->
			<aside class="w-64 flex-shrink-0">
				<nav class="space-y-2">
					<a
						href="/admin"
						class="block rounded-lg px-4 py-2 text-gray-700 transition hover:bg-gray-200"
					>
						?“Š ?€?œë³´??
					</a>
					<a
						href="/admin/posts"
						class="block rounded-lg px-4 py-2 text-gray-700 transition hover:bg-gray-200"
					>
						?“ ê²Œì‹œê¸€ ê´€ë¦?
					</a>
					<a
						href="/admin/users"
						class="block rounded-lg px-4 py-2 text-gray-700 transition hover:bg-gray-200"
					>
						?‘¥ ?¬ìš©??ê´€ë¦?
					</a>
					<a
						href="/admin/comments"
						class="block rounded-lg px-4 py-2 text-gray-700 transition hover:bg-gray-200"
					>
						?’¬ ?“ê? ê´€ë¦?
					</a>
				</nav>
			</aside>

			<!-- Main Content -->
			<main class="flex-1">
				{@render children()}
			</main>
		</div>
	</div>
</div>
