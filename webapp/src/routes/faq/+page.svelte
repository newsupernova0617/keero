<script lang="ts">
	import { Separator } from '$lib/components/ui/separator'
	import { ChevronDown } from '@lucide/svelte'
	import { getBaseUrl, SITE_NAME } from '$lib/utils/seo'

	const baseUrl = getBaseUrl()

	// FAQ 데이터
	const faqs = [
		{
			category: '서비스 이용',
			items: [
				{
					question: 'KEERO는 어떤 서비스인가요?',
					answer: 'KEERO는 뽐뿌, FM코리아, 오늘의유머, 루리웹, 웃긴대학 등 여러 커뮤니티 사이트의 유머 게시글을 한곳에 모아 제공하는 서비스입니다. 각 사이트를 일일이 방문하지 않고도 재미있는 콘텐츠를 편리하게 즐길 수 있습니다.'
				},
				{
					question: '회원가입 없이도 이용할 수 있나요?',
					answer: '네, 게시글 열람과 검색은 회원가입 없이 가능합니다. 다만 댓글 작성, 좋아요, 북마크 기능은 로그인이 필요합니다.'
				},
				{
					question: '게시글은 얼마나 자주 업데이트되나요?',
					answer: '크롤러가 10분마다 자동으로 실행되어 최신 게시글을 수집합니다. 따라서 항상 최신 유머 콘텐츠를 확인하실 수 있습니다.'
				},
				{
					question: '모바일에서도 이용할 수 있나요?',
					answer: '네, KEERO는 반응형 디자인으로 제작되어 PC, 태블릿, 모바일 등 모든 기기에서 최적화된 화면으로 이용하실 수 있습니다.'
				}
			]
		},
		{
			category: '계정 및 기능',
			items: [
				{
					question: '회원가입은 어떻게 하나요?',
					answer: '우측 상단의 "로그인" 버튼을 클릭하면 Supabase 인증을 통해 간편하게 회원가입 및 로그인이 가능합니다. 이메일 주소만 있으면 가입할 수 있습니다.'
				},
				{
					question: '댓글을 수정하거나 삭제할 수 있나요?',
					answer: '네, 본인이 작성한 댓글은 언제든지 수정하거나 삭제할 수 있습니다. 댓글 우측의 메뉴 버튼을 클릭하면 수정/삭제 옵션이 표시됩니다.'
				},
				{
					question: '북마크한 게시글은 어디서 확인하나요?',
					answer: '로그인 후 우측 상단의 프로필 메뉴에서 "내 활동"을 클릭하면 북마크한 게시글 목록을 확인할 수 있습니다.'
				},
				{
					question: '다크 모드를 사용할 수 있나요?',
					answer: '네, 우측 상단의 달 아이콘을 클릭하면 다크 모드와 라이트 모드를 전환할 수 있습니다. 설정은 자동으로 저장됩니다.'
				}
			]
		},
		{
			category: '콘텐츠 및 저작권',
			items: [
				{
					question: '게시글의 저작권은 누구에게 있나요?',
					answer: '모든 게시글의 저작권은 원저작자에게 있습니다. KEERO는 공개된 게시글의 링크와 미리보기만 제공하며, 모든 게시글에는 원본 출처가 명확히 표시됩니다.'
				},
				{
					question: '제 게시글을 삭제해주실 수 있나요?',
					answer: '네, 저작권자의 요청이 있을 경우 즉시 해당 콘텐츠를 삭제합니다. 문의하기 페이지 또는 keero1356@gmail.com으로 게시글 URL과 함께 삭제 요청을 보내주세요.'
				},
				{
					question: '부적절한 게시글을 신고할 수 있나요?',
					answer: '네, 각 게시글 하단의 신고 버튼을 통해 부적절한 콘텐츠를 신고할 수 있습니다. 신고된 게시글은 관리자가 검토 후 조치합니다.'
				},
				{
					question: '원본 게시글로 이동하려면 어떻게 하나요?',
					answer: '각 게시글 상단에 표시된 출처 사이트 이름을 클릭하거나, 게시글 하단의 "원본 보기" 버튼을 클릭하면 원본 사이트로 이동합니다.'
				}
			]
		},
		{
			category: '기술 및 문제 해결',
			items: [
				{
					question: '이미지가 로딩되지 않아요.',
					answer: '이미지는 Cloudflare R2에 최적화되어 저장됩니다. 로딩이 느리거나 표시되지 않는 경우 페이지를 새로고침하거나 잠시 후 다시 시도해주세요. 문제가 지속되면 문의해주세요.'
				},
				{
					question: '검색이 작동하지 않아요.',
					answer: '검색 기능은 제목과 내용을 전체 검색(FTS)합니다. 검색어를 2자 이상 입력해주세요. 문제가 지속되면 브라우저 캐시를 삭제하거나 다른 브라우저를 사용해보세요.'
				},
				{
					question: '로그인이 되지 않아요.',
					answer: 'Supabase 인증 시스템을 사용합니다. 쿠키가 차단되어 있지 않은지 확인하고, 팝업 차단이 해제되어 있는지 확인해주세요. 문제가 지속되면 문의해주세요.'
				},
				{
					question: '페이지 로딩이 느려요.',
					answer: '서비스는 Railway에 배포되어 있으며, 이미지는 WebP 형식으로 최적화되어 있습니다. 네트워크 상태를 확인하시고, 문제가 지속되면 문의해주세요.'
				}
			]
		},
		{
			category: '기타',
			items: [
				{
					question: '서비스는 무료인가요?',
					answer: '네, KEERO는 완전 무료 서비스입니다. 광고를 통해 운영되며, 모든 기능을 무료로 이용하실 수 있습니다.'
				},
				{
					question: '새로운 기능을 제안하고 싶어요.',
					answer: '언제든지 환영합니다! 문의하기 페이지 또는 keero1356@gmail.com으로 의견을 보내주세요. 사용자 여러분의 피드백이 서비스 발전에 큰 도움이 됩니다.'
				},
				{
					question: '개인정보는 어떻게 관리되나요?',
					answer: '개인정보처리방침 페이지에서 자세한 내용을 확인하실 수 있습니다. 최소한의 정보(이메일)만 수집하며, 제3자에게 제공하지 않습니다.'
				},
				{
					question: '서비스 이용 중 문제가 발생했어요.',
					answer: '문의하기 페이지 또는 keero1356@gmail.com으로 문제 상황을 자세히 설명해주세요. 가능하면 스크린샷을 함께 보내주시면 더욱 빠르게 해결할 수 있습니다.'
				}
			]
		}
	]

	let openItems = $state<Set<string>>(new Set())

	function toggleItem(category: string, index: number) {
		const key = `${category}-${index}`
		if (openItems.has(key)) {
			openItems.delete(key)
		} else {
			openItems.add(key)
		}
		openItems = new Set(openItems)
	}

	function isOpen(category: string, index: number): boolean {
		return openItems.has(`${category}-${index}`)
	}
</script>

<svelte:head>
	<title>자주 묻는 질문 (FAQ) - {SITE_NAME}</title>
	<meta
		name="description"
		content="KEERO 서비스 이용 중 자주 묻는 질문과 답변을 확인하세요. 회원가입, 기능 사용법, 저작권, 문제 해결 등 다양한 정보를 제공합니다."
	/>

	<!-- Open Graph -->
	<meta property="og:title" content="자주 묻는 질문 (FAQ) - {SITE_NAME}" />
	<meta
		property="og:description"
		content="KEERO 서비스 이용 중 자주 묻는 질문과 답변을 확인하세요."
	/>
	<meta property="og:url" content="{baseUrl}/faq" />
	<meta property="og:type" content="website" />
	<meta property="og:image" content="{baseUrl}/og-default.png" />

	<!-- Canonical -->
	<link rel="canonical" href="{baseUrl}/faq" />
</svelte:head>

<div class="mx-auto max-w-4xl px-4 py-12">
	<h1 class="mb-4 text-4xl font-bold">자주 묻는 질문</h1>
	<p class="mb-12 text-lg text-muted-foreground">
		KEERO 서비스 이용 중 궁금한 점을 빠르게 해결하세요.
		찾으시는 답변이 없다면 <a href="/contact" class="text-primary hover:underline">문의하기</a>를
		이용해주세요.
	</p>

	<div class="space-y-12">
		{#each faqs as faqCategory}
			<section>
				<h2 class="mb-6 text-2xl font-semibold">{faqCategory.category}</h2>

				<div class="space-y-3">
					{#each faqCategory.items as item, index}
						<div class="rounded-lg border bg-card">
							<button
								class="flex w-full items-center justify-between p-4 text-left transition hover:bg-accent"
								onclick={() => toggleItem(faqCategory.category, index)}
								aria-expanded={isOpen(faqCategory.category, index)}
							>
								<span class="font-medium pr-4">{item.question}</span>
								<ChevronDown
									class="h-5 w-5 flex-shrink-0 text-muted-foreground transition-transform {isOpen(
										faqCategory.category,
										index
									)
										? 'rotate-180'
										: ''}"
								/>
							</button>

							{#if isOpen(faqCategory.category, index)}
								<div class="border-t px-4 pb-4 pt-3">
									<p class="text-sm leading-relaxed text-muted-foreground">
										{item.answer}
									</p>
								</div>
							{/if}
						</div>
					{/each}
				</div>
			</section>

			{#if faqCategory !== faqs[faqs.length - 1]}
				<Separator />
			{/if}
		{/each}
	</div>

	<!-- 추가 도움말 -->
	<div class="mt-12 rounded-lg border bg-muted/50 p-6 text-center">
		<h3 class="mb-2 text-lg font-semibold">찾으시는 답변이 없나요?</h3>
		<p class="mb-4 text-sm text-muted-foreground">
			추가 문의사항이 있으시면 언제든지 연락해주세요.
		</p>
		<div class="flex flex-col items-center justify-center gap-3 sm:flex-row">
			<a
				href="/contact"
				class="inline-flex items-center rounded-lg bg-primary px-4 py-2 text-sm font-medium text-primary-foreground transition hover:bg-primary/90"
			>
				문의하기
			</a>
			<a
				href="mailto:keero1356@gmail.com"
				class="inline-flex items-center rounded-lg border bg-background px-4 py-2 text-sm font-medium transition hover:bg-accent"
			>
				이메일 보내기
			</a>
		</div>
	</div>

	<!-- 마지막 업데이트 -->
	<div class="mt-8 text-center text-sm text-muted-foreground">
		마지막 업데이트: 2026년 1월 12일
	</div>
</div>
