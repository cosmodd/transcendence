<script lang="ts">
	import TournamentCard from "$lib/components/tournament/TournamentCard.svelte";

	const names = [
		"Battle Bash",
		"Infinite Invitational",
		"Battleground Brawl",
		"Iron Fist",
		"Brutal Brawl",
		"Iron Fist",
		"Extreme Encounter",
		"Ocean Odyssey",
		"Valiant Vendetta",
		"Legendary Lethal League",
		"Royal Rumble Challenge",
		"Shadow Cup",
		"Apocalypse Arena",
		"Sovereign Settle",
		"Colossal Combat",
		"Chaos Frenzy",
		"Interdimensional Invitational",
		"Carnage Cartel",
		"Colossal Combat",
		"Combat Chronicles",
	];

	const tournaments = Array.from({ length: 30 }, (_, i) => {
		const maxPlayers = Math.floor(Math.random() * 10) * 2 + 2;
		return {
			players: Array.from({ length: Math.floor(Math.random() * maxPlayers) }, (_, j) => `Player ${j + 1}`),
			maxPlayers,
			name: names[Math.floor(Math.random() * names.length)],
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
		grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
	}
</style>
