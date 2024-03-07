<script lang="ts">
	export let scores: { username: string; score: number }[];
	export let date: Date;

	$: hasWon = scores[0].score > scores[1].score;
	$: dateString = date.toLocaleDateString("en-US");
</script>

<div class="d-flex justify-content-between align-items-center p-3 border-start border-3 border-{hasWon ? 'success' : 'danger'}">
	<div class="scores d-flex flex-row gap-2">
		<p class="text-muted m-0">{scores[0].username}</p>
		<p class="{hasWon ? 'text-success' : 'text-danger'} fw-bold m-0">{scores[0].score}</p>
		:
		<p class="{!hasWon ? 'text-success' : 'text-danger'} fw-bold m-0">{scores[1].score}</p>
		<p class="text-muted m-0">{scores[1].username}</p>
	</div>
	<p class="m-0 text-muted">{dateString}</p>
</div>

<style>
	.border-success {
		background: linear-gradient(90deg, rgba(var(--bs-success-rgb), .2) 0%, transparent 10%);
	}
</style>