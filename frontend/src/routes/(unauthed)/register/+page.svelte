<script lang="ts">
	import Logo42 from "$lib/assets/icons/42.svelte";
	import Fa from "svelte-fa";
	import { faRightToBracket } from "@fortawesome/free-solid-svg-icons";
	import { goto } from "$app/navigation";

	function handleForm(event: SubmitEvent) {
		const formData = new FormData(event.target as HTMLFormElement);

		const username = formData.get("username") as string;
		const email = formData.get("email") as string;
		const password = formData.get("password") as string;

		console.log({ username, email, password });
	}
</script>

<form
	class="card p-5 d-flex flex-column gap-3 needs-validation"
	id="register-form"
	style="min-width: 400px;"
	on:submit|preventDefault={handleForm}
	novalidate
>
	<h1 class="h3 fw-normal">Register</h1>
	<div id="usernameField">
		<label for="username" class="visually-hidden">Username</label>
		<input
			type="text"
			id="username"
			name="username"
			class="form-control"
			placeholder="Username"
			value="username"
			required
		/>
		<div class="valid-feedback">Looks good!</div>
	</div>
	<label for="email" class="visually-hidden">Email</label>
	<input
		type="email"
		id="email"
		name="email"
		class="form-control"
		placeholder="mail@domain.ext"
		value="username@user.com"
		required
	/>
	<div>
		<label for="password" class="visually-hidden">Password</label>
		<input
			type="password"
			id="password"
			name="password"
			class="form-control"
			placeholder="Password"
			value="password"
			aria-labelledby="passwordHelpBlock"
			required
		/>
		<div class="form-text" id="passwordHelpBlock">Password must be at least 8 characters long</div>
	</div>
	<label for="password-confirm" class="visually-hidden">Confirm Password</label>
	<input
		type="password"
		id="password-confirm"
		class="form-control"
		placeholder="Confirm Password"
		value="password"
		required
	/>
	<p class="mb-0 text-muted">Already have an account? <a href="/login">Login</a></p>
	<div class="d-flex flex-column justify-content-center gap-2">
		<button class="btn btn-primary d-flex justify-content-center gap-2 align-items-center" type="submit">
			<Fa icon={faRightToBracket} />
			Register
		</button>
		<button
			type="button"
			id="intra-login"
			class="btn bg-black text-white d-flex justify-content-center gap-2 align-items-center"
		>
			<Logo42 style="width: 20px; height: 20px; fill: white;" />
			Register with intra
		</button>
	</div>
</form>

<style>
	.disabled {
		cursor: not-allowed !important;
	}
</style>
