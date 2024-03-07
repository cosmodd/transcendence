<script lang="ts">
	export let tournament: {
		id: number;
		name?: string;
		players: string[];
		maxPlayers: number;
		state: 0 | 1 | 2;
	};

	const states = [
		"Waiting for players",
		"In progress",
		"Finished"
	]
</script>

<div class="card mb-3">
	<div class="card-body">
		<h5 class="card-title">{tournament.name}</h5>
		<p class="card-text">{tournament.players.length}/{tournament.maxPlayers}</p>
		<p class="card-text">State: {tournament.state}</p>
	</div>
</div>