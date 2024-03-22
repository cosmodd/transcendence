<script lang="ts">
	import { faTrophy, faUserGroup } from "@fortawesome/free-solid-svg-icons";
	import Fa from "svelte-fa";

	export let scores: { username: string; score: number }[];
	export let date: Date;
	export let type: "casual" | "tournament";

	$: hasWon = scores[0].score > scores[1].score;
	$: resultColor = hasWon ? "success" : "danger";
	$: dateString = date.toLocaleDateString("en-US");
	$: formattedType = type === "casual" ? "Casual" : "Tournament";
</script>

<div class="d-flex justify-content-between align-items-center p-3 border-start border-3 border-{resultColor}">
	<div class="start row gap-2 w-100">
		<div class="gameType d-flex gap-2 align-items-center col-4">
			<Fa icon={type === "tournament" ? faTrophy : faUserGroup} />
			<span class="fw-bold">{formattedType}</span>
		</div>
		{#if type === "casual"}
			<div class="d-flex gap-2 align-items-center col">
				<span class="badge rounded-pill bg-{resultColor}">{hasWon ? "Won" : "Lost"}</span>
				<div class="score d-flex gap-2 fw-bold" style="font-variant-numeric: tabular-nums">
					<span class="text-{resultColor}">
						{scores[0].score.toString().padStart(2, "0")}
					</span>
					<span class="text-muted">vs</span>
					<span class="text-{!hasWon ? 'success' : 'danger'}">
						{scores[1].score.toString().padStart(2, "0")}
					</span>
					<span>{scores[1].username}</span>
				</div>
			</div>
		{:else}
			<div class="d-flex gap-2 align-items-center col">
				<span class="badge rounded-pill bg-{resultColor}">{hasWon ? "Won" : ["Quarter", "Semi", "Final"][Math.floor(Math.random() * 3)]}</span>
				<div class="score d-flex gap-2 fw-bold" style="font-variant-numeric: tabular-nums">
					<span class="text-{resultColor}">
						{scores[0].score.toString().padStart(2, "0")}
					</span>
					<span class="text-muted">vs</span>
					<span class="text-{!hasWon ? 'success' : 'danger'}">
						{scores[1].score.toString().padStart(2, "0")}
					</span>
					<span>{scores[1].username}</span>
				</div>
			</div>
		{/if}
	</div>
	<div class="end row gap-2 w-100 justify-content-end">
		<p class="text-muted m-0 text-end">{dateString}</p>
	</div>
</div>

<style>
	.border-success {
		background: linear-gradient(90deg, rgba(var(--bs-success-rgb), 0.2) 0%, transparent);
	}
</style>
