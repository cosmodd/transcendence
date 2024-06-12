<script lang="ts">
	import { faTrophy, faUserGroup } from "@fortawesome/free-solid-svg-icons";
	import Fa from "svelte-fa";

	interface Game {
		type: "duel" | "tournament";
		winner: string;
		players: {
			username: string;
			display_name: string;
		}[];
		scores: number[];
		date_begin: string;
		status: "in_progress" | "over" | "cancelled";
		timeout: boolean;
		round: "none" | "quarter" | "semi" | "final";
	}

	export let game: Game;
	export let user: any;

	$: {
		if (game.players[1].username == user.username) {
			// console.log("reversing");
			game.players = game.players.reverse();
		}

		if ((game.winner === user.username && game.scores[0] < game.scores[1]) ||
                            (game.winner !== user.username && game.scores[0] > game.scores[1])) {
			game.scores = game.scores.reverse();
		}

	}
	$: hasWon = game.winner === user.username;
	$: resultColor = hasWon ? "success" : "danger";
	$: dateString = new Date(game.date_begin).toLocaleDateString("en-US");
	$: formattedType = game.type === "duel" ? "Duel" : "Tournament - " + game.round;
</script>

<div class="d-flex justify-content-between align-items-center p-3 border-start border-3 border-{resultColor}">
	<div class="start row gap-2 w-100">
		<div class="gameType d-flex gap-2 align-items-center col-4">
			<Fa icon={game.type === "tournament" ? faTrophy : faUserGroup} />
			<span class="fw-bold">{formattedType}</span>
		</div>
		<div class="d-flex gap-2 col align-items-center">
			<span class="badge rounded-pill bg-{resultColor}">{hasWon ? "Won" : "Lost"}</span>
			<div class="score d-flex gap-2 fw-bold align-items-center" style="font-variant-numeric: tabular-nums">
				<span class="text-{resultColor}">
					{game.scores[0].toString().padStart(2, "0")}
				</span>
				<span class="text-muted">vs</span>
				<span class="text-{!hasWon ? 'success' : 'danger'}">
					{game.scores[1].toString().padStart(2, "0")}
				</span>
				<a href={`/profile/${game.players[1].username}`} class="text-decoration-none text-body user-link py-1 px-2 rounded-3">
					{game.players[1].display_name}
				</a>
			</div>
		</div>
	</div>
	<div class="end row gap-2 w-100 justify-content-end">
		<p class="text-muted m-0 text-end">{dateString}</p>
	</div>
</div>

<style>
	.border-success {
		background: linear-gradient(90deg, rgba(var(--bs-success-rgb), 0.2) 0%, transparent);
	}

	.user-link {
		transition: background 0.1s ease-in-out;
	}

	.user-link:hover {
		background: rgba(255, 255, 255, 0.1);
	}
</style>
