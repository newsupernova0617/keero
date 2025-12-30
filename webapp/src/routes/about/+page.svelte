<script lang="ts">
	import { Separator } from '$lib/components/ui/separator'
	import { ExternalLink } from '@lucide/svelte'
</script>

<svelte:head>
	<title>서비스 소개 - KEERO</title>
	<meta name="description" content="여러 커뮤니티의 재미있는 유머를 한곳에서 만나보세요." />
</svelte:head>

<div class="mx-auto max-w-4xl px-4 py-12">
	<h1 class="mb-8 text-4xl font-bold">서비스 소개</h1>

	<div class="prose prose-neutral dark:prose-invert max-w-none">
		<!-- 서비스 개요 -->
		<section class="mb-12">
			<h2 class="mb-4 text-2xl font-semibold">우리는 누구인가요?</h2>
			<p class="text-muted-foreground leading-relaxed">
				KEERO는 국내 주요 커뮤니티 사이트의 유머 게시글을 한곳에 모아 제공하는 서비스입니다.
				여러 사이트를 일일이 방문하지 않고도 재미있는 콘텐츠를 편리하게 즐길 수 있습니다.
			</p>
		</section>

		<Separator class="my-8" />

		<!-- 주요 기능 -->
		<section class="mb-12">
			<h2 class="mb-4 text-2xl font-semibold">주요 기능</h2>
			<ul class="space-y-3 text-muted-foreground">
				<li class="flex items-start gap-2">
					<span class="mt-1.5 h-1.5 w-1.5 flex-shrink-0 rounded-full bg-primary"></span>
					<span><strong>통합 게시판</strong>: 여러 커뮤니티의 유머 게시글을 한눈에 확인</span>
				</li>
				<li class="flex items-start gap-2">
					<span class="mt-1.5 h-1.5 w-1.5 flex-shrink-0 rounded-full bg-primary"></span>
					<span><strong>실시간 업데이트</strong>: 5분마다 최신 게시글 자동 수집</span>
				</li>
				<li class="flex items-start gap-2">
					<span class="mt-1.5 h-1.5 w-1.5 flex-shrink-0 rounded-full bg-primary"></span>
					<span><strong>댓글 및 좋아요</strong>: 재미있는 게시글에 반응하고 의견 공유</span>
				</li>
				<li class="flex items-start gap-2">
					<span class="mt-1.5 h-1.5 w-1.5 flex-shrink-0 rounded-full bg-primary"></span>
					<span><strong>북마크</strong>: 나중에 다시 보고 싶은 게시글 저장</span>
				</li>
				<li class="flex items-start gap-2">
					<span class="mt-1.5 h-1.5 w-1.5 flex-shrink-0 rounded-full bg-primary"></span>
					<span><strong>검색 기능</strong>: 원하는 콘텐츠를 빠르게 찾기</span>
				</li>
			</ul>
		</section>

		<Separator class="my-8" />

		<!-- 수집 사이트 -->
		<section class="mb-12">
			<h2 class="mb-4 text-2xl font-semibold">콘텐츠 출처</h2>
			<p class="mb-4 text-muted-foreground">
				다음 커뮤니티 사이트의 유머 게시판에서 콘텐츠를 수집합니다:
			</p>
			<div class="grid gap-3 sm:grid-cols-2">
				<a
					href="https://www.ppomppu.co.kr/zboard/zboard.php?id=humor"
					target="_blank"
					rel="noopener noreferrer"
					class="flex items-center gap-2 rounded-lg border p-4 transition hover:bg-accent"
				>
					<span class="font-medium">뽐뿌 유머게시판</span>
					<ExternalLink class="h-4 w-4 text-muted-foreground" />
				</a>
				<a
					href="https://www.fmkorea.com/index.php?mid=best&listStyle=list"
					target="_blank"
					rel="noopener noreferrer"
					class="flex items-center gap-2 rounded-lg border p-4 transition hover:bg-accent"
				>
					<span class="font-medium">FM코리아 베스트</span>
					<ExternalLink class="h-4 w-4 text-muted-foreground" />
				</a>
				<a
					href="https://www.todayhumor.co.kr/board/list.php?table=bestofbest"
					target="_blank"
					rel="noopener noreferrer"
					class="flex items-center gap-2 rounded-lg border p-4 transition hover:bg-accent"
				>
					<span class="font-medium">오늘의유머 베오베</span>
					<ExternalLink class="h-4 w-4 text-muted-foreground" />
				</a>
				<a
					href="https://bbs.ruliweb.com/community/board/300143"
					target="_blank"
					rel="noopener noreferrer"
					class="flex items-center gap-2 rounded-lg border p-4 transition hover:bg-accent"
				>
					<span class="font-medium">루리웹 유머게시판</span>
					<ExternalLink class="h-4 w-4 text-muted-foreground" />
				</a>
				<a
					href="https://www.humoruniv.com/board/humor/list.html"
					target="_blank"
					rel="noopener noreferrer"
					class="flex items-center gap-2 rounded-lg border p-4 transition hover:bg-accent"
				>
					<span class="font-medium">웃긴대학</span>
					<ExternalLink class="h-4 w-4 text-muted-foreground" />
				</a>
			</div>
		</section>

		<Separator class="my-8" />

		<!-- 저작권 고지 -->
		<section class="mb-12">
			<h2 class="mb-4 text-2xl font-semibold">저작권 및 출처 표시</h2>
			<div class="rounded-lg border border-amber-500/50 bg-amber-500/10 p-4">
				<p class="text-sm leading-relaxed text-muted-foreground">
					본 서비스는 공개된 커뮤니티 게시글을 수집하여 제공합니다. 모든 게시글은 원본 출처가 명확히
					표시되며, 원본 사이트로 이동할 수 있는 링크를 제공합니다. 저작권은 원저작자에게 있으며,
					저작권자의 요청이 있을 경우 즉시 해당 콘텐츠를 삭제합니다.
				</p>
			</div>
		</section>

		<Separator class="my-8" />

		<!-- 문의 -->
		<section class="mb-12">
			<h2 class="mb-4 text-2xl font-semibold">문의하기</h2>
			<p class="mb-4 text-muted-foreground">
				서비스 이용 중 문의사항이나 개선 제안이 있으시면 언제든지 연락해주세요.
			</p>
			<div class="rounded-lg border bg-card p-6">
				<div class="space-y-2">
					<p class="text-sm text-muted-foreground">
						<strong class="text-foreground">이메일:</strong>
						<a href="mailto:keero1356@gmail.com" class="ml-2 text-primary hover:underline">
							keero1356@gmail.com
						</a>
					</p>
				</div>
			</div>
		</section>

		<!-- 마지막 업데이트 -->
		<div class="mt-12 text-center text-sm text-muted-foreground">
			마지막 업데이트: 2025년 12월 30일
		</div>
	</div>
</div>

<style>
	.prose {
		max-width: none;
	}
</style>
