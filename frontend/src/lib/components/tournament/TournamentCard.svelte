<script lang="ts">
	import { faEye, faRightToBracket, faUserGroup } from "@fortawesome/free-solid-svg-icons";
    import { createEventDispatcher } from "svelte";
	import Fa from "svelte-fa";

	export let tournament: Tournament;
	export let hasUser: boolean;
	export let isUserInTournament: boolean;

	const dispatch = createEventDispatcher();
</script>

<div class="card p-4 d-inline-flex flex-column gap-1 border-2">
	<h4 class="m-0 fw-bold">{tournament.name ?? `Tournament ${tournament.id}`}</h4>
	<div class="d-flex flex-row align-items-center gap-2 mb-2 text-muted">
		<Fa icon={faUserGroup} />
		<span>{tournament.players_count} / {tournament.size} players</span>
	</div>
	<div class="buttons d-flex flex-row gap-2">
		{#if !hasUser}
			<button on:click={() => dispatch('join', tournament.id)} class="btn btn-primary flex-fill" disabled={isUserInTournament}>
				<Fa icon={faRightToBracket} />
				<span class="ms-1 fw-bold">Join</span>
			</button>
		{:else}
			<a href="/tournament/{tournament.id}" class="btn btn-primary flex-fill">
				<Fa icon={faEye} />
				<span class="ms-1 fw-bold">View</span>
			</a>
		{/if}
	</div>
</div>