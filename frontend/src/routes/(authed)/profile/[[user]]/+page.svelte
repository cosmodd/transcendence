<script lang="ts">
	import { page } from "$app/stores";
	import MatchSummary from "$lib/components/profile/GameSummary.svelte";
	import { authedFetch } from "$lib/stores/auth";
	import { user } from "$lib/stores/user";
	import {
		faBan,
		faFaceFrown,
		faGamepad,
		faMessage,
		faStar,
		faTrophy,
		faUserPlus,
	} from "@fortawesome/free-solid-svg-icons";
	import { onDestroy, onMount } from "svelte";
	import Fa from "svelte-fa";

	let userData: any = null;
	let games: any[] = [];

	$: queriedUsername = $page.params.user;
	$: self = queriedUsername == null || $user.username == queriedUsername;


	async function loadUser() {
		if (self) {
			userData = $user;
			return;
		}

		const response = await authedFetch(`/api/user/${queriedUsername}/`);

		if (!response.ok) {
			userData = null;
			return;
		}

		userData = await response.json();
	}

	function loadGames() {
		if (userData == null) return;

		const username = userData.username;

		authedFetch(`/api/pong/${username}/`).then(async (response) => {
			if (!response.ok) return;
			games = (await response.json())?.games ?? [];
		});
	}

	$: {
		queriedUsername;
		loadUser().then(() => loadGames());
	}
</script>

{#if userData == null}
	<div class="d-flex flex-column justify-content-center align-items-center h-100 gap-2">
		<div class="d-flex align-items-center gap-3">
			<h2>User not found</h2>
			<Fa icon={faFaceFrown} size="2x" />
		</div>
		<a href="/"><button class="btn btn-primary">Go back</button></a>
	</div>
{:else}
	<div class="row h-100 m-0 gap-3">
		<div class="col-3 card border-2 p-4 gap-3">
			<div class="d-flex flex-column align-items-center">
				<img
					src={userData.profile_image}
					class="rounded-circle"
					style="width: 100px; height: 100px;"
					alt="Avatar"
				/>
				<h3 class="m-0 mt-2 fw-bold">{userData.display_name}</h3>
				<p class="m-0 text-muted">@{userData.username}</p>
				<span class="mt-2 badge rounded-pill bg-secondary">Offline</span>
			</div>
			<hr class="m-0" />
			<div class="d-flex flex-column gap-2">
				<h5>Statistics</h5>
				<div class="d-flex justify-content-between">
					<div class="col d-flex gap-2 align-items-center">
						<Fa icon={faGamepad} />
						<p class="m-0">Games Played</p>
					</div>
					<p class="m-0">{games.length}</p>
				</div>
				<div class="d-flex justify-content-between">
					<div class="col d-flex gap-2 align-items-center">
						<Fa icon={faTrophy} />
						<p class="m-0">Wins</p>
					</div>
					<p class="m-0">{games.filter((game) => game.winner == userData.username).length}</p>
				</div>
				<div class="d-flex justify-content-between">
					<div class="col d-flex gap-2 align-items-center">
						<Fa icon={faFaceFrown} />
						<p class="m-0">Losses</p>
					</div>
					<p class="m-0">{games.filter((game) => game.winner != userData.username).length}</p>
				</div>
				<div class="d-flex justify-content-between">
					<div class="col d-flex gap-2 align-items-center">
						<Fa icon={faStar} />
						<p class="m-0">Win Rate</p>
					</div>
					<p class="m-0">
						{((games.filter((game) => game.winner == userData.username).length / games.length) * 100).toFixed(
							2,
						)}%
					</p>
				</div>
			</div>
			{#if !self}
				<div class="buttons d-flex flex-column gap-2 align-items-center mt-auto">
					<button class="btn btn-success w-100"><Fa icon={faUserPlus} class="me-1" />Add friend</button>
					<button class="btn btn-primary w-100"><Fa icon={faMessage} class="me-1" />Message</button>
					<button class="btn btn-danger w-100"><Fa icon={faBan} class="me-1" />Block</button>
				</div>
			{/if}
		</div>
		<div class="col card border-2 h-100 p-3">
			{#if games.length == 0}
				<div class="d-flex justify-content-center align-items-center h-100">
					<h3 class="text-muted">No games played</h3>
				</div>
			{:else}
				<h3 class="fw-bold mb-3">Games History</h3>
				<div class="container-fluid overflow-y-scroll d-flex flex-column gap-1 p-0">
					{#each games.reverse() as game}
						<MatchSummary {game} user={userData} />
					{/each}
				</div>
			{/if}
		</div>
	</div>
{/if}