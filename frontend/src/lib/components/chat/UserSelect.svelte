<script lang="ts">
	import { createEventDispatcher } from "svelte";
	import type { Conversation } from "$lib/stores/websocket";
	import Avatar from "../Avatar.svelte";

	export let conversation: Conversation;
	export let selected: boolean;

	const dispatcher = createEventDispatcher();

	function handleClick() {
		// selected = username;
		dispatcher("select", conversation.chatting_with);
	}
</script>

<button
	class="d-flex flex-row gap-3 align-items-center py-2 px-3 text-decoration-none text-reset text-start"
	class:active={selected}
	on:click|preventDefault={handleClick}
>
	<Avatar src={conversation.chatting_with.profile_image} size={32} />
	<div class="d-flex flex-column" style="min-width: 0;">
		<div class="fw-bold">{conversation.chatting_with.display_name}</div>
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
