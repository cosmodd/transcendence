<script lang="ts">
    import Avatar from "../Avatar.svelte";


	export let game: TournamentGame | null = null;

	
	const players: any[] = game?.players ?? [];
	const firstPlayerWon = game?.winner === players[0]?.username;
	const scores: number[] = game?.scores.slice().sort((a, b) => firstPlayerWon ? b - a : a - b) ?? [];

</script>

{#if game != null}
	<div class="card d-flex flex-column border-2 overflow-hidden my-3">
		<a class="player p-2 d-flex flex-row gap-2 align-items-center text-decoration-none text-reset user-link {players[0] == null ? 'disabled' : ''}" href="/profile/{players[0].username}">
			<Avatar src={players[0]?.profile_image ?? "/static/images/default_profile_image.jpg"} size={24} />
			<span class="displayname fw-bold me-1">{players[0]?.username ?? "TBD"}</span>
			{#if game.status == "over"}
			<span class="score badge bg-{firstPlayerWon ? 'success' : 'danger'} ms-auto">{scores[0] ?? "N/A"}</span>
			{:else if game.status == "cancelled"}
			<span class="score badge bg-danger ms-auto">CNCLD</span>
			{:else}
			<span class="score badge bg-secondary ms-auto">N/A</span>
			{/if}
		</a>
		<hr class="m-0 border-2" />
		<a class="player p-2 d-flex flex-row gap-2 align-items-center text-decoration-none text-reset user-link {players[1] == null ? 'disabled' : ''}" href="/profile/{players[1].username}">
			<Avatar src={players[1]?.profile_image ?? "/static/images/default_profile_image.jpg"} size={24} />
			<span class="text-truncate fw-bold me-1">{players[1]?.username ?? "TBD"}</span>
			{#if game.status == "over"}
				<span class="score badge bg-{!firstPlayerWon ? 'success' : 'danger'} ms-auto">{scores[1] ?? "N/A"}</span>
			{:else if game.status == "cancelled"}
				<span class="score badge bg-danger ms-auto">CNCLD</span>
			{:else}
				<span class="score badge bg-secondary ms-auto">N/A</span>
			{/if}
		</a>
	</div>
{:else}
	<div class="card d-flex flex-column border-2 overflow-hidden my-3">
		<a class="player p-2 d-flex flex-row gap-2 align-items-center text-decoration-none text-reset user-link disabled" href="#">
			<Avatar src="/static/images/default_profile_image.jpg" size={24} />
			<span class="displayname fw-bold me-1">TBD</span>
			<span class="score badge bg-secondary ms-auto">N/A</span>
		</a>
		<hr class="m-0 border-2" />
		<a class="player p-2 d-flex flex-row gap-2 align-items-center text-decoration-none text-reset user-link disabled" href="#">
			<Avatar src="/static/images/default_profile_image.jpg" size={24} />
			<span class="text-truncate fw-bold me-1">TBD</span>
			<span class="score badge bg-secondary ms-auto">N/A</span>
		</a>
	</div>
{/if}

<style>
	.card {
		width: 250px;
	}

	a.disabled {
		pointer-events: none;
		cursor: default;
	}

	.user-link {
		transition: background 0.1s ease-in-out;
	}

	.user-link:not(.disabled):hover {
		background: rgba(255, 255, 255, 0.1);
	}
</style>
