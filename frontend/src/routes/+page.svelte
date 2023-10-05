<script>
	import { onMount } from 'svelte';

	let data = [];
	let raceOptions = [
		'Human',
		'Elf',
		'Dwarf',
		'Halfling',
		'Gnome',
		'Half-Elf',
		'Half-Orc',
		'Other'
	];

	onMount(async () => {
		setTimeout(async () => {
			fetchData();
		}, 1000);
	});

	function fetchData() {
		fetch('/api/')
			.then(res => res.json())
			.then(json => {
				data = json;
			});
	}

	function handleSubmit(event) {
		const data = {
			name: event.target.name.value,
			age: event.target.age.value,
			race: event.target.race.value
		};

		fetch('/api/', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(data)
		}).then(res => fetchData());
	}

</script>

<h1>API Test</h1>

{#if data.length}
	<ol>
		{#each data as item}
			<div class="card">
				<div class="info">
					<p class="name">{item.name}</p>
					<p class="age">{item.age}</p>
				</div>
				<p class="race">{item.race}</p>
			</div>
		{/each}
	</ol>
{:else}
	<p>loading...</p>
{/if}

<form on:submit|preventDefault={handleSubmit}>
	<!-- name, age, race -->
	<input type="text" name="name" placeholder="name" />
	<input type="number" name="age" placeholder="age" />
	<select name="race">
		{#each raceOptions as option}
			<option value={option}>{option}</option>
		{/each}
	</select>
	<input type="submit" value="post">
</form>

<style lang="scss">

	* {
		box-sizing: border-box;
		padding: 0;
		margin: 0;
		font-family: sans-serif;
	}

	ol {
		list-style: none;
		padding: 0;
		margin: 0;

		display: flex;
		flex-direction: column;
		gap: 8px;
	}

	.card {
		width: 100%;
		background: #f0f0f0;
		border-radius: 8px;
		padding: 8px;
		display: grid;
		grid-template-columns: 1fr min-content;
		grid-template-rows: min-content min-content;
		grid-template-areas: 
			"info info"
			"race race";

		.info { grid-area: info; }
		.race { grid-area: race; }

		.info {
			display: flex;
			flex-direction: row;
			gap: 8px;
			align-items: end;

			.name {
				font-weight: bold;
				font-size: 1.2rem;
			}
		}
	}
</style>