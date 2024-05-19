<script lang="ts">
	import { createEventDispatcher } from "svelte";
	import type { Conversation } from "$lib/stores/websocket";

	export let conversation: Conversation;
	export let selected: boolean;

	const dispatcher = createEventDispatcher();

	function handleClick() {
		// selected = username;
		dispatcher("select", conversation.chatting_with);
	}
</script>

<button
	class="d-flex flex-row gap-3 align-items-center py-2 px-3 text-decoration-none text-reset"
	class:active={selected}
	on:click|preventDefault={handleClick}
>
	<img
		class="rounded-circle bg-primary"
		src="https://via.placeholder.com/128"
		style="width: 32px; height: 32px;"
		alt=""
	/>
	<div class="d-flex flex-column flex-grow-1" style="min-width: 0;">
		<div class="fw-bold">{conversation.chatting_with}</div>
		<div class="text-muted text-truncate">
			{conversation.last_message ?? "No message yet"}
		</div>
	</div>
</button>

<style>
	.active {
		background-color: rgba(var(--bs-body-color-rgb), 0.1);
	}

	button {
		transition: background-color 0.1s ease-in-out;
		border: none;
		outline: none;
		background: unset;
		border-radius: none;
	}

	button:hover {
		background-color: rgba(var(--bs-body-color-rgb), 0.05);
	}
</style>
