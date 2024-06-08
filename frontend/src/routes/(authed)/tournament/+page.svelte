<script lang="ts">
	import TournamentCard from "$lib/components/tournament/TournamentCard.svelte";
    import { authedFetch } from "$lib/stores/auth";
    import { faPlus, faTriangleExclamation } from "@fortawesome/free-solid-svg-icons";
    import { onMount } from "svelte";
    import Fa from "svelte-fa";

	interface Tournament {
		name: string;
		id: number;
		status: string;
		players_count: number;
		size: "eight" | "four";
	};

	let tournaments: Tournament[] = [];
	let creationAlert: string = "";

	async function loadTournaments() {
		const response = await authedFetch("/api/tournament/");
		tournaments = await response.json();
	}

	async function createTournament(event: SubmitEvent) {
		const target = event.target as HTMLFormElement;
		const data = new FormData(target);

		const response = await authedFetch("/api/tournament/create/", {
			method: "POST",
			body: JSON.stringify({
				name: data.get("name"),
				size: data.get("size"),
			}),
		});

		const json = await response.json();

		if (!response.ok) {
			creationAlert = json.error;
			return;
		}

		await loadTournaments();

		const modalInstance = bootstrap.Modal.getInstance(document.getElementById("tournamentModal"));
		if (modalInstance) modalInstance.hide();
	}

	onMount(async () => {
		await loadTournaments();
	});
</script>

<div class="container h-100 d-flex flex-column">
	<div class="header d-flex flex-row justify-content-between align-items-center">
		<h1 class="fw-bold mb-3">Tournaments</h1>
		<div class="buttons d-flex flex-row">
			<button class="btn btn-primary px-3" data-bs-toggle="modal" data-bs-target="#tournamentModal">
				<Fa icon={faPlus} class="me-1" />
				Create Tournament
			</button>
		</div>
	</div>
	
		{#if tournaments.length == 0}
			<div class="d-flex justify-content-center align-items-center h-100">
				<h3 class="text-muted">No tournaments available</h3>
			</div>
		{:else}
			<div class="tournaments h-100 overflow-y-auto gap-3">
				{#each tournaments as tournament}
					<TournamentCard {tournament} />
				{/each}
			</div>
		{/if}
</div>

<!-- Tournament Modal -->
<div class="modal fade" id="tournamentModal" tabindex="-1" aria-labelledby="tournamentModalLabel" aria-hidden="true">
	<div class="modal-dialog modal-dialog-centered">
		<div class="modal-content">
			<div class="modal-header">
				<h5 class="modal-title" id="tournamentModalLabel">New Tournament</h5>
				<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" />
			</div>
			
			<div class="modal-body p-4 d-flex flex-column gap-3">
				{#if creationAlert}
					<div class="alert alert-danger m-0" role="alert">
						<Fa icon={faTriangleExclamation} />
						{creationAlert}
					</div>
				{/if}
				<form action="#" on:submit|preventDefault={createTournament}>
					<div class="mb-3">
						<label for="name" class="form-label visually-hidden">Name</label>
						<input type="text" class="form-control" id="name" name="name" placeholder="Tournament Name" required />
					</div>
					<div class="mb-3 btn-group w-100 border border-1">
						<input type="radio" name="size" value="four" class="btn-check" id="four" checked>
						<label class="btn btn-dark" for="four">4 Players</label>

						<input type="radio" name="size" value="eight" class="btn-check" id="eight">
						<label class="btn btn-dark" for="eight">8 Players</label>
					</div>
					<button
						type="submit"
						class="btn btn-primary d-flex flex-row gap-2 align-items-center fw-bold w-100 justify-content-center"
					>
						Create
					</button>
				</form>
			</div>
		</div>
	</div>
</div>

<style>
	.tournaments {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
		grid-auto-rows: min-content;
	}
</style>
