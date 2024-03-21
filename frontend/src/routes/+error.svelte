<script lang="ts">
	import { page } from "$app/stores";
</script>

<div class="container d-flex flex-column justify-content-center vh-100 position-relative">
	<span class="decoration position-absolute fw-bold">{$page.status}</span>
	<h1 class="display-1 fw-bold" id="title">{$page.status}</h1>
	<h3>{$page.error?.message}</h3>
	<a href="/">Go Home</a>
</div>

<style>
	.decoration {
		right: 0;
		z-index: -1;
		opacity: 0.1;
		font-size: 30rem;
	}
</style>
