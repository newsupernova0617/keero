<script lang="ts">
	import { Separator } from '$lib/components/ui/separator'
	import { Mail, MessageSquare, AlertCircle } from '@lucide/svelte'
	import { getBaseUrl, SITE_NAME } from '$lib/utils/seo'

	const baseUrl = getBaseUrl()
</script>

<svelte:head>
	<title>문의하기 - {SITE_NAME}</title>
	<meta name="description" content="KEERO 서비스 이용 중 궁금한 점이나 문의사항이 있으시면 언제든지 연락해주세요." />
	
	<!-- Open Graph -->
	<meta property="og:title" content="문의하기 - {SITE_NAME}" />
	<meta property="og:description" content="KEERO 서비스 이용 중 궁금한 점이나 문의사항이 있으시면 언제든지 연락해주세요." />
	<meta property="og:url" content="{baseUrl}/contact" />
	<meta property="og:type" content="website" />
	<meta property="og:image" content="{baseUrl}/og-default.png" />
	
	<!-- Canonical -->
	<link rel="canonical" href="{baseUrl}/contact" />
</svelte:head>

<div class="mx-auto max-w-4xl px-4 py-12">
	<h1 class="mb-8 text-4xl font-bold">문의하기</h1>

	<div class="prose prose-neutral dark:prose-invert max-w-none">
		<!-- 소개 -->
		<section class="mb-12">
			<p class="text-lg text-muted-foreground leading-relaxed">
				KEERO 서비스 이용 중 궁금한 점이나 개선 제안, 버그 리포트, 저작권 관련 문의 등이 있으시면
				아래 연락처로 언제든지 문의해주세요. 빠른 시일 내에 답변드리겠습니다.
			</p>
		</section>

		<Separator class="my-8" />

		<!-- 연락처 정보 -->
		<section class="mb-12">
			<h2 class="mb-6 text-2xl font-semibold">연락처</h2>
			
			<div class="grid gap-6 md:grid-cols-2">
				<!-- 이메일 -->
				<div class="rounded-lg border bg-card p-6">
					<div class="mb-4 flex items-center gap-3">
						<div class="rounded-full bg-primary/10 p-3">
							<Mail class="h-6 w-6 text-primary" />
						</div>
						<h3 class="text-lg font-semibold">이메일</h3>
					</div>
					<p class="mb-3 text-sm text-muted-foreground">
						가장 빠른 답변을 받으실 수 있습니다.
					</p>
					<a 
						href="mailto:keero1356@gmail.com" 
						class="inline-flex items-center gap-2 text-primary hover:underline"
					>
						<span class="font-medium">keero1356@gmail.com</span>
					</a>
				</div>

				<!-- 응답 시간 -->
				<div class="rounded-lg border bg-card p-6">
					<div class="mb-4 flex items-center gap-3">
						<div class="rounded-full bg-primary/10 p-3">
							<MessageSquare class="h-6 w-6 text-primary" />
						</div>
						<h3 class="text-lg font-semibold">응답 시간</h3>
					</div>
					<p class="text-sm text-muted-foreground">
						평일: 24시간 이내<br />
						주말/공휴일: 48시간 이내
					</p>
					<p class="mt-3 text-xs text-muted-foreground">
						* 긴급한 문의는 이메일 제목에 [긴급]을 표시해주세요.
					</p>
				</div>
			</div>
		</section>

		<Separator class="my-8" />

		<!-- 문의 유형 -->
		<section class="mb-12">
			<h2 class="mb-6 text-2xl font-semibold">문의 유형</h2>
			
			<div class="space-y-4">
				<div class="rounded-lg border p-4">
					<h3 class="mb-2 font-semibold">🐛 버그 리포트</h3>
					<p class="text-sm text-muted-foreground">
						서비스 이용 중 발견한 오류나 버그를 제보해주세요.
						가능하면 스크린샷이나 재현 방법을 함께 보내주시면 더욱 빠르게 해결할 수 있습니다.
					</p>
				</div>

				<div class="rounded-lg border p-4">
					<h3 class="mb-2 font-semibold">💡 기능 제안</h3>
					<p class="text-sm text-muted-foreground">
						서비스 개선을 위한 아이디어나 새로운 기능 제안을 환영합니다.
						사용자 여러분의 의견이 서비스 발전에 큰 도움이 됩니다.
					</p>
				</div>

				<div class="rounded-lg border p-4">
					<h3 class="mb-2 font-semibold">⚖️ 저작권 문의</h3>
					<p class="text-sm text-muted-foreground">
						저작권 침해 신고 또는 콘텐츠 삭제 요청은 이메일로 보내주세요.
						게시글 URL과 삭제 사유를 함께 보내주시면 즉시 조치하겠습니다.
					</p>
				</div>

				<div class="rounded-lg border p-4">
					<h3 class="mb-2 font-semibold">❓ 일반 문의</h3>
					<p class="text-sm text-muted-foreground">
						서비스 이용 방법, 계정 관련 문의, 기타 궁금한 사항을 문의해주세요.
					</p>
				</div>

				<div class="rounded-lg border p-4">
					<h3 class="mb-2 font-semibold">🤝 제휴 문의</h3>
					<p class="text-sm text-muted-foreground">
						광고, 제휴, 협업 등 비즈니스 관련 문의를 환영합니다.
					</p>
				</div>
			</div>
		</section>

		<Separator class="my-8" />

		<!-- 주의사항 -->
		<section class="mb-12">
			<div class="rounded-lg border border-amber-500/50 bg-amber-500/10 p-6">
				<div class="mb-3 flex items-center gap-2">
					<AlertCircle class="h-5 w-5 text-amber-600 dark:text-amber-400" />
					<h3 class="text-lg font-semibold">문의 전 확인사항</h3>
				</div>
				<ul class="ml-6 list-disc space-y-2 text-sm text-muted-foreground">
					<li>
						<a href="/about" class="text-primary hover:underline">서비스 소개</a> 페이지에서 
						기본적인 서비스 정보를 확인하실 수 있습니다.
					</li>
					<li>
						<a href="/privacy" class="text-primary hover:underline">개인정보처리방침</a>과 
						<a href="/terms" class="text-primary hover:underline">이용약관</a>을 먼저 확인해주세요.
					</li>
					<li>
						문의 시 구체적인 상황 설명과 함께 스크린샷을 첨부해주시면 
						더욱 정확하고 빠른 답변이 가능합니다.
					</li>
					<li>
						스팸성 메일이나 광고성 메일은 답변하지 않습니다.
					</li>
				</ul>
			</div>
		</section>

		<!-- 운영 시간 -->
		<section class="mb-12">
			<h2 class="mb-4 text-2xl font-semibold">운영 시간</h2>
			<div class="rounded-lg border bg-card p-6">
				<div class="grid gap-4 md:grid-cols-2">
					<div>
						<p class="mb-2 font-medium">이메일 확인</p>
						<p class="text-sm text-muted-foreground">
							평일: 오전 9시 - 오후 6시<br />
							주말/공휴일: 부정기적 확인
						</p>
					</div>
					<div>
						<p class="mb-2 font-medium">서비스 운영</p>
						<p class="text-sm text-muted-foreground">
							24시간 365일 자동 운영<br />
							크롤링: 10분마다 자동 업데이트
						</p>
					</div>
				</div>
			</div>
		</section>

		<!-- 마지막 업데이트 -->
		<div class="mt-12 text-center text-sm text-muted-foreground">
			마지막 업데이트: 2026년 1월 12일
		</div>
	</div>
</div>

<style>
	.prose {
		max-width: none;
	}
</style>
