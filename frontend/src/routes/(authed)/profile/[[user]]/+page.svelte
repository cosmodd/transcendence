<script lang="ts">
	import { user } from "$lib/stores/user";
	import MatchSummary from "$lib/components/profile/MatchSummary.svelte";
	import {
		faBan,
		faFaceFrown,
		faGamepad,
		faMessage,
		faStar,
		faTrophy,
		faUserPlus,
	} from "@fortawesome/free-solid-svg-icons";
	import Fa from "svelte-fa";

	let userStatistics: any = {};

	userStatistics.gamesPlayed = 100;
	userStatistics.gamesWon = Math.floor(Math.random() * 100);
	userStatistics.gamesLost = userStatistics.gamesPlayed - userStatistics.gamesWon;
	userStatistics.winRate = userStatistics.gamesWon / userStatistics.gamesPlayed;

	const games = Array.from({ length: 30 }, (_, i) => {
		const firstScore = Math.floor(Math.random() * 100);
		const secondScore = 100 - firstScore;

		const date = new Date();
		date.setDate(date.getDate() - i);

		return {
			scores: [
				{ username: $user.display_name, score: firstScore },
				{ username: "random", score: secondScore },
			],
			date: date.toISOString(),
		};
	});
</script>

<div class="row h-100 m-0 gap-3">
	<div class="col-3 card border-2 p-4 gap-3">
		<div class="d-flex flex-column align-items-center">
			<img src={$user.profile_image} class="rounded-circle" style="width: 100px; height: 100px;" alt="Avatar" />
			<h3 class="m-0 mt-2 fw-bold">{$user.display_name}</h3>
			<p class="m-0 text-muted">@{$user.username}</p>
			<p class="m-0 text-muted">
				<span class="rounded-circle bg-success p-1"></span>
				Offline
			</p>
		</div>
		<hr class="m-0" />
		<div class="d-flex flex-column gap-2">
			<h5>Statistics</h5>
			<div class="d-flex justify-content-between">
				<div class="col d-flex gap-2 align-items-center">
					<Fa icon={faGamepad} />
					<p class="m-0">Games Played</p>
				</div>
				<p class="m-0">{userStatistics.gamesPlayed}</p>
			</div>
			<div class="d-flex justify-content-between">
				<div class="col d-flex gap-2 align-items-center">
					<Fa icon={faTrophy} />
					<p class="m-0">Wins</p>
				</div>
				<p class="m-0">{userStatistics.gamesWon}</p>
			</div>
			<div class="d-flex justify-content-between">
				<div class="col d-flex gap-2 align-items-center">
					<Fa icon={faFaceFrown} />
					<p class="m-0">Losses</p>
				</div>
				<p class="m-0">{userStatistics.gamesLost}</p>
			</div>
			<div class="d-flex justify-content-between">
				<div class="col d-flex gap-2 align-items-center">
					<Fa icon={faStar} />
					<p class="m-0">Win Rate</p>
				</div>
				<p class="m-0">{Math.floor(userStatistics.winRate * 100)}%</p>
			</div>
		</div>
		<div class="buttons d-flex flex-column gap-2 align-items-center mt-auto">
			<button class="btn btn-success w-100"><Fa icon={faUserPlus} class="me-1" /> Add friend</button>
			<button class="btn btn-primary w-100"><Fa icon={faMessage} class="me-1" /> Message</button>
			<button class="btn btn-danger w-100"><Fa icon={faBan} class="me-1" /> Block</button>
		</div>
	</div>
	<div class="col card border-2 h-100 p-0">
		<h1 class="h3 fw-bold p-3 m-0">Games</h1>
		<div class="container-fluid overflow-y-scroll d-flex flex-column gap-1">
			{#each games as game}
				<MatchSummary scores={game.scores} date={new Date(game.date)} />
			{/each}
		</div>
	</div>
</div>
