<script lang="ts">
	import { invalidateAll } from "$app/navigation";
	import { page } from "$app/stores";
	import Matchup from "$lib/components/tournament/Matchup.svelte";
	import { faPlay, faUserPlus } from "@fortawesome/free-solid-svg-icons";
	import { onDestroy, onMount } from "svelte";
	import Fa from "svelte-fa";

	let tournament: Tournament;
	let rounds: TournamentGame[][];

	$: tournament = $page.data.tournament;
	$: rounds = $page.data.arrangedGames;

	$: status = tournament.status;

	let interval_id: NodeJS.Timeout | undefined;

	function reloadData() {
		if (tournament == null) return;
		if (!["looking_for_players", "in_progress"].includes(status)) return;

		invalidateAll();
	}

	onDestroy(() => {
		if (interval_id) clearInterval(interval_id);
	});

	onMount(() => {
		interval_id = setInterval(() => {
			reloadData();
		}, 2000);
	});
</script>

<svelte:window on:notification={() => reloadData()} />

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
			{#if games.length > 1}
				<div class="connectors d-flex flex-column">
					{#each games as _}
						<div class="connector flex-grow-1 position-relative" />
					{/each}
				</div>
			{/if}
		{/each}
	</div>
</div>

{#if ["looking_for_players", "in_progress"].includes(status)}
	<div class="buttons d-flex flex-row justify-content-center gap-2">
		<a href="/game/online" class="btn btn-primary px-4 {status !== 'in_progress' ? 'disabled' : ''}">
			<Fa icon={faPlay} class="me-2" />
			Play your next game
		</a>
	</div>
{/if}

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
