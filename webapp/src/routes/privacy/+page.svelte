<script lang="ts">
	import { Separator } from '$lib/components/ui/separator'
	import { getBaseUrl, SITE_NAME } from '$lib/utils/seo'

	const baseUrl = getBaseUrl()
</script>

<svelte:head>
	<title>개인정보처리방침 - KEERO</title>
	<meta name="description" content="KEERO 개인정보처리방침" />
	
	<!-- Open Graph -->
	<meta property="og:site_name" content={SITE_NAME} />
	<meta property="og:title" content="개인정보처리방침 - KEERO" />
	<meta property="og:description" content="KEERO 개인정보처리방침" />
	<meta property="og:type" content="website" />
	<meta property="og:url" content="{baseUrl}/privacy" />
	<meta property="og:image" content="{baseUrl}/og-default.png" />
	
	<!-- Twitter Card -->
	<meta name="twitter:card" content="summary" />
	<meta name="twitter:title" content="개인정보처리방침 - KEERO" />
	<meta name="twitter:description" content="KEERO 개인정보처리방침" />
	
	<!-- Canonical -->
	<link rel="canonical" href="{baseUrl}/privacy" />
</svelte:head>

<div class="mx-auto max-w-4xl px-4 py-12">
	<h1 class="mb-8 text-4xl font-bold">개인정보처리방침</h1>

	<div class="prose prose-neutral dark:prose-invert max-w-none">
		<!-- 목차 -->
		<div class="mb-8 rounded-lg border bg-muted/50 p-6">
			<h3 class="mb-4 text-lg font-semibold">목차</h3>
			<ol class="space-y-2 text-sm">
				<li><a href="#section1" class="text-primary hover:underline">1. 개인정보의 수집 항목 및 방법</a></li>
				<li><a href="#section2" class="text-primary hover:underline">2. 개인정보의 수집 및 이용 목적</a></li>
				<li><a href="#section3" class="text-primary hover:underline">3. 개인정보의 보유 및 이용 기간</a></li>
				<li><a href="#section4" class="text-primary hover:underline">4. 개인정보의 제3자 제공</a></li>
				<li><a href="#section5" class="text-primary hover:underline">5. 개인정보의 파기</a></li>
				<li><a href="#section6" class="text-primary hover:underline">6. 이용자의 권리와 행사 방법</a></li>
				<li><a href="#section7" class="text-primary hover:underline">7. 쿠키의 운용</a></li>
				<li><a href="#section8" class="text-primary hover:underline">8. 개인정보 보호책임자</a></li>
				<li><a href="#section9" class="text-primary hover:underline">9. 개인정보처리방침 변경</a></li>
			</ol>
		</div>

		<!-- 1. 수집 항목 -->
		<section id="section1" class="mb-12">
			<h2 class="mb-4 text-2xl font-semibold">1. 개인정보의 수집 항목 및 방법</h2>
			
			<h3 class="mb-3 text-xl font-medium">수집 항목</h3>
			<div class="mb-4 rounded-lg border p-4">
				<p class="mb-2 font-medium">회원가입 시 (필수)</p>
				<ul class="ml-6 list-disc space-y-1 text-muted-foreground">
					<li>이메일 주소</li>
					<li>비밀번호 (암호화 저장)</li>
				</ul>
			</div>

			<div class="mb-4 rounded-lg border p-4">
				<p class="mb-2 font-medium">서비스 이용 시 (자동 수집)</p>
				<ul class="ml-6 list-disc space-y-1 text-muted-foreground">
					<li>IP 주소</li>
					<li>쿠키 및 세션 정보</li>
					<li>서비스 이용 기록</li>
					<li>접속 로그</li>
				</ul>
			</div>

			<h3 class="mb-3 mt-6 text-xl font-medium">수집 방법</h3>
			<ul class="ml-6 list-disc space-y-2 text-muted-foreground">
				<li>회원가입 및 서비스 이용 과정에서 이용자가 직접 입력</li>
				<li>서비스 이용 중 자동 생성 및 수집</li>
			</ul>
		</section>

		<Separator class="my-8" />

		<!-- 2. 수집 및 이용 목적 -->
		<section id="section2" class="mb-12">
			<h2 class="mb-4 text-2xl font-semibold">2. 개인정보의 수집 및 이용 목적</h2>
			<ul class="ml-6 list-disc space-y-2 text-muted-foreground">
				<li><strong>회원 관리:</strong> 회원제 서비스 제공, 본인 확인, 부정 이용 방지</li>
				<li><strong>서비스 제공:</strong> 댓글 작성, 좋아요, 북마크 등 맞춤형 서비스 제공</li>
				<li><strong>서비스 개선:</strong> 신규 서비스 개발, 통계 분석, 서비스 품질 향상</li>
				<li><strong>고객 지원:</strong> 문의사항 응대, 공지사항 전달</li>
			</ul>
		</section>

		<Separator class="my-8" />

		<!-- 3. 보유 및 이용 기간 -->
		<section id="section3" class="mb-12">
			<h2 class="mb-4 text-2xl font-semibold">3. 개인정보의 보유 및 이용 기간</h2>
			<p class="mb-4 text-muted-foreground">
				회사는 이용자의 개인정보를 수집 목적이 달성될 때까지 보유하며, 목적 달성 후에는 지체 없이 파기합니다.
			</p>
			<div class="rounded-lg border p-4">
				<ul class="space-y-2 text-muted-foreground">
					<li><strong>회원 탈퇴 시:</strong> 즉시 파기 (단, 관련 법령에 따라 보존이 필요한 경우 예외)</li>
					<li><strong>법령에 따른 보존:</strong></li>
					<ul class="ml-6 mt-2 list-disc space-y-1">
						<li>계약 또는 청약철회 등에 관한 기록: 5년 (전자상거래법)</li>
						<li>소비자 불만 또는 분쟁처리 기록: 3년 (전자상거래법)</li>
						<li>접속 로그 기록: 3개월 (통신비밀보호법)</li>
					</ul>
				</ul>
			</div>
		</section>

		<Separator class="my-8" />

		<!-- 4. 제3자 제공 -->
		<section id="section4" class="mb-12">
			<h2 class="mb-4 text-2xl font-semibold">4. 개인정보의 제3자 제공</h2>
			<div class="rounded-lg border border-blue-500/50 bg-blue-500/10 p-4">
				<p class="text-muted-foreground">
					회사는 원칙적으로 이용자의 개인정보를 제3자에게 제공하지 않습니다. 
					다만, 다음의 경우에는 예외로 합니다:
				</p>
				<ul class="ml-6 mt-3 list-disc space-y-1 text-muted-foreground">
					<li>이용자가 사전에 동의한 경우</li>
					<li>법령의 규정에 의거하거나, 수사 목적으로 법령에 정해진 절차와 방법에 따라 수사기관의 요구가 있는 경우</li>
				</ul>
			</div>
		</section>

		<Separator class="my-8" />

		<!-- 5. 개인정보의 파기 -->
		<section id="section5" class="mb-12">
			<h2 class="mb-4 text-2xl font-semibold">5. 개인정보의 파기</h2>
			<p class="mb-4 text-muted-foreground">
				회사는 개인정보 보유기간의 경과, 처리목적 달성 등 개인정보가 불필요하게 되었을 때에는 
				지체 없이 해당 개인정보를 파기합니다.
			</p>
			<div class="rounded-lg border p-4">
				<p class="mb-2 font-medium">파기 절차 및 방법</p>
				<ul class="ml-6 list-disc space-y-2 text-muted-foreground">
					<li><strong>전자적 파일:</strong> 복구 및 재생이 불가능한 방법으로 영구 삭제</li>
					<li><strong>종이 문서:</strong> 분쇄기로 분쇄하거나 소각</li>
				</ul>
			</div>
		</section>

		<Separator class="my-8" />

		<!-- 6. 이용자의 권리 -->
		<section id="section6" class="mb-12">
			<h2 class="mb-4 text-2xl font-semibold">6. 이용자의 권리와 행사 방법</h2>
			<p class="mb-4 text-muted-foreground">
				이용자는 언제든지 다음과 같은 권리를 행사할 수 있습니다:
			</p>
			<ul class="ml-6 list-disc space-y-2 text-muted-foreground">
				<li>개인정보 열람 요구</li>
				<li>개인정보 정정 요구</li>
				<li>개인정보 삭제 요구</li>
				<li>개인정보 처리 정지 요구</li>
			</ul>
			<p class="mt-4 text-sm text-muted-foreground">
				권리 행사는 개인정보 보호책임자에게 이메일로 요청하실 수 있으며, 
				회사는 이에 대해 지체 없이 조치하겠습니다.
			</p>
		</section>

		<Separator class="my-8" />

		<!-- 7. 쿠키 -->
		<section id="section7" class="mb-12">
			<h2 class="mb-4 text-2xl font-semibold">7. 쿠키의 운용</h2>
			<p class="mb-4 text-muted-foreground">
				회사는 이용자에게 개인화되고 맞춤화된 서비스를 제공하기 위해 쿠키를 사용합니다.
			</p>
			<div class="rounded-lg border p-4">
				<p class="mb-2 font-medium">쿠키의 사용 목적</p>
				<ul class="ml-6 list-disc space-y-1 text-muted-foreground">
					<li>로그인 세션 유지</li>
					<li>사용자 설정 저장 (다크모드 등)</li>
					<li>서비스 이용 통계 분석</li>
				</ul>
				<p class="mt-4 text-sm text-muted-foreground">
					이용자는 웹 브라우저 설정을 통해 쿠키 저장을 거부할 수 있습니다. 
					다만, 쿠키 저장을 거부할 경우 일부 서비스 이용에 제한이 있을 수 있습니다.
				</p>
			</div>
		</section>

		<Separator class="my-8" />

		<!-- 8. 개인정보 보호책임자 -->
		<section id="section8" class="mb-12">
			<h2 class="mb-4 text-2xl font-semibold">8. 개인정보 보호책임자</h2>
			<div class="rounded-lg border bg-card p-6">
				<p class="mb-4 text-muted-foreground">
					회사는 개인정보 처리에 관한 업무를 총괄해서 책임지고, 
					개인정보 처리와 관련한 정보주체의 불만처리 및 피해구제를 위하여 
					아래와 같이 개인정보 보호책임자를 지정하고 있습니다.
				</p>
				<div class="space-y-2 text-sm">
					<p>
						<strong class="text-foreground">이메일:</strong>
						<a href="mailto:keero1356@gmail.com" class="ml-2 text-primary hover:underline">
							keero1356@gmail.com
						</a>
					</p>
				</div>
			</div>
		</section>

		<Separator class="my-8" />

		<!-- 9. 방침 변경 -->
		<section id="section9" class="mb-12">
			<h2 class="mb-4 text-2xl font-semibold">9. 개인정보처리방침 변경</h2>
			<p class="text-muted-foreground">
				이 개인정보처리방침은 법령, 정책 또는 보안기술의 변경에 따라 내용이 추가, 삭제 및 수정될 수 있으며, 
				변경 시에는 최소 7일 전에 공지사항을 통해 고지하겠습니다.
			</p>
		</section>

		<!-- 시행일 -->
		<div class="mt-12 rounded-lg border bg-muted/50 p-4 text-center">
			<p class="text-sm text-muted-foreground">
				<strong>시행일:</strong> 2026년 1월 1일
			</p>
		</div>
	</div>
</div>

<style>
	.prose {
		max-width: none;
	}
	
	.prose h2 {
		scroll-margin-top: 2rem;
	}
</style>
