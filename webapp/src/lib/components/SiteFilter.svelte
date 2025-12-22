<script lang="ts">
	import * as Tabs from '$lib/components/ui/tabs'
	
	let { onFilterChange }: { onFilterChange: (site: string) => void } = $props()
	
	const sites = [
		{ value: 'all', label: '?ÑÏ≤¥' },
		{ value: 'ruliweb', label: 'Î£®Î¶¨?? },
		{ value: 'fmkorea', label: 'FMKorea' },
		{ value: 'mlbpark', label: 'MLBPark' },
		{ value: 'clien', label: 'Clien' },
		{ value: 'humoruniv', label: '?ÉÍ∏¥?Ä?? },
		{ value: 'dogdrip', label: 'Dogdrip' },
		{ value: 'todayhumor', label: '?§Îäò?òÏú†Î®? },
		{ value: 'ppomppu', label: 'ÎΩêÎøå' }
	]
</script>

<Tabs.Root defaultValue="all" onValueChange={onFilterChange}>
	<Tabs.List class="w-full justify-start overflow-x-auto">
		{#each sites as site}
			<Tabs.Trigger value={site.value} class="whitespace-nowrap">
				{site.label}
			</Tabs.Trigger>
		{/each}
	</Tabs.List>
</Tabs.Root>
