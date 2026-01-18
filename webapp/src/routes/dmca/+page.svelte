<script lang="ts">
	import { Separator } from '$lib/components/ui/separator'
	import { AlertTriangle, Mail, FileText, Clock, Shield, CheckCircle } from '@lucide/svelte'
	import { getBaseUrl, SITE_NAME } from '$lib/utils/seo'

	const baseUrl = getBaseUrl()
</script>

<svelte:head>
	<title>저작권 정책 (DMCA) - KEERO</title>
	<meta name="description" content="KEERO 저작권 정책 및 DMCA 침해 신고 절차 안내" />
	
	<!-- Open Graph -->
	<meta property="og:site_name" content={SITE_NAME} />
	<meta property="og:title" content="저작권 정책 (DMCA) - KEERO" />
	<meta property="og:description" content="KEERO 저작권 정책 및 DMCA 침해 신고 절차 안내" />
	<meta property="og:type" content="website" />
	<meta property="og:url" content="{baseUrl}/dmca" />
	<meta property="og:image" content="{baseUrl}/og-default.png" />
	
	<!-- Twitter Card -->
	<meta name="twitter:card" content="summary" />
	<meta name="twitter:title" content="저작권 정책 (DMCA) - KEERO" />
	<meta name="twitter:description" content="KEERO 저작권 정책 및 DMCA 침해 신고 절차 안내" />
	
	<!-- Canonical -->
	<link rel="canonical" href="{baseUrl}/dmca" />
</svelte:head>

<div class="mx-auto max-w-4xl px-4 py-12">
	<h1 class="mb-8 text-4xl font-bold flex items-center gap-3">
		<Shield class="h-10 w-10 text-primary" />
		저작권 정책 (DMCA)
	</h1>

	<div class="prose prose-neutral dark:prose-invert max-w-none">
		<!-- 개요 -->
		<section class="mb-12">
			<div class="rounded-lg border border-blue-500/50 bg-blue-500/10 p-6">
				<div class="flex items-start gap-3">
					<FileText class="h-6 w-6 text-blue-500 flex-shrink-0 mt-1" />
					<div>
						<h2 class="text-xl font-semibold mb-2 mt-0">저작권 보호 정책</h2>
						<p class="text-muted-foreground mb-0">
							KEERO는 저작권법 및 DMCA(Digital Millennium Copyright Act)를 존중합니다.
							본 서비스에 게시된 모든 콘텐츠의 저작권은 원저작자에게 있으며,
							저작권 침해가 확인된 콘텐츠는 즉시 삭제 조치합니다.
						</p>
					</div>
				</div>
			</div>
		</section>

		<Separator class="my-8" />

		<!-- 콘텐츠 출처 -->
		<section class="mb-12">
			<h2 class="mb-4 text-2xl font-semibold">콘텐츠 출처 안내</h2>
			<p class="text-muted-foreground mb-4">
				KEERO는 다음 커뮤니티 사이트의 공개된 게시글을 수집하여 제공합니다:
			</p>
			<ul class="ml-6 list-disc space-y-2 text-muted-foreground">
				<li>뽐뿌 유머게시판</li>
				<li>FM코리아 베스트</li>
				<li>오늘의유머 베오베</li>
				<li>루리웹 유머게시판</li>
				<li>웃긴대학</li>
			</ul>
			<p class="mt-4 text-muted-foreground">
				모든 게시글에는 원본 출처가 명시되어 있으며, 원본 사이트로 이동할 수 있는 링크를 제공합니다.
			</p>
		</section>

		<Separator class="my-8" />

		<!-- 신고 절차 -->
		<section class="mb-12">
			<h2 class="mb-6 text-2xl font-semibold flex items-center gap-2">
				<AlertTriangle class="h-6 w-6 text-amber-500" />
				저작권 침해 신고 절차
			</h2>
			
			<p class="text-muted-foreground mb-6">
				귀하의 저작물이 본 서비스에서 무단으로 사용되고 있다고 판단되는 경우,
				아래 절차에 따라 삭제를 요청하실 수 있습니다.
			</p>

			<div class="space-y-4">
				<div class="rounded-lg border p-4">
					<h3 class="text-lg font-semibold mb-3">1단계: 신고 메일 작성</h3>
					<p class="text-sm text-muted-foreground mb-3">
						아래 이메일 주소로 다음 정보를 포함하여 신고해주세요:
					</p>
					<a 
						href="mailto:keero1356@gmail.com?subject=[저작권 침해 신고]"
						class="inline-flex items-center gap-2 text-primary hover:underline"
					>
						<Mail class="h-4 w-4" />
						keero1356@gmail.com
					</a>
				</div>

				<div class="rounded-lg border p-4">
					<h3 class="text-lg font-semibold mb-3">2단계: 필수 정보 포함</h3>
					<ul class="ml-6 list-disc space-y-2 text-sm text-muted-foreground">
						<li><strong>침해 콘텐츠 URL</strong>: KEERO에서 해당 게시글의 URL</li>
						<li><strong>원본 콘텐츠 URL</strong>: 원본 저작물이 게재된 URL</li>
						<li><strong>저작권 소유 증명</strong>: 본인이 저작권자임을 증명할 수 있는 자료</li>
						<li><strong>연락처</strong>: 회신을 받을 이메일 주소 또는 전화번호</li>
						<li><strong>진술서</strong>: 신고 내용이 사실임을 확인하는 진술</li>
					</ul>
				</div>

				<div class="rounded-lg border p-4">
					<h3 class="text-lg font-semibold mb-3">3단계: 처리 완료 대기</h3>
					<p class="text-sm text-muted-foreground">
						신고가 접수되면 검토 후 조치 결과를 이메일로 알려드립니다.
					</p>
				</div>
			</div>
		</section>

		<Separator class="my-8" />

		<!-- 처리 기한 -->
		<section class="mb-12">
			<h2 class="mb-4 text-2xl font-semibold flex items-center gap-2">
				<Clock class="h-6 w-6 text-green-500" />
				처리 기한
			</h2>
			
			<div class="grid gap-4 md:grid-cols-3">
				<div class="rounded-lg border bg-card p-4 text-center">
					<div class="text-3xl font-bold text-primary mb-2">24시간</div>
					<p class="text-sm text-muted-foreground">신고 접수 확인</p>
				</div>
				<div class="rounded-lg border bg-card p-4 text-center">
					<div class="text-3xl font-bold text-primary mb-2">48시간</div>
					<p class="text-sm text-muted-foreground">검토 완료</p>
				</div>
				<div class="rounded-lg border bg-card p-4 text-center">
					<div class="text-3xl font-bold text-primary mb-2">즉시</div>
					<p class="text-sm text-muted-foreground">확인 시 삭제</p>
				</div>
			</div>
		</section>

		<Separator class="my-8" />

		<!-- 반복 침해 정책 -->
		<section class="mb-12">
			<h2 class="mb-4 text-2xl font-semibold">반복 침해자 정책</h2>
			<div class="rounded-lg border border-red-500/50 bg-red-500/10 p-6">
				<p class="text-muted-foreground mb-0">
					KEERO는 반복적인 저작권 침해에 대해 엄격하게 대응합니다.
					동일 출처에서 반복적인 침해 신고가 접수될 경우,
					해당 출처의 콘텐츠 수집을 중단하거나 영구적으로 차단할 수 있습니다.
				</p>
			</div>
		</section>

		<Separator class="my-8" />

		<!-- 면책 조항 -->
		<section class="mb-12">
			<h2 class="mb-4 text-2xl font-semibold">면책 조항</h2>
			<div class="space-y-4 text-muted-foreground">
				<p>
					1. KEERO는 공개된 커뮤니티 게시글을 자동으로 수집하여 제공하는 서비스입니다.
					수집된 콘텐츠의 저작권은 원저작자에게 있습니다.
				</p>
				<p>
					2. KEERO는 수집된 콘텐츠의 정확성, 완전성, 적법성에 대해 보증하지 않습니다.
				</p>
				<p>
					3. 저작권 침해 신고가 접수된 경우, KEERO는 검토 후 적절한 조치를 취하며,
					이로 인한 어떠한 손해에 대해서도 책임지지 않습니다.
				</p>
				<p>
					4. 허위 신고로 인한 법적 책임은 신고자에게 있습니다.
				</p>
			</div>
		</section>

		<Separator class="my-8" />

		<!-- Counter Notice -->
		<section class="mb-12">
			<h2 class="mb-4 text-2xl font-semibold">이의 제기 (Counter Notice)</h2>
			<p class="text-muted-foreground mb-4">
				귀하의 콘텐츠가 저작권 침해로 잘못 삭제되었다고 판단되는 경우,
				이의 제기서를 제출하실 수 있습니다.
			</p>
			<div class="rounded-lg border p-4">
				<h3 class="text-lg font-semibold mb-3">이의 제기 시 필요 정보</h3>
				<ul class="ml-6 list-disc space-y-2 text-sm text-muted-foreground">
					<li>삭제된 콘텐츠 설명</li>
					<li>삭제가 부당하다고 생각하는 이유</li>
					<li>본인 연락처 및 서명</li>
					<li>법적 절차에 동의한다는 진술</li>
				</ul>
			</div>
		</section>

		<!-- 연락처 -->
		<section class="mb-12">
			<h2 class="mb-4 text-2xl font-semibold flex items-center gap-2">
				<Mail class="h-6 w-6" />
				연락처
			</h2>
			<div class="rounded-lg border bg-card p-6">
				<div class="space-y-3">
					<div class="flex items-center gap-3">
						<span class="font-medium w-24">이메일:</span>
						<a href="mailto:keero1356@gmail.com" class="text-primary hover:underline">
							keero1356@gmail.com
						</a>
					</div>
					<div class="flex items-center gap-3">
						<span class="font-medium w-24">운영:</span>
						<span class="text-muted-foreground">KEERO (개인 운영)</span>
					</div>
				</div>
			</div>
		</section>

		<!-- 마지막 업데이트 -->
		<div class="mt-12 rounded-lg border bg-muted/50 p-4 text-center">
			<p class="text-sm text-muted-foreground">
				<strong>시행일:</strong> 2026년 1월 12일
			</p>
		</div>
	</div>
</div>

<style>
	.prose {
		max-width: none;
	}
</style>
