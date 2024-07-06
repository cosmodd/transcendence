<script lang="ts">
	import { beforeNavigate, goto } from "$app/navigation";
	import { onDestroy, onMount } from "svelte";
	import Init from "../shared/sources/main.js";
	import toasts from "$lib/stores/toasts.js";

	let cancelRedirect: boolean = false;

	beforeNavigate(() => {
		cancelRedirect = true;
	});

	onDestroy(() => {
		ServerAPI.websocket.close();
	});

	onMount(() => {
		Init("game_type_online");
		ServerAPI.websocket.addEventListener("close", () => {
			if (cancelRedirect) return;

			toasts.add({
				description: "Game finished, redirecting to home...",
				duration: 2000,
			});

			setTimeout(() => {
				if (cancelRedirect) return;
				goto("/");
			}, 2000);
		});
	});
</script>

<div class="wrapper h-100 position-relative">
	<div class="blur-5" id="blurcul">
		<canvas class="position-relative card border-2 mx-auto w-100" id="glcanvas"></canvas>
		<div class="position-absolute top-0 start-50 translate-middle-x text-center d-flex flex-row">
			<span id="left_username" class="px-3 py-2"></span>
			<span id="score1" class="bg-secondary px-3 py-2 rounded-start"></span>
			<span id="time" class="bg-light px-3 py-2 text-dark"></span>
			<span id="score2" class="bg-secondary px-3 py-2 rounded-end"></span>
			<span id="right_username" class="px-3 py-2"></span>
		</div>
	</div>
	<button class="position-absolute start-50 top-50 translate-middle btn btn-primary" id="ready"></button>
</div>

<style>
	.blur-5 {
		filter: blur(5px);
	}
</style>
