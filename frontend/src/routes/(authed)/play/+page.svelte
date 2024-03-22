<script>
	import { faComputer, faPlay, faSquarePlus, faTrophy, faUserGroup } from "@fortawesome/free-solid-svg-icons";
	import Fa from "svelte-fa";
</script>

<div class="row gap-3 mx-0 h-100" id="modes">
	<div
		class="card d-flex flex-column justify-content-end p-4 bg-danger bg-gradient border-0 col position-relative overflow-hidden"
	>
		<Fa icon={faTrophy} class="text-dark mode-illustration" />
		<h2 class="card-title fw-bold text-light">Tournaments</h2>
		<p class="card-text text-light">Play or create a new tournament</p>
		<div class="d-flex flex-row gap-2">
			<button class="btn btn-dark flex-fill">
				<Fa icon={faPlay} class="me-1" />
				Play
			</button>
			<button class="btn btn-dark flex-fill">
				<Fa icon={faSquarePlus} class="me-1" />
				Create
			</button>
		</div>
	</div>
	<div
		class="card d-flex flex-column justify-content-end p-4 bg-success bg-gradient border-0 col position-relative overflow-hidden"
	>
		<Fa icon={faUserGroup} class="text-dark mode-illustration" />
		<h2 class="card-title fw-bold text-light">Online</h2>
		<p class="card-text text-light">Play against a random opponent online</p>
		<a href="/game/online" class="btn btn-dark">
			<Fa icon={faPlay} class="me-1" />
			Play
		</a>
	</div>
	<div
		class="card d-flex flex-column justify-content-end p-4 bg-primary bg-gradient border-0 col position-relative overflow-hidden"
	>
		<Fa icon={faComputer} class="text-dark mode-illustration" />
		<h2 class="card-title fw-bold text-light">Local</h2>
		<p class="card-text text-light">Play against your fake IRL friends</p>
		<a href="/game/local" class="btn btn-dark">
			<Fa icon={faPlay} class="me-1" />
			Play
		</a>
	</div>
</div>

<style>
	:global(.mode-illustration) {
		position: absolute;
		top: 50%;
		left: 50%;
		transform: translate(-50%, -50%) rotate(-15deg);
		width: 640px;
		height: 640px !important;
		opacity: 0.2;
		z-index: -1;
	}

	#modes > div {
		z-index: 0;
	}
</style>
