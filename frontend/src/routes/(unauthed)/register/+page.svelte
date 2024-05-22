<script lang="ts">
	import { login } from "$lib/stores/auth"
	import Logo42 from "$lib/assets/icons/42.svelte";
	import UsernameField from "$lib/components/auth/UsernameField.svelte";
	import PasswordField from "$lib/components/auth/PasswordField.svelte";
	import Fa from "svelte-fa";
	import { faRightToBracket, faTriangleExclamation } from "@fortawesome/free-solid-svg-icons";
	import { goto } from "$app/navigation";

	let alertMessage = "";

	async function handleForm(event: SubmitEvent) {
		const form = event.target as HTMLFormElement;
		const formData = new FormData(event.target as HTMLFormElement);

		const username = formData.get("username") as string;
		const email = formData.get("email") as string;
		const password = formData.get("password") as string;

		form.classList.add("was-validated");

		if (!form.checkValidity()) {
			event.preventDefault();
			event.stopPropagation();
			return;
		}

		const response: Response = await fetch("/api/register/", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify({
				username,
				email,
				password,
			}),
		});

		if (response == null) return;

		const responseData = await response.json();

		if (!response.ok) {
			alertMessage = responseData?.message;
			return;
		}

		login(responseData["access"], responseData["refresh"]);
		goto("/");
	}
</script>

<form
	class="card p-5 d-flex flex-column gap-3 needs-validation"
	id="register-form"
	style="min-width: 500px;"
	on:submit|preventDefault={handleForm}
	novalidate
>
	<h1 class="h3 fw-bold">Register</h1>

	{#if alertMessage}
		<div class="alert alert-danger m-0" role="alert">
			<Fa icon={faTriangleExclamation} class="me-1"/>
			{alertMessage}
		</div>
	{/if}

	<UsernameField />
	<div id="emailField">
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
	</div>
	<PasswordField />
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
