<script lang="ts">
	import TournamentCard from "$lib/components/TournamentCard.svelte";

	const tournaments = Array.from({ length: 30 }, (_, i) => {
		const maxPlayers = Math.floor(Math.random() * 10) * 2 + 2;
		return {
			players: Array.from({ length: Math.floor(Math.random() * maxPlayers) }, (_, j) => `Player ${j + 1}`),
			maxPlayers,
			name: `Tournament ${i + 1}`,
			id: i,
		};
	});
</script>

<div class="container h-100 d-flex flex-column">
	<h1 class="fw-bold">Tournaments</h1>
	<div class="tournaments h-100 overflow-y-auto gap-3">
		{#each tournaments as tournament}
			<TournamentCard {tournament} />
		{/each}
	</div>
</div>

<style>
	.tournaments {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
	}
</style>
