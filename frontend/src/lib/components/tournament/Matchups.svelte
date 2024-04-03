<script lang="ts">
	import Matchup from "./Matchup.svelte";

	// TODO: Get matches information form parent
</script>

<div class="matchups d-flex flex-row">
	<div class="matches d-flex flex-column">
		<Matchup />
		<Matchup />
	</div>
	<div class="connector d-flex flex-column gap-3">
		<div class="merger flex-grow-1 position-relative border"></div>
		<div class="merger flex-grow-1 position-relative border"></div>
	</div>
</div>

<style>
	.connector {
		min-width: 100px;
	}

	.merger {
		border: none !important;
	}

	.merger::before {
		content: "";
		display: block;
		width: 50%;
		height: 100%;
		position: absolute;
		top: -50%;
		left: 0;
		border-bottom: 2px solid var(--bs-border-color);
		border-right: 2px solid var(--bs-border-color);
		border-radius: 0 0 0.375rem 0;
	}

	.merger:first-child::before {
		border: none;
		border-top: 2px solid var(--bs-border-color);
		border-right: 2px solid var(--bs-border-color);
		top: 50%;
		border-radius: 0 0.375rem 0 0;
	}
</style>
