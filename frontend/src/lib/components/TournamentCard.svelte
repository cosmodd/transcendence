<script lang="ts">
	import { faJoint, faUserGroup } from "@fortawesome/free-solid-svg-icons";
	import Fa from "svelte-fa";

	export let tournament: {
		id: number;
		name?: string;
		players: string[];
		maxPlayers: number;
	};

	const states = ["Waiting for players", "In progress"];
</script>

<div class="card p-4 d-flex flex-column gap-1">
	<h4 class="m-0 fw-bold">{tournament.name || `Tournament ${tournament.id}`}</h4>
	<!-- Tournament players with an icon in front -->
	<div class="d-flex flex-row align-items-center gap-2 mb-2 text-muted">
		<Fa icon={faUserGroup} />
		<span>{tournament.players.length} / {tournament.maxPlayers} players</span>
	</div>
	<a href="/tournament/{tournament.id}" class="btn btn-primary">Join</a>
</div>