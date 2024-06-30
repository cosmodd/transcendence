<script lang="ts">
	import { faRightToBracket, faUserGroup } from "@fortawesome/free-solid-svg-icons";
    import { authedFetch } from "$lib/stores/auth";
	import Fa from "svelte-fa";

	export let tournament: {
		id: number;
		name: string;
		size: 4 | 8;
		status: string;
		players_count: number;
		players: string[];
	};

	async function joinTournament(id: number) {
		const response = await authedFetch("/api/tournament/join/", {
			method: "POST",
			body: JSON.stringify({
				id: id,
			}),
		});

		if (!response.ok) {
			const error = await response.json();
			console.log("Error! " + error.error)
			alert("Error! " + error.error)
			return;
		}
	}
</script>

<div class="card p-4 d-inline-flex flex-column gap-1 border-2">
	<h4 class="m-0 fw-bold">{tournament.name ?? `Tournament ${tournament.id}`}</h4>
	<div class="d-flex flex-row align-items-center gap-2 mb-2 text-muted">
		<Fa icon={faUserGroup} />
		<span>{tournament.players_count} / {tournament.size} players</span>
	</div>
	<button on:click={() => joinTournament(tournament.id)} class="btn btn-primary">
		<Fa icon={faRightToBracket} />
		<span class="ms-1 fw-bold">Join</span>
	</button>
</div>
