<script lang="ts">
	import Logo42 from '$lib/assets/icons/42.svelte';
    import Fa from 'svelte-fa';
    import { faRightToBracket } from '@fortawesome/free-solid-svg-icons';
	import { goto } from '$app/navigation';

	function handleForm(event: SubmitEvent) {
		event.preventDefault();
		localStorage.setItem('token', 'some-token');
		goto('/test');
	}
</script>

<form class="card p-5 d-flex flex-column gap-3" id="register-form" style="min-width: 400px;" on:submit={handleForm}>
	<h1 class="h3 fw-normal">Register</h1>
	<label for="username" class="visually-hidden">Username</label>
	<input type="text" id="username" class="form-control" placeholder="Username" value="username" required autofocus />
	<label for="email" class="visually-hidden">Email</label>
	<input type="email" id="email" class="form-control" placeholder="mail@domain.ext" value="username@user.com" required />
	<label for="password" class="visually-hidden">Password</label>
	<input type="password" id="password" class="form-control" placeholder="Password" value="password" required />
	<label for="password-confirm" class="visually-hidden">Confirm Password</label>
	<input type="password" id="password-confirm" class="form-control" placeholder="Confirm Password" value="password" required />
	<p class="mb-0 text-muted">Already have an account? <a href="/login">Login</a></p>
	<div class="d-flex flex-column justify-content-center gap-2">
		<button class="btn btn-primary d-flex justify-content-center gap-2 align-items-center" type="submit">
			<Fa icon={faRightToBracket} />
			Register
		</button>
		<button type="button" id="intra-login" class="btn bg-black text-white d-flex justify-content-center gap-2 align-items-center">
			<Logo42 style="width: 20px; height: 20px; fill: white;"/>
			Register with intra
		</button>
	</div>
</form>