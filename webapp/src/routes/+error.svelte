<script lang="ts">
	import { page } from '$app/stores'
	import { Button } from '$lib/components/ui/button'
	import { Home, ArrowLeft, Search, AlertCircle } from '@lucide/svelte'
</script>

<svelte:head>
	<title>페이지를 찾을 수 없습니다 - KEERO</title>
	<meta name="robots" content="noindex" />
</svelte:head>

<div class="flex min-h-[70vh] flex-col items-center justify-center px-4 text-center">
	<!-- 에러 아이콘 -->
	<div class="mb-6 rounded-full bg-muted p-6">
		<AlertCircle class="h-16 w-16 text-muted-foreground" />
	</div>

	<!-- 에러 코드 -->
	<h1 class="mb-2 text-7xl font-bold text-primary">
		{$page.status}
	</h1>

	<!-- 에러 메시지 -->
	<h2 class="mb-4 text-2xl font-semibold">
		{#if $page.status === 404}
			페이지를 찾을 수 없습니다
		{:else if $page.status === 500}
			서버 오류가 발생했습니다
		{:else}
			오류가 발생했습니다
		{/if}
	</h2>

	<!-- 설명 -->
	<p class="mb-8 max-w-md text-muted-foreground">
		{#if $page.status === 404}
			요청하신 페이지가 존재하지 않거나 이동되었을 수 있습니다.
			URL을 다시 확인해주세요.
		{:else if $page.status === 500}
			일시적인 서버 문제가 발생했습니다.
			잠시 후 다시 시도해주세요.
		{:else}
			{$page.error?.message || '알 수 없는 오류가 발생했습니다.'}
		{/if}
	</p>

	<!-- 액션 버튼들 -->
	<div class="flex flex-col gap-3 sm:flex-row">
		<Button href="/" class="gap-2">
			<Home class="h-4 w-4" />
			홈으로 가기
		</Button>
		<Button variant="outline" onclick={() => history.back()} class="gap-2">
			<ArrowLeft class="h-4 w-4" />
			이전 페이지
		</Button>
		<Button variant="outline" href="/search" class="gap-2">
			<Search class="h-4 w-4" />
			검색하기
		</Button>
	</div>

	<!-- 추가 링크 -->
	<div class="mt-12 text-sm text-muted-foreground">
		<p>문제가 계속되면 <a href="/contact" class="text-primary hover:underline">문의하기</a>를 이용해주세요.</p>
	</div>
</div>
