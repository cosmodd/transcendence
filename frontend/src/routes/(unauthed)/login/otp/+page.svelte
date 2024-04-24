<script lang="ts">
	import InputOTP from "$lib/components/auth/InputOTP.svelte";
	import Fa from "svelte-fa";
	import {
		faArrowLeft,
		faArrowRight,
		faRightToBracket,
		faTriangleExclamation,
	} from "@fortawesome/free-solid-svg-icons";
	import { page } from "$app/stores";
	import { login } from "$lib/stores/auth";
	import { goto } from "$app/navigation";

	const id = $page.url.searchParams.get("id");
	let alertMessage = "";

	async function handleOTP(event: SubmitEvent) {
		const formData = new FormData(event.target as HTMLFormElement);
		const code = formData.get("otp");

		if (id == null || code == null) return;

		const response = await fetch("/api/fa/", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify({ id, code }),
		});

		const responseData = await response.json();

		if (!response.ok) {
			alertMessage = responseData["message"];
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
	on:submit|preventDefault={handleOTP}
>
	<h1 class="h3 d-flex gap-3">
		<a href="/login" class="text-decoration-none text-body"><Fa icon={faArrowLeft} size="1x" /></a>
		Enter 2FA Code
	</h1>

	{#if alertMessage}
		<div class="alert alert-danger m-0" role="alert">
			<Fa icon={faTriangleExclamation} />
			{alertMessage}
		</div>
	{/if}

	<InputOTP autofocus />
	<div class="d-flex flex-column justify-content-center gap-2">
		<button type="submit" class="btn btn-primary d-flex justify-content-center gap-2 align-items-center">
			<Fa icon={faRightToBracket} />
			Login
		</button>
	</div>
</form>
