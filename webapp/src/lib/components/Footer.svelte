<script lang="ts">
	import { Separator } from '$lib/components/ui/separator'
	import { Mail } from '@lucide/svelte'
</script>

<footer class="border-t bg-card">
	<div class="mx-auto max-w-7xl px-4 py-8">
		<div class="grid gap-8 md:grid-cols-3">
			<!-- About -->
			<div>
				<h3 class="mb-3 text-lg font-semibold">KEERO</h3>
				<p class="text-sm text-muted-foreground">
					여러 커뮤니티의 재미있는 유머를 한곳에서 만나보세요.
				</p>
				<p class="mt-2 text-xs text-muted-foreground">
					뽐뿌, FM코리아, 오늘의유머, 루리웹, 웃긴대학의 유머 게시글을 실시간으로 제공합니다.
				</p>
			</div>

			<!-- Links -->
			<div>
				<h3 class="mb-3 text-lg font-semibold">정보</h3>
				<ul class="space-y-2 text-sm">
					<li>
						<a href="/about" class="text-muted-foreground transition hover:text-foreground">
							서비스 소개
						</a>
					</li>
					<li>
						<a href="/stats" class="text-muted-foreground transition hover:text-foreground">
							통계
						</a>
					</li>
					<li>
						<a href="/highlights/weekly" class="text-muted-foreground transition hover:text-foreground">
							주간 하이라이트
						</a>
					</li>
					<li>
						<a href="/best-comments" class="text-muted-foreground transition hover:text-foreground">
							베스트 댓글
						</a>
					</li>
					<li>
						<a href="/faq" class="text-muted-foreground transition hover:text-foreground">
							자주 묻는 질문
						</a>
					</li>
					<li>
						<a href="/privacy" class="text-muted-foreground transition hover:text-foreground">
							개인정보처리방침
						</a>
					</li>
					<li>
						<a href="/terms" class="text-muted-foreground transition hover:text-foreground">
							이용약관
						</a>
					</li>
					<li>
						<a href="/dmca" class="text-muted-foreground transition hover:text-foreground">
							저작권 정책 (DMCA)
						</a>
					</li>
					<li>
						<a href="/contact" class="text-muted-foreground transition hover:text-foreground">
							문의하기
						</a>
					</li>
				</ul>
			</div>

			<!-- Contact -->
			<div>
				<h3 class="mb-3 text-lg font-semibold">문의</h3>
				<div class="space-y-3">
					<a
						href="mailto:keero1356@gmail.com"
						class="flex items-center gap-2 text-sm text-muted-foreground transition hover:text-foreground"
						aria-label="Email"
					>
						<Mail class="h-4 w-4" />
						<span>keero1356@gmail.com</span>
					</a>
				</div>
			</div>
		</div>

		<Separator class="my-6" />

		<div class="flex flex-col items-center justify-between gap-4 text-sm text-muted-foreground sm:flex-row">
			<p>© 2026 KEERO. All rights reserved.</p>
			<p class="text-xs">
				본 서비스는 공개된 게시글을 수집하여 제공하며, 모든 저작권은 원저작자에게 있습니다.
			</p>
		</div>
	</div>
</footer>
