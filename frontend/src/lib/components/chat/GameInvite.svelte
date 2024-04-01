<script lang="ts">
	import { faGamepad, faRightToBracket, faTrophy } from "@fortawesome/free-solid-svg-icons";
	import Fa from "svelte-fa";

	export let type: "casual" | "tournament" = "casual";
	$: icon = type === "casual" ? faGamepad : faTrophy;
</script>

<div class="d-flex flex-row justify-content-between align-items-center">
	<div
		class="p-3 d-flex flex-row align-items-center gap-3 bg-{type === 'casual'
			? 'success'
			: 'danger'} bg-gradient rounded"
	>
		<div class="d-flex flex-column">
			<div class="fw-bold d-flex gap-2 align-items-center">
				<Fa {icon} />
				{type === "casual" ? "Game" : "Tournament"} invite
			</div>
			<div class="text-muted">You've been invited to a {type === "casual" ? "game" : "tournament"}</div>
		</div>
		<!-- Join button to redirect to game page -->
		<a href="/game/0" class="btn btn-dark d-flex flex-row align-items-center gap-2">
			<Fa icon={faRightToBracket} />
		</a>
	</div>
</div>
