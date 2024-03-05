<script>
	import Logo42 from '$lib/assets/icons/42.svelte';
	import Fa from "svelte-fa";
	import { faRightToBracket } from "@fortawesome/free-solid-svg-icons";
</script>

<form class="card p-5 d-flex flex-column gap-3" id="login-form" style="min-width: 400px;">
	<h1 class="h3 fw-normal">Welcome back!</h1>
	<label for="username" class="visually-hidden">Username</label>
	<input type="text" id="username" class="form-control" placeholder="Username" required autofocus />
	<label for="password" class="visually-hidden">Password</label>
	<input type="password" id="password" class="form-control" placeholder="Password" required />
	<p class="mb-0 text-muted">Don't have an account? <a href="/register">Register</a></p>
	<div class="d-flex flex-column justify-content-center gap-2">
		<button class="btn btn-primary d-flex justify-content-center gap-2 align-items-center" type="submit">
			<Fa icon={faRightToBracket} />
			Sign in
		</button>
		<button type="button" id="intra-login" class="btn bg-black text-white d-flex justify-content-center gap-2 align-items-center">
			<Logo42 style="width: 20px; height: 20px; fill: white;"/>
			Login with intra
		</button>
	</div>
</form>