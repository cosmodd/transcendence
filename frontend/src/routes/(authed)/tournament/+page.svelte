<script lang="ts">
	import { goto } from "$app/navigation";
	import TournamentCard from "$lib/components/tournament/TournamentCard.svelte";
	import { authedFetch } from "$lib/stores/auth";
	import toasts from "$lib/stores/toasts";
	import { user } from "$lib/stores/user";
	import { faPlus, faTriangleExclamation, faTrophy, faWarning } from "@fortawesome/free-solid-svg-icons";
	import { onMount } from "svelte";
	import Fa from "svelte-fa";

	let tournaments: Tournament[] = [];
	let creationAlert: string = "";
	let joinAlert: string = "";

	let id: number = -1;

	let joinModalElement: HTMLElement;

	$: isUserInTournament = tournaments.some((tournament) => tournament.players.includes($user.username));

	async function loadTournaments() {
		const response = await authedFetch("/api/tournament/");
		const data = await response.json();

		if (!data) return;

		tournaments = data.sort(
			(a: Tournament, b: Tournament) => b.players.includes($user.username) - a.players.includes($user.username),
		);
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

		goto(`/tournament/${json.id}`);

		const modalInstance = bootstrap.Modal.getInstance(document.getElementById("tournamentModal"));
		if (modalInstance) modalInstance.hide();
	}

	function openJoinModal(tournamentId: number) {
		const modalInstance = bootstrap.Modal.getOrCreateInstance(joinModalElement);
		if (modalInstance) modalInstance.show();
		id = tournamentId;
	}

	async function joinTournament(event: SubmitEvent) {
		const target = event.target as HTMLFormElement;
		const data = new FormData(target);

		const response = await authedFetch("/api/tournament/join/", {
			method: "POST",
			body: JSON.stringify({
				id: id,
				display_name: data.get("display_name"),
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
			description: "Joined tournament",
		});

		const modalInstance = bootstrap.Modal.getOrCreateInstance(joinModalElement);
		if (modalInstance) modalInstance.hide();

		goto(`/tournament/${id}`);
	}

	onMount(async () => {
		await loadTournaments();
	});
</script>

<div class="container h-100 d-flex flex-column">
	<div class="header d-flex flex-row justify-content-between align-items-center">
		<h3 class="fw-bold mb-3">
			<Fa icon={faTrophy} class="me-1" />
			Tournaments
		</h3>
		<div class="buttons d-flex flex-row">
			<button
				class="btn btn-primary px-3"
				data-bs-toggle="modal"
				data-bs-target="#tournamentModal"
				disabled={isUserInTournament}
			>
				<Fa icon={faPlus} class="me-1" />
				Create Tournament
			</button>
		</div>
	</div>

	{#if tournaments.length === 0}
		<div class="d-flex justify-content-center align-items-center h-100">
			<h3 class="text-muted">No tournaments available</h3>
		</div>
	{:else}
		<div class="tournaments h-100 overflow-y-auto gap-3">
			{#each tournaments as tournament}
				<TournamentCard
					{tournament}
					hasUser={tournament.players.includes($user.username)}
					{isUserInTournament}
					on:join={() => openJoinModal(tournament.id)}
				/>
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
						<input
							type="text"
							class="form-control"
							id="name"
							name="name"
							placeholder="Tournament Name"
							required
						/>
					</div>
					<div class="mb-3 btn-group w-100 border border-1">
						<input type="radio" name="size" value="4" class="btn-check" id="four" checked />
						<label class="btn btn-dark" for="four">4 Players</label>

						<input type="radio" name="size" value="8" class="btn-check" id="eight" />
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

<div
	class="modal fade"
	bind:this={joinModalElement}
	id="joinModal"
	tabindex="-1"
	aria-labelledby="joinModalLabel"
	aria-hidden="true"
>
	<div class="modal-dialog modal-dialog-centered">
		<div class="modal-content">
			<div class="modal-header">
				<h5 class="modal-title" id="joinModalLabel">Join Tournament</h5>
				<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" />
			</div>

			<div class="modal-body p-4 d-flex flex-column gap-3">
				{#if joinAlert}
					<div class="alert alert-danger m-0" role="alert">
						<Fa icon={faTriangleExclamation} />
						{joinAlert}
					</div>
				{/if}
				<form action="#" on:submit|preventDefault={joinTournament}>
					<div class="mb-3 d-flex flex-column">
						<label for="name" class="form-label visually-hidden">Unique display name</label>
						<input
							type="text"
							class="form-control"
							id="display_name"
							name="display_name"
							placeholder="Unique display name"
							value={$user.display_name}
							required
						/>
						<span class="text-muted m-2">
							<Fa icon={faWarning} />
							This will change your display name globally
						</span>
					</div>
					<button
						type="submit"
						class="btn btn-primary d-flex flex-row gap-2 align-items-center fw-bold w-100 justify-content-center"
					>
						Join
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
