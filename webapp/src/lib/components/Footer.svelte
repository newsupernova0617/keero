<script lang="ts">
	import { Separator } from '$lib/components/ui/separator'
	import { Github, Mail, Heart } from '@lucide/svelte'
</script>

<footer class="border-t bg-card">
	<div class="mx-auto max-w-7xl px-4 py-8">
		<div class="grid gap-8 md:grid-cols-3">
			<!-- About -->
			<div>
				<h3 class="mb-3 text-lg font-semibold">? ë¨¸ ê²Œì‹œ??/h3>
				<p class="text-sm text-muted-foreground">
					?¬ëŸ¬ ì»¤ë??ˆí‹°???¬ë??ˆëŠ” ? ë¨¸ë¥??œê³³?ì„œ ë§Œë‚˜ë³´ì„¸??
				</p>
			</div>

			<!-- Links -->
			<div>
				<h3 class="mb-3 text-lg font-semibold">ë§í¬</h3>
				<ul class="space-y-2 text-sm">
					<li>
						<a href="/about" class="text-muted-foreground transition hover:text-foreground">
							?Œê°œ
						</a>
					</li>
					<li>
						<a href="/privacy" class="text-muted-foreground transition hover:text-foreground">
							ê°œì¸?•ë³´ì²˜ë¦¬ë°©ì¹¨
						</a>
					</li>
					<li>
						<a href="/terms" class="text-muted-foreground transition hover:text-foreground">
							?´ìš©?½ê?
						</a>
					</li>
				</ul>
			</div>

			<!-- Social -->
			<div>
				<h3 class="mb-3 text-lg font-semibold">?Œì…œ</h3>
				<div class="flex gap-4">
					<a
						href="https://github.com"
						target="_blank"
						rel="noopener noreferrer"
						class="text-muted-foreground transition hover:text-foreground"
						aria-label="GitHub"
					>
						<Github class="h-5 w-5" />
					</a>
					<a
						href="mailto:contact@example.com"
						class="text-muted-foreground transition hover:text-foreground"
						aria-label="Email"
					>
						<Mail class="h-5 w-5" />
					</a>
				</div>
			</div>
		</div>

		<Separator class="my-6" />

		<div class="flex flex-col items-center justify-between gap-4 text-sm text-muted-foreground sm:flex-row">
			<p>Â© 2024 ? ë¨¸ ê²Œì‹œ?? All rights reserved.</p>
			<p class="flex items-center gap-1">
				Made with <Heart class="h-4 w-4 fill-red-500 text-red-500" /> by Your Team
			</p>
		</div>
	</div>
</footer>
