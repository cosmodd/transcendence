<script lang="ts">
	import Fa from "svelte-fa";
	import { faSquareCheck, faSquareXmark } from "@fortawesome/free-solid-svg-icons";

	let focused = false;
	let username = "";

	const requirements = [
		{
			matches: (value: string): boolean => /^[a-z0-9._]+$/.test(value),
			message: "Contain only lowercase letters, numbers, dots or underscores",
		},
		{
			matches: (value: string): boolean => value.length >= 2 && value.length <= 32,
			message: "Be between 2 and 32 characters",
		},
		{
			matches: (value: string): boolean => !/^[\._]|[\._]$/g.test(value),
			message: "Do not start or end with a dot or underscore",
		},
		{
			matches: (value: string): boolean => !/\.{2}|_{2}/g.test(value),
			message: "Do not use double dots or double underscores",
		},
	];

	function customValidity(event: Event) {
		const input = event.target as HTMLInputElement;
		input.setCustomValidity("");

		for (const requirement of requirements) {
			if (requirement.matches(username)) continue;
			input.setCustomValidity(requirement.message);
		}
	}
</script>

<div id="usernameField">
	<label for="username" class="visually-hidden">Username</label>
	<input
		type="text"
		class="form-control"
		name="username"
		id="username"
		placeholder="Username"
		minlength="2"
		maxlength="32"
		pattern="^[a-z0-9._]+$"
		required
		on:focus={() => (focused = true)}
		on:blur={() => (focused = false)}
		bind:value={username}
		on:input={customValidity}
	/>
	<div id="usernameHelpBlock" class="form-text">
		{#each requirements as requirement}
			<!-- {#if focused || !requirement.matches(username)} -->
			<div
				class="requirement d-flex flex-row align-items-center gap-1"
				class:valid={requirement.matches(username)}
			>
				{#if requirement.matches(username)}
					<Fa icon={faSquareCheck} class="text-success" />
				{:else}
					<Fa icon={faSquareXmark} class="text-danger" />
				{/if}
				<span>{requirement.message}</span>
			</div>
			<!-- {/if} -->
		{/each}
	</div>
</div>

<style>
	/* When the requirement is valid, make it disappear with a transition */
	.requirement.valid {
		animation: validRequirement 0.5s ease-in-out 1;
		height: 0;
		opacity: 0;
	}

	@keyframes validRequirement {
		0% {
			opacity: 1;
			height: 100%;
		}

		75% {
			opacity: 1;
			height: 100%;
		}

		100% {
			opacity: 0;
			height: 0;
		}
	}
</style>