<script lang="ts">
	import { createEventDispatcher } from "svelte";

	export let username: string;
	export let selected: string;

	const dispatcher = createEventDispatcher();

	function handleClick() {
		selected = username;
		dispatcher("select", username);
	}
</script>

<a
	class="d-flex flex-row gap-3 align-items-center py-2 px-3 text-decoration-none text-reset"
	class:active={selected === username}
	on:click|preventDefault={handleClick}
	href=""
>
	<img
		class="rounded-circle bg-primary"
		src="https://via.placeholder.com/128"
		style="width: 32px; height: 32px;"
		alt=""
	/>
	<div class="d-flex flex-column flex-grow-1" style="min-width: 0;">
		<div class="fw-bold">{username}</div>
		<div class="text-muted text-truncate">
			{[
				"Hey Sarah, on my way home now! Should be there in 30 minutes. Can you grab some milk on the way?",
				"Hey David, up for grabbing drinks after work tonight? :)",
				"Don't forget! Movie night at my place tonight at 8pm!",
				"Hi Emma, you're invited to my birthday party on Saturday night! Details to follow.",
				"Hi Michael, this is a reminder of your dental cleaning appointment tomorrow at 2pm.",
			][Math.floor(Math.random() * 5)]}
		</div>
	</div>
</a>

<style>
	.active {
		background-color: rgba(var(--bs-body-color-rgb), 0.1);
	}

	a {
		transition: background-color 0.1s ease-in-out;
	}

	a:hover {
		background-color: rgba(var(--bs-body-color-rgb), 0.05);
	}
</style>
