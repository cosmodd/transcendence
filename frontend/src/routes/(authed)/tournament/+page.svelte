<script lang="ts">
	import TournamentCard from "$lib/components/tournament/TournamentCard.svelte";
    import { authedFetch } from "$lib/stores/auth";
    import { onMount } from "svelte";

	interface Tournament {
		name: string;
		id: number;
		status: string;
		players_count: number;
		size: "eight" | "four";
	};

	let tournaments: Tournament[] = [];

	onMount(async () => {
		const response = await authedFetch("/api/tournament/");
		tournaments = await response.json();
	});
</script>

<div class="container h-100 d-flex flex-column">
	<h1 class="fw-bold mb-3">Tournaments</h1>
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
