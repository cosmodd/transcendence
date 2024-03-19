<script lang="ts">
	import { login } from "$lib/stores/auth";
	import Logo42 from "$lib/assets/icons/42.svelte";
	import Fa from "svelte-fa";
	import { faRightToBracket, faTriangleExclamation } from "@fortawesome/free-solid-svg-icons";
	import { goto } from "$app/navigation";

	let alertMessage = "";

	let feedbacks = {
		username: [],
		password: [],
	};

	async function handleForm(event: SubmitEvent) {
		const form = event.target as HTMLFormElement;
		const formData = new FormData(event.target as HTMLFormElement);

		const data = {
			username: formData.get("username") as string,
			password: formData.get("password") as string,
		};

		const loginResponse: Response = await fetch("/api/login/", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify(data),
		});

		const responseData = await loginResponse.json();

		if (!loginResponse.ok) {
			feedbacks.username = responseData["username"] ?? [];
			feedbacks.password = responseData["password"] ?? [];
			console.log(feedbacks);
			return;
		}

		login(responseData["access"], responseData["refresh"]);
		goto("/play");
	}
</script>

<form
	class="card p-5 d-flex flex-column gap-3"
	id="login-form"
	style="min-width: 400px"
	on:submit|preventDefault={handleForm}
>
	<h1 class="h3 fw-normal">Welcome back!</h1>

	{#if alertMessage}
		<div class="alert alert-danger m-0" role="alert">
			<Fa icon={faTriangleExclamation} />
			{alertMessage}
		</div>
	{/if}

	<div id="usernameField">
		<label for="username" class="visually-hidden">Username</label>
		<input
			type="text"
			id="username"
			name="username"
			class="form-control"
			class:is-invalid={feedbacks.username.length > 0}
			on:input={() => (feedbacks.username = [])}
			placeholder="Username"
			required
		/>
		<div class="invalid-feedback">
			{#each feedbacks.username as feedback}
				{feedback}
			{/each}
		</div>
	</div>
	<div id="passwordField">
		<label for="password" class="visually-hidden">Password</label>
		<input
			type="password"
			id="password"
			name="password"
			class="form-control"
			class:is-invalid={feedbacks.password.length > 0}
			on:input={() => (feedbacks.password = [])}
			placeholder="Password"
			required
		/>
		<div class="invalid-feedback">
			{#each feedbacks.password as feedback}
				{feedback}
			{/each}
		</div>
	</div>
	<p class="mb-0 text-muted">Don't have an account? <a href="/register">Register</a></p>
	<div class="d-flex flex-column justify-content-center gap-2">
		<button class="btn btn-primary d-flex justify-content-center gap-2 align-items-center" type="submit">
			<Fa icon={faRightToBracket} />
			Sign in
		</button>
		<button
			type="button"
			id="intra-login"
			class="btn bg-black text-white d-flex justify-content-center gap-2 align-items-center"
		>
			<Logo42 style="width: 20px; height: 20px; fill: white;" />
			Login with intra
		</button>
	</div>
</form>
