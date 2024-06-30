<script lang="ts">
	import { page } from "$app/stores";
	import Matchup from "$lib/components/tournament/Matchup.svelte";

	let tournament: Tournament;
	let rounds: TournamentGame[][];

	$: tournament = $page.data.tournament;
	$: rounds = $page.data.arrangedGames;

</script>

<div class="d-flex flex-row justify-content-center card border-2 mb-2 flex-grow-1">
	<div class="bracket d-flex flex-row my-auto">
		{#each rounds as games}
			<div class="round d-flex flex-column justify-content-between">
				{#each games as game}
					<div class="matchup flex-grow-1 d-flex align-items-center py-2">
						<Matchup {game} />
					</div>
				{/each}
			</div>
			<div class="connectors d-flex flex-column">
				{#each games as _}
					<div class="connector flex-grow-1 position-relative" />
				{/each}
			</div>
		{/each}

		<div class="round final d-flex flex-column justify-content-between">
			<div class="matchup flex-grow-1 d-flex align-items-center py-2">
				<Matchup game={rounds[rounds.length - 1][0]} />
			</div>
		</div>
	</div>
</div>

<div class="buttons d-flex flex-row">
	<button type="button" class="btn btn-primary">Submit</button>
</div>

<style>
	.connectors {
		--connector-width: 2px;
		min-width: 4rem;
	}

	.connector::before {
		content: "";
		position: absolute;
		width: 50%;
		height: 50%;
	}

	.connector:nth-child(2n + 1)::before {
		content: "";
		position: absolute;
		top: calc(50% - var(--connector-width) / 2);
		width: 50%;
		height: 75%;
		border-top: var(--connector-width) solid var(--bs-border-color);
		border-right: var(--connector-width) solid var(--bs-border-color);
		border-radius: 0 0.375rem 0 0;
	}

	.connector:nth-child(2n)::before {
		content: "";
		position: absolute;
		bottom: calc(50% - var(--connector-width) / 2);
		width: 50%;
		height: 75%;
		border-bottom: var(--connector-width) solid var(--bs-border-color);
		border-right: var(--connector-width) solid var(--bs-border-color);
		border-radius: 0 0 0.375rem 0;
	}

	.connector:nth-child(2n + 1)::after {
		content: "";
		position: absolute;
		top: calc(50% + var(--connector-width) / 2);
		left: 50%;
		width: 50%;
		height: 50%;
		border-bottom: var(--connector-width) solid var(--bs-border-color);
	}
</style>
