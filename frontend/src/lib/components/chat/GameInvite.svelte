<script lang="ts">
	import { faGamepad, faRightToBracket, faTrophy } from "@fortawesome/free-solid-svg-icons";
  	import { onDestroy } from "svelte";
	import Fa from "svelte-fa";
	import { sendInvitation } from "$lib/stores/websocket";

	export let game_type: "casual" | "tournament" = "casual";
	export let self: boolean = false;
	export let invitation_date: string;
	export let is_accepted: boolean = false;
	export let room_name: string = "";
	
	let is_expired: boolean = false;
	let clear_timeout: NodeJS.Timeout | null = null;

	// set timeout of 5 minutes to expire the invitation if not accepted
	const expiration_date = new Date(invitation_date);
	expiration_date.setMinutes(expiration_date.getMinutes() + 1);
	const now = new Date();
	console.log("expiration date", expiration_date);
	console.log("now", now);
	if (now > expiration_date) {
		is_expired = true;
	}
	else{
		clear_timeout = setTimeout(() => {
			is_expired = true;
		}, expiration_date.getTime() - now.getTime());
	}

	onDestroy(() => {
		if (clear_timeout) {
			clearTimeout(clear_timeout);
		}
	});

	$: icon = game_type === "casual" ? faGamepad : faTrophy;
</script>

<div class="d-flex flex-row {self ? 'justify-content-end' : ''} align-items-center">
	<div
		class="p-3 d-flex flex-row align-items-center gap-3 bg-{is_expired === false
			? 'success'
			: 'secondary'} bg-gradient rounded"
	>
		<div class="d-flex flex-column">
			<div class="fw-bold d-flex gap-2 align-items-center">
				<Fa {icon} />
				{game_type === "casual" ? "Game" : "Tournament"} invite
			</div>
			<div class="text-muted">
				{#if !is_expired && !is_accepted}
					{self ? "You've sent an invite to a game" : `You've been invited to a ${game_type === "casual" ? "game" : "tournament"}` }
				{:else if is_accepted}
					{self ? "Your invitation has been accepted" : "The invitation has been accepted"}
				{:else}
					{self ? "Your invitation has expired" : "The invitation has expired" }
				{/if}
			</div>
		</div>
		<!-- Join button to redirect to game page -->
		{#if !self && !is_expired && !is_accepted}
			<button
				class="btn btn-primary"
				on:click={() => {
					// on click update the invitation status to accepted
					is_accepted = true;
					sendInvitation("accepted", room_name);
				}}
			>
				Confirm
			</button>
		{/if}
	</div>
</div>
