<script lang="ts">
	import Matchup from "$lib/components/tournament/Matchup.svelte";

	const playerCount: number = 2 << 2;
</script>

<div class="bracket d-flex flex-row justify-content-center h-100">
	{#if playerCount >= 8}
		<div class="round quarter d-flex flex-column justify-content-between">
			{#each Array(4) as i}
				<div class="matchup flex-grow-1 d-flex align-items-center py-2">
					<Matchup />
				</div>
			{/each}
		</div>
		<div class="quarter connectors d-flex flex-column">
			{#each Array(4) as i}
				<div class="connector flex-grow-1 position-relative" />
			{/each}
		</div>
	{/if}

	{#if playerCount >= 4}
		<div class="round semi d-flex flex-column justify-content-between">
			{#each Array(2) as i}
				<div class="matchup flex-grow-1 d-flex align-items-center py-2">
					<Matchup />
				</div>
			{/each}
		</div>
		<div class="semi connectors d-flex flex-column">
			{#each Array(2) as i}
				<div class="connector flex-grow-1 position-relative" />
			{/each}
		</div>
	{/if}

	<div class="round final d-flex flex-column justify-content-between">
		<div class="matchup flex-grow-1 d-flex align-items-center py-2">
			<Matchup />
		</div>
	</div>
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
