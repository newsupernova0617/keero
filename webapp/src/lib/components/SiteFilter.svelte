<script lang="ts">
	import * as Tabs from '$lib/components/ui/tabs'
	
	let { onFilterChange }: { onFilterChange: (site: string) => void } = $props()
	
	let selectedSite = $state('all')
	
	const sites = [
		{ value: 'all', label: '전체' },
		{ value: 'ruliweb', label: '루리웹' },
		{ value: 'fmkorea', label: 'FMKorea' },
		{ value: 'mlbpark', label: 'MLBPark' },
		{ value: 'clien', label: 'Clien' },
		{ value: 'humoruniv', label: '웃긴대학' },
		{ value: 'dogdrip', label: 'Dogdrip' },
		{ value: 'todayhumor', label: '오늘의유머' },
		{ value: 'ppomppu', label: '뽐뿌' }
	]
</script>

<Tabs.Root value={selectedSite} onValueChange={(val) => { selectedSite = val; onFilterChange(val); }}>
	<Tabs.List class="w-full justify-start overflow-x-auto">
		{#each sites as site}
			<Tabs.Trigger value={site.value} class="whitespace-nowrap">
				{site.label}
			</Tabs.Trigger>
		{/each}
	</Tabs.List>
</Tabs.Root>
