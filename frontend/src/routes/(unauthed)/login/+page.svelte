<script lang="ts">
	import { login } from "$lib/stores/auth";
	import Logo42 from "$lib/assets/icons/42.svelte";
	import Fa from "svelte-fa";
	import { faRightToBracket, faTriangleExclamation } from "@fortawesome/free-solid-svg-icons";
	import { goto } from "$app/navigation";
	import { onMount } from "svelte";
	import { page } from "$app/stores";

	let thirdPartyLogin: boolean = false;
	let alertMessage: string = "";

	let feedbacks = {
		username: [],
		password: [],
	};

	async function handleForm(event: SubmitEvent) {
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
			alertMessage = responseData["message"] ?? "";
			return;
		}

		// Handle 2FA auth
		if (responseData["id"]) {
			console.log(responseData);
			goto(`/login/otp?id=${responseData["id"]}`);
			return;
		}

		login(responseData["access"], responseData["refresh"]);
		goto("/");
	}

	async function handle42Login(code: string) {
		const response = await fetch("/api/auth/42/", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify({ code }),
		});

		const data = await response.json();

		if (!response.ok) {
			alertMessage = data.message;
			return;
		}

		login(data["access"], data["refresh"]);
		goto("/");
	}

	onMount(() => {
		const oauthCode = $page.url.searchParams.get("code");

		if (oauthCode) {
			thirdPartyLogin = true;
			handle42Login(oauthCode);
		}
	});
</script>

{#if thirdPartyLogin}
	<div class="d-flex flex-row justify-content-center align-items-center gap-2">
		<h1 class="h3 fw-normal">Signing you in with</h1>
		<Logo42 style="width: 32px; height: 32px; fill: white;" />
	</div>
{:else}
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
			<a
				id="intra-login"
				href="/api/auth/42/redirect/"
				class="btn bg-black text-white d-flex justify-content-center gap-2 align-items-center"
			>
				<Logo42 style="width: 20px; height: 20px; fill: white;" />
				Login with intra
			</a>
		</div>
	</form>
{/if}
