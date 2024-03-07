<script lang="ts">
	import TournamentCard from "$lib/components/TournamentCard.svelte";

	const tournaments = Array.from({length: 30}, (_, i) => {
		const maxPlayers = Math.floor(Math.random() * 10) * 2 + 2;
		return {
			players: Array.from({length: Math.floor(Math.random() * maxPlayers)}, (_, j) => `Player ${j + 1}`),
			maxPlayers,
			state: Math.floor(Math.random() * 3) as 0 | 1 | 2,
			name: `Tournament ${i + 1}`,
			id: i
		};
	});
</script>

<div class="tournaments d-flex flex-column h-100 overflow-y-auto">
	{#each tournaments as tournament}
		<TournamentCard tournament={tournament} />
	{/each}
</div>

<style>
	.tournaments {
		display: grid;
		
	}
</style>