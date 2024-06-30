<script lang="ts">

	export let game: TournamentGame;

</script>

<div class="card d-flex flex-column border-2 overflow-hidden my-3">
	<div class="player p-2 d-flex flex-row gap-2 align-items-center">
		<img
			src="/static/images/default_profile_image.jpg"
			class="rounded-circle"
			alt="avatar"
			style="width: 24px; height: 24px;"
		/>
		<span class="displayname fw-bold me-1">TBD</span>
		<span class="score badge bg-success ms-auto">N/A</span>
	</div>
	<hr class="m-0 border-2" />
	<div class="player p-2 d-flex flex-row gap-2 align-items-center">
		<img
			src="/static/images/default_profile_image.jpg"
			class="rounded-circle"
			alt="avatar"
			style="width: 24px; height: 24px;"
		/>
		<span class="text-truncate fw-bold me-1">TBD</span>
		<span class="score badge bg-danger ms-auto">N/A</span>
	</div>
</div>

<style>
	.card {
		width: 250px;
	}
</style>
