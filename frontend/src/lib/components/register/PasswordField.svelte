<script lang="ts">
	import Fa from "svelte-fa";
	import { faSquareCheck, faSquareXmark } from "@fortawesome/free-solid-svg-icons";

	let focused = false;
	let password = "";
	let confirmPassword = "";

	const requirements = [
		{
			matches: (value: string): boolean => value.length >= 8,
			message: "Be at least 8 characters long",
		},
		{
			matches: (value: string): boolean => /[A-Z]/g.test(value),
			message: "Contain at least one uppercase letter",
		},
		{
			matches: (value: string): boolean => /[a-z]/g.test(value),
			message: "Contain at least one lowercase letter",
		},
		{
			matches: (value: string): boolean => /[0-9]/g.test(value),
			message: "Contain at least one number",
		},
		{
			matches: (value: string): boolean => /[^A-Za-z0-9]/g.test(value),
			message: "Contain at least one special character",
		},
	];

	function passwordCustomValidity(event: Event) {
		const input = event.target as HTMLInputElement;
		input.setCustomValidity("");

		for (const requirement of requirements) {
			if (requirement.matches(password)) continue;
			input.setCustomValidity(requirement.message);
		}
	}

	function confirmCustomValidity(event: Event) {
		const input = event.target as HTMLInputElement;
		input.setCustomValidity("");

		if (password !== confirmPassword) input.setCustomValidity("Passwords do not match");
	}
</script>

<div id="passwordField">
	<label for="password" class="visually-hidden">Password</label>
	<input
		type="password"
		id="password"
		name="password"
		class="form-control"
		placeholder="Password"
		aria-labelledby="passwordHelpBlock"
		minlength="8"
		required
		on:focus={() => (focused = true)}
		on:blur={() => (focused = false)}
		bind:value={password}
		on:input={passwordCustomValidity}
	/>
	<div id="passwordHelpBlock" class="form-text">
		{#each requirements as requirement}
			<!-- {#if focused || !requirement.matches(username)} -->
			<div class="requirement d-flex flex-row align-items-center gap-1">
				{#if requirement.matches(password)}
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

<div id="confirmPasswordField">
	<label for="confirmPassword" class="visually-hidden">Confirm Password</label>
	<input
		type="password"
		id="confirmPassword"
		name="confirmPassword"
		class="form-control"
		placeholder="Confirm Password"
		aria-labelledby="passwordHelpBlock"
		minlength="8"
		required
		bind:value={confirmPassword}
		on:input={confirmCustomValidity}
	/>
</div>
