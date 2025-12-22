<script lang="ts">
	import { Button } from '$lib/components/ui/button'
	import { ChevronLeft, ChevronRight } from '@lucide/svelte'

	let {
		page,
		totalPages,
		totalCount
	}: {
		page: number
		totalPages: number
		totalCount: number
	} = $props()

	// 페이지 번호 배열 생성 (최대 7개 표시)
	let pageNumbers = $derived(() => {
		const pages: number[] = []
		const maxVisible = 7
		
		if (totalPages <= maxVisible) {
			// 전체 페이지가 7개 이하면 모두 표시
			for (let i = 1; i <= totalPages; i++) {
				pages.push(i)
			}
		} else {
			// 현재 페이지 기준으로 앞뒤 3개씩 표시
			let start = Math.max(1, page - 3)
			let end = Math.min(totalPages, page + 3)
			
			// 시작이 1이면 끝을 늘림
			if (start === 1) {
				end = Math.min(totalPages, maxVisible)
			}
			// 끝이 마지막이면 시작을 줄임
			if (end === totalPages) {
				start = Math.max(1, totalPages - maxVisible + 1)
			}
			
			for (let i = start; i <= end; i++) {
				pages.push(i)
			}
		}
		
		return pages
	})
</script>

{#if totalPages > 1}
	<div class="flex items-center justify-center gap-2">
		<!-- 이전 페이지 -->
		<Button
			href="?page={page - 1}"
			variant="outline"
			size="sm"
			disabled={page <= 1}
			class="gap-1"
		>
			<ChevronLeft class="h-4 w-4" />
			이전
		</Button>

		<!-- 페이지 번호 -->
		<div class="flex gap-1">
			{#if pageNumbers()[0] > 1}
				<Button href="?page=1" variant="outline" size="sm">1</Button>
				{#if pageNumbers()[0] > 2}
					<span class="flex items-center px-2">...</span>
				{/if}
			{/if}

			{#each pageNumbers() as pageNum}
				<Button
					href="?page={pageNum}"
					variant={pageNum === page ? 'default' : 'outline'}
					size="sm"
				>
					{pageNum}
				</Button>
			{/each}

			{#if pageNumbers()[pageNumbers().length - 1] < totalPages}
				{#if pageNumbers()[pageNumbers().length - 1] < totalPages - 1}
					<span class="flex items-center px-2">...</span>
				{/if}
				<Button href="?page={totalPages}" variant="outline" size="sm">{totalPages}</Button>
			{/if}
		</div>

		<!-- 다음 페이지 -->
		<Button
			href="?page={page + 1}"
			variant="outline"
			size="sm"
			disabled={page >= totalPages}
			class="gap-1"
		>
			다음
			<ChevronRight class="h-4 w-4" />
		</Button>
	</div>

	<!-- 페이지 정보 -->
	<p class="text-center text-sm text-muted-foreground">
		전체 {totalCount}개 게시글 중 {page} / {totalPages} 페이지
	</p>
{/if}
