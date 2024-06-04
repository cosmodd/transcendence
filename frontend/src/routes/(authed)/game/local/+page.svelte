<script lang='ts'>
    import { onMount } from "svelte";
	import Init from "../shared/sources/main.js";

	onMount(() => {
		Init("game_type_local");
	})
</script>

<style>
	.blur-5 {
		filter: blur(5px);
    }
</style>

<div class="wrapper position-relative h-100">
	 <div class="blur-5" id="blurcul">
		<canvas class="position-relative card border-2 mx-auto w-100" id="glcanvas">
		</canvas>
		<div class="position-absolute top-0 start-50 translate-middle-x text-center d-flex flex-row">
			<span id="score1" class="bg-secondary px-3 py-2 rounded-start"></span>
			<span id="time" class="bg-light px-3 py-2 text-dark" style="font-variant-numeric: tabular-nums;"></span>
			<span id="score2" class="bg-secondary px-3 py-2 rounded-end"></span>
		</div>
	</div>
	<button class="position-absolute start-50 top-50 translate-middle btn btn-primary" id="ready" ></button>
</div>