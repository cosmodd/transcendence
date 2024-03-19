<script lang="ts">
	import Fa from "svelte-fa";
	import { faEye, faEyeSlash, faSquareCheck, faSquareXmark } from "@fortawesome/free-solid-svg-icons";
	import { onMount } from "svelte";

	interface PasswordField {
		type: "password" | "text";
		value: string;
		input: HTMLInputElement | null;
	}

	let focused: boolean = false;
	let passwordField: PasswordField = {
		type: "password",
		value: "",
		input: null,
	};
	let confirmField: PasswordField = {
		type: "password",
		value: "",
		input: null,
	};

	$: samePassword = passwordField.value === confirmField.value && confirmField.value.length > 0;

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

	onMount(() => {
		passwordField.input = document.querySelector("#passwordField input");
		confirmField.input = document.querySelector("#confirmPasswordField input");
	});

	// Function to update the state of "same password" requirement
	function updateSamePasswordRequirement() {
		const samePassword = passwordField.value === confirmField.value && confirmField.value.length > 0;
		if (!samePassword) {
			confirmField.input?.setCustomValidity("Passwords do not match");
			return;
		}
		confirmField.input?.setCustomValidity("");
	}

	function passwordCustomValidity(event: Event) {
		const input = event.target as HTMLInputElement;
		input.setCustomValidity("");

		for (const requirement of requirements) {
			if (requirement.matches(passwordField.value)) continue;
			input.setCustomValidity(requirement.message);
		}

		updateSamePasswordRequirement();
	}

	function confirmCustomValidity(event: Event) {
		const input = event.target as HTMLInputElement;
		input.setCustomValidity("");

		if (passwordField.value !== confirmField.value) input.setCustomValidity("Passwords do not match");
	}
</script>

<div id="passwordField">
	<label for="password" class="visually-hidden">Password</label>
	<div class="input-group">
		<input
			{...{ type: passwordField.type }}
			id="password"
			name="password"
			class="form-control"
			placeholder="Password"
			aria-labelledby="passwordHelpBlock"
			minlength="8"
			required
			on:focus={() => (focused = true)}
			on:blur={() => (focused = false)}
			bind:value={passwordField.value}
			on:input={passwordCustomValidity}
		/>
		<button
			type="button"
			class="btn btn-outline-secondary"
			on:click={() => (passwordField.type = passwordField.type === "password" ? "text" : "password")}
		>
			<Fa icon={passwordField.type === "password" ? faEye : faEyeSlash} />
		</button>
	</div>
	<div id="passwordHelpBlock" class="form-text">
		{#each requirements as requirement}
			<div
				class="requirement d-flex flex-row align-items-center gap-1"
				class:valid={requirement.matches(passwordField.value)}
			>
				<Fa
					icon={requirement.matches(passwordField.value) ? faSquareCheck : faSquareXmark}
					class={requirement.matches(passwordField.value) ? "text-success" : "text-danger"}
				/>
				<span>{requirement.message}</span>
			</div>
		{/each}
	</div>
</div>

<div id="confirmPasswordField">
	<label for="confirmPassword" class="visually-hidden">Confirm Password</label>
	<div class="input-group">
		<input
			{...{ type: confirmField.type }}
			id="confirmPassword"
			name="confirmPassword"
			class="form-control"
			placeholder="Confirm Password"
			minlength="8"
			required
			bind:value={confirmField.value}
			on:input={confirmCustomValidity}
		/>
		<button
			type="button"
			class="btn btn-outline-secondary"
			on:click={() => (confirmField.type = confirmField.type === "password" ? "text" : "password")}
		>
			<Fa icon={confirmField.type === "password" ? faEye : faEyeSlash} />
		</button>
	</div>
	<div id="confirmPasswordHelpBlock" class="form-text">
		<div class="requirement d-flex flex-row align-items-center gap-1" class:valid={samePassword}>
			<Fa
				icon={samePassword ? faSquareCheck : faSquareXmark}
				class={samePassword ? "text-success" : "text-danger"}
			/>
			<span>Passwords do not match</span>
		</div>
	</div>
</div>

<style>
	/* When the requirement is valid, make it disappear with a transition */
	.requirement.valid {
		animation: validRequirement 0.5s ease-in-out 1;
		opacity: 0;
		height: 0;
	}

	@keyframes validRequirement {
		0%,
		50% {
			opacity: 1;
			height: 100%;
		}

		99% {
			height: 100%;
		}
		100% {
			opacity: 0;
			height: 0;
		}
	}
</style>
