<svelte:head>
	<script src="/static/pong/sources/main.js" type="module"></script>
	<script type="module">
		import Init from "/static/pong/sources/main.js";
		Init("game_type_online");
	</script>
	<link rel="stylesheet" href="/static/pong/style/style.css">
</svelte:head>

<div class="wrapper h-100 position-relative">
	<canvas class="card border-2 mx-auto w-100" id="glcanvas">
	</canvas>
	<div class="position-absolute top-0 start-50 translate-middle-x text-center d-flex flex-row">
		<span id="score1" class="bg-secondary px-3 py-2 rounded-start"></span>
		<span id="time" class="bg-light px-3 py-2 text-dark"></span>
		<span id="score2" class="bg-secondary px-3 py-2 rounded-end"></span>
	</div>
	<button class="btn btn-warning" id="ready" ></button>
</div>