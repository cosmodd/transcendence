<script lang="ts">
	import { faEye, faRightToBracket, faUserGroup } from "@fortawesome/free-solid-svg-icons";
    import { authedFetch } from "$lib/stores/auth";
	import Fa from "svelte-fa";
    import toasts from "$lib/stores/toasts";
    import { goto } from "$app/navigation";

	export let tournament: Tournament;

	export let hasUser: boolean;
	export let isUserInTournament: boolean;

	async function joinTournament(id: number) {
		const response = await authedFetch("/api/tournament/join/", {
			method: "POST",
			body: JSON.stringify({
				id: id,
			}),
		});

		if (!response.ok) {
			const error = await response.json();
			toasts.add({
				type: "error",
				description: error.error,
				duration: 5000,
			});
			return;
		}

		toasts.add({
			type: "success",
			description: "Joined tournament"
		});

		goto(`/tournament/${id}`);
	}
</script>

<div class="card p-4 d-inline-flex flex-column gap-1 border-2">
	<h4 class="m-0 fw-bold">{tournament.name ?? `Tournament ${tournament.id}`}</h4>
	<div class="d-flex flex-row align-items-center gap-2 mb-2 text-muted">
		<Fa icon={faUserGroup} />
		<span>{tournament.players_count} / {tournament.size} players</span>
	</div>
	<div class="buttons d-flex flex-row gap-2">
		{#if !hasUser}
			<button on:click={() => joinTournament(tournament.id)} class="btn btn-primary flex-fill" disabled={isUserInTournament}>
				<Fa icon={faRightToBracket} />
				<span class="ms-1 fw-bold">Join</span>
			</button>
		{:else}
			<a href="/tournament/{tournament.id}" class="btn btn-primary flex-fill">
				<Fa icon={faEye} />
				<span class="ms-1 fw-bold">View</span>
			</a>
		{/if}
	</div>
</div>