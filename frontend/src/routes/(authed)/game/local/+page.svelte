<svelte:head>
	<script src="/static/pong/sources/main.js" type="module"></script>
	<script type="module">
		import Init from "/static/pong/sources/main.js";
		Init("game_type_local");
	</script>
	<link rel="stylesheet" href="/static/pong/style/style.css">
</svelte:head>

<div class="wrapper position-relative">
	<canvas class="position-relative card border-2 mx-auto w-100 blur-5" id="glcanvas">
	</canvas>
	<div class="position-absolute top-0 start-50 translate-middle-x text-center d-flex flex-row">
		<span id="score1" class="bg-secondary px-3 py-2 rounded-start blur-5"></span>
		<span id="time" class="bg-light px-3 py-2 text-dark blur-5" style="font-variant-numeric: tabular-nums;"></span>
		<span id="score2" class="bg-secondary px-3 py-2 rounded-end blur-5"></span>
	</div>
	<button class="position-absolute start-50 top-50 translate-middle btn btn-primary" id="ready" ></button>
</div>