<script lang="ts">
	import { Separator } from '$lib/components/ui/separator'
</script>

<svelte:head>
	<title>이용약관 - KEERO</title>
	<meta name="description" content="KEERO 이용약관" />
</svelte:head>

<div class="mx-auto max-w-4xl px-4 py-12">
	<h1 class="mb-8 text-4xl font-bold">이용약관</h1>

	<div class="prose prose-neutral dark:prose-invert max-w-none">
		<!-- 목차 -->
		<div class="mb-8 rounded-lg border bg-muted/50 p-6">
			<h3 class="mb-4 text-lg font-semibold">목차</h3>
			<ol class="space-y-2 text-sm">
				<li><a href="#section1" class="text-primary hover:underline">제1조 (목적)</a></li>
				<li><a href="#section2" class="text-primary hover:underline">제2조 (용어의 정의)</a></li>
				<li><a href="#section3" class="text-primary hover:underline">제3조 (약관의 효력 및 변경)</a></li>
				<li><a href="#section4" class="text-primary hover:underline">제4조 (회원가입)</a></li>
				<li><a href="#section5" class="text-primary hover:underline">제5조 (회원 탈퇴 및 자격 상실)</a></li>
				<li><a href="#section6" class="text-primary hover:underline">제6조 (서비스의 제공 및 변경)</a></li>
				<li><a href="#section7" class="text-primary hover:underline">제7조 (서비스의 중단)</a></li>
				<li><a href="#section8" class="text-primary hover:underline">제8조 (회원의 의무)</a></li>
				<li><a href="#section9" class="text-primary hover:underline">제9조 (게시물의 관리)</a></li>
				<li><a href="#section10" class="text-primary hover:underline">제10조 (저작권의 귀속 및 이용제한)</a></li>
				<li><a href="#section11" class="text-primary hover:underline">제11조 (면책조항)</a></li>
				<li><a href="#section12" class="text-primary hover:underline">제12조 (분쟁의 해결)</a></li>
			</ol>
		</div>

		<!-- 제1조 -->
		<section id="section1" class="mb-12">
			<h2 class="mb-4 text-2xl font-semibold">제1조 (목적)</h2>
			<p class="text-muted-foreground">
				본 약관은 KEERO(이하 "회사")이 제공하는 서비스의 이용과 관련하여 
				회사와 이용자 간의 권리, 의무 및 책임사항, 기타 필요한 사항을 규정함을 목적으로 합니다.
			</p>
		</section>

		<Separator class="my-8" />

		<!-- 제2조 -->
		<section id="section2" class="mb-12">
			<h2 class="mb-4 text-2xl font-semibold">제2조 (용어의 정의)</h2>
			<div class="space-y-3">
				<div class="rounded-lg border p-4">
					<p class="mb-2"><strong>1. "서비스"</strong></p>
					<p class="text-sm text-muted-foreground">
						회사가 제공하는 유머 게시글 통합 플랫폼 및 관련 부가 서비스를 의미합니다.
					</p>
				</div>
				<div class="rounded-lg border p-4">
					<p class="mb-2"><strong>2. "회원"</strong></p>
					<p class="text-sm text-muted-foreground">
						본 약관에 따라 회사와 이용계약을 체결하고 회사가 제공하는 서비스를 이용하는 자를 의미합니다.
					</p>
				</div>
				<div class="rounded-lg border p-4">
					<p class="mb-2"><strong>3. "게시물"</strong></p>
					<p class="text-sm text-muted-foreground">
						회원이 서비스를 이용함에 있어 서비스에 게시한 댓글, 좋아요, 북마크 등의 정보를 의미합니다.
					</p>
				</div>
			</div>
		</section>

		<Separator class="my-8" />

		<!-- 제3조 -->
		<section id="section3" class="mb-12">
			<h2 class="mb-4 text-2xl font-semibold">제3조 (약관의 효력 및 변경)</h2>
			<ol class="ml-6 list-decimal space-y-3 text-muted-foreground">
				<li>
					본 약관은 서비스 화면에 게시하거나 기타의 방법으로 회원에게 공지함으로써 효력이 발생합니다.
				</li>
				<li>
					회사는 필요한 경우 관련 법령을 위배하지 않는 범위에서 본 약관을 변경할 수 있으며, 
					약관이 변경되는 경우 변경사항을 시행일자 7일 전부터 공지합니다.
				</li>
				<li>
					회원이 변경된 약관에 동의하지 않는 경우, 서비스 이용을 중단하고 탈퇴할 수 있습니다. 
					변경된 약관의 효력 발생일 이후에도 서비스를 계속 이용하는 경우 약관 변경에 동의한 것으로 간주됩니다.
				</li>
			</ol>
		</section>

		<Separator class="my-8" />

		<!-- 제4조 -->
		<section id="section4" class="mb-12">
			<h2 class="mb-4 text-2xl font-semibold">제4조 (회원가입)</h2>
			<ol class="ml-6 list-decimal space-y-3 text-muted-foreground">
				<li>
					회원가입은 이용자가 약관의 내용에 동의하고, 회사가 정한 가입 양식에 따라 
					회원정보를 기입한 후 가입 신청을 완료함으로써 이루어집니다.
				</li>
				<li>
					회사는 다음 각 호에 해당하는 신청에 대해서는 승인을 거부하거나 사후에 이용계약을 해지할 수 있습니다:
					<ul class="ml-6 mt-2 list-disc space-y-1">
						<li>타인의 명의를 도용한 경우</li>
						<li>허위 정보를 기재한 경우</li>
						<li>사회의 안녕질서 또는 미풍양속을 저해할 목적으로 신청한 경우</li>
						<li>기타 회사가 정한 이용신청 요건이 미비한 경우</li>
					</ul>
				</li>
			</ol>
		</section>

		<Separator class="my-8" />

		<!-- 제5조 -->
		<section id="section5" class="mb-12">
			<h2 class="mb-4 text-2xl font-semibold">제5조 (회원 탈퇴 및 자격 상실)</h2>
			<ol class="ml-6 list-decimal space-y-3 text-muted-foreground">
				<li>
					회원은 언제든지 서비스 내 설정 메뉴를 통해 회원 탈퇴를 요청할 수 있으며, 
					회사는 즉시 회원 탈퇴를 처리합니다.
				</li>
				<li>
					회원이 다음 각 호의 사유에 해당하는 경우, 회사는 회원 자격을 제한 또는 정지시킬 수 있습니다:
					<ul class="ml-6 mt-2 list-disc space-y-1">
						<li>가입 신청 시 허위 내용을 등록한 경우</li>
						<li>다른 사람의 서비스 이용을 방해하거나 정보를 도용하는 등 전자상거래 질서를 위협하는 경우</li>
						<li>서비스를 이용하여 법령 또는 본 약관이 금지하는 행위를 하는 경우</li>
					</ul>
				</li>
			</ol>
		</section>

		<Separator class="my-8" />

		<!-- 제6조 -->
		<section id="section6" class="mb-12">
			<h2 class="mb-4 text-2xl font-semibold">제6조 (서비스의 제공 및 변경)</h2>
			<ol class="ml-6 list-decimal space-y-3 text-muted-foreground">
				<li>
					회사는 다음과 같은 서비스를 제공합니다:
					<ul class="ml-6 mt-2 list-disc space-y-1">
						<li>여러 커뮤니티 사이트의 유머 게시글 통합 제공</li>
						<li>댓글 작성, 좋아요, 북마크 기능</li>
						<li>게시글 검색 기능</li>
						<li>기타 회사가 추가 개발하거나 제휴계약 등을 통해 제공하는 서비스</li>
					</ul>
				</li>
				<li>
					회사는 서비스의 내용을 변경할 경우 변경사항을 서비스 화면에 공지합니다.
				</li>
			</ol>
		</section>

		<Separator class="my-8" />

		<!-- 제7조 -->
		<section id="section7" class="mb-12">
			<h2 class="mb-4 text-2xl font-semibold">제7조 (서비스의 중단)</h2>
			<ol class="ml-6 list-decimal space-y-3 text-muted-foreground">
				<li>
					회사는 컴퓨터 등 정보통신설비의 보수점검, 교체 및 고장, 통신의 두절 등의 사유가 발생한 경우에는 
					서비스의 제공을 일시적으로 중단할 수 있습니다.
				</li>
				<li>
					회사는 제1항의 사유로 서비스의 제공이 일시적으로 중단됨으로 인하여 
					회원 또는 제3자가 입은 손해에 대하여 배상하지 않습니다. 
					다만, 회사의 고의 또는 중과실에 의한 경우에는 그러하지 아니합니다.
				</li>
			</ol>
		</section>

		<Separator class="my-8" />

		<!-- 제8조 -->
		<section id="section8" class="mb-12">
			<h2 class="mb-4 text-2xl font-semibold">제8조 (회원의 의무)</h2>
			<p class="mb-4 text-muted-foreground">회원은 다음 행위를 하여서는 안 됩니다:</p>
			<div class="rounded-lg border border-red-500/50 bg-red-500/10 p-4">
				<ul class="ml-6 list-disc space-y-2 text-sm text-muted-foreground">
					<li>신청 또는 변경 시 허위 내용의 등록</li>
					<li>타인의 정보 도용</li>
					<li>회사가 게시한 정보의 변경</li>
					<li>회사가 정한 정보 이외의 정보(컴퓨터 프로그램 등) 등의 송신 또는 게시</li>
					<li>회사와 기타 제3자의 저작권 등 지적재산권에 대한 침해</li>
					<li>회사 및 기타 제3자의 명예를 손상시키거나 업무를 방해하는 행위</li>
					<li>외설 또는 폭력적인 메시지, 화상, 음성, 기타 공서양속에 반하는 정보를 서비스에 공개 또는 게시하는 행위</li>
					<li>스팸성 댓글 또는 광고성 게시물 작성</li>
					<li>서비스를 이용한 영리 행위</li>
				</ul>
			</div>
		</section>

		<Separator class="my-8" />

		<!-- 제9조 -->
		<section id="section9" class="mb-12">
			<h2 class="mb-4 text-2xl font-semibold">제9조 (게시물의 관리)</h2>
			<ol class="ml-6 list-decimal space-y-3 text-muted-foreground">
				<li>
					회원의 게시물(댓글 등)이 정보통신망법 및 저작권법 등 관련법에 위반되는 내용을 포함하는 경우, 
					권리자는 관련법이 정한 절차에 따라 해당 게시물의 게시중단 및 삭제 등을 요청할 수 있으며, 
					회사는 관련법에 따라 조치를 취하여야 합니다.
				</li>
				<li>
					회사는 전항에 따른 권리자의 요청이 없는 경우라도 권리침해가 인정될 만한 사유가 있거나 
					기타 회사 정책 및 관련법에 위반되는 경우에는 관련법에 따라 해당 게시물에 대해 
					임시조치 등을 취할 수 있습니다.
				</li>
			</ol>
		</section>

		<Separator class="my-8" />

		<!-- 제10조 -->
		<section id="section10" class="mb-12">
			<h2 class="mb-4 text-2xl font-semibold">제10조 (저작권의 귀속 및 이용제한)</h2>
			<ol class="ml-6 list-decimal space-y-3 text-muted-foreground">
				<li>
					회사가 작성한 저작물에 대한 저작권 기타 지적재산권은 회사에 귀속합니다.
				</li>
				<li>
					회원이 서비스 내에 게시한 게시물의 저작권은 해당 게시물의 저작자에게 귀속됩니다.
				</li>
				<li>
					회원은 서비스를 이용하여 얻은 정보 중 회사에게 지적재산권이 귀속된 정보를 
					회사의 사전 승낙 없이 복제, 송신, 출판, 배포, 방송 기타 방법에 의하여 
					영리목적으로 이용하거나 제3자에게 이용하게 하여서는 안됩니다.
				</li>
				<li>
					서비스에 게시된 원본 게시글의 저작권은 원저작자에게 있으며, 
					회사는 출처를 명시하고 원본 링크를 제공합니다.
				</li>
			</ol>
		</section>

		<Separator class="my-8" />

		<!-- 제11조 -->
		<section id="section11" class="mb-12">
			<h2 class="mb-4 text-2xl font-semibold">제11조 (면책조항)</h2>
			<ol class="ml-6 list-decimal space-y-3 text-muted-foreground">
				<li>
					회사는 천재지변 또는 이에 준하는 불가항력으로 인하여 서비스를 제공할 수 없는 경우에는 
					서비스 제공에 관한 책임이 면제됩니다.
				</li>
				<li>
					회사는 회원의 귀책사유로 인한 서비스 이용의 장애에 대하여는 책임을 지지 않습니다.
				</li>
				<li>
					회사는 회원이 서비스를 이용하여 기대하는 수익을 상실한 것에 대하여 책임을 지지 않으며, 
					그 밖에 서비스를 통하여 얻은 자료로 인한 손해에 관하여 책임을 지지 않습니다.
				</li>
				<li>
					회사는 회원이 게재한 정보, 자료, 사실의 신뢰도, 정확성 등의 내용에 관하여는 책임을 지지 않습니다.
				</li>
				<li>
					회사는 서비스 이용과 관련하여 회원에게 발생한 손해 가운데 
					회원의 고의, 과실에 의한 손해에 대하여 책임을 지지 않습니다.
				</li>
			</ol>
		</section>

		<Separator class="my-8" />

		<!-- 제12조 -->
		<section id="section12" class="mb-12">
			<h2 class="mb-4 text-2xl font-semibold">제12조 (분쟁의 해결)</h2>
			<ol class="ml-6 list-decimal space-y-3 text-muted-foreground">
				<li>
					회사는 회원이 제기하는 정당한 의견이나 불만을 반영하고 그 피해를 보상처리하기 위하여 
					피해보상처리기구를 설치·운영합니다.
				</li>
				<li>
					회사와 회원 간에 발생한 전자상거래 분쟁과 관련하여 회원의 피해구제신청이 있는 경우에는 
					공정거래위원회 또는 시·도지사가 의뢰하는 분쟁조정기관의 조정에 따를 수 있습니다.
				</li>
				<li>
					회사와 회원 간 제기된 소송은 대한민국 법을 준거법으로 합니다.
				</li>
			</ol>
		</section>

		<!-- 부칙 -->
		<div class="mt-12 rounded-lg border bg-muted/50 p-4">
			<p class="mb-2 font-semibold">부칙</p>
			<p class="text-sm text-muted-foreground">
				<strong>시행일:</strong> 본 약관은 2025년 12월 30일부터 시행됩니다.
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
