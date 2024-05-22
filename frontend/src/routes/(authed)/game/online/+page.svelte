<script lang='ts'>
    import { initial } from "lodash";
    import { onDestroy, onMount } from "svelte";

	onDestroy(() => {
		ServerAPI.websocket.close();
	});

	// onMount(() => {
	// 	Init("game_type_online");
	// })
</script>

<svelte:head>
	<script src="/static/pong/sources/main.js" type="module"></script>
	<script type="module">
		import Init from "/static/pong/sources/main.js";

		Init("game_type_online");
	</script>
	<link rel="stylesheet" href="/static/pong/style/style.css">
</svelte:head>

<div class="wrapper h-100 position-relative">
	<div id="blurcul" class="blur-5">
		<canvas class="position-relative card border-2 mx-auto w-100" id="glcanvas">
		</canvas>
		<div class="position-absolute top-0 start-50 translate-middle-x text-center d-flex flex-row">
			<span id="left_username" class="px-3 py-2"></span>
			<span id="score1" class="bg-secondary px-3 py-2 rounded-start"></span>
			<span id="time" class="bg-light px-3 py-2 text-dark"></span>
			<span id="score2" class="bg-secondary px-3 py-2 rounded-end"></span>
			<span id="right_username" class="px-3 py-2"></span>
		</div>
	</div>
	<button class="position-absolute start-50 top-50 translate-middle btn btn-primary" id="ready" ></button>
</div>