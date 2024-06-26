import { authedFetch } from '$lib/stores/auth.js';

export async function load({ params }) {
	const response = await authedFetch(`/api/tournament/${params.id}/`);

	if (!response.ok) {
		return {
			tournament: null
		};
	}

	const tournament = await response.json();
	const rounds = Array.from({ length: Math.log2(tournament.size - 1) }, (_, i) => Math.pow(2, i + 1)).reverse();


	let gamesCopy = tournament.games.slice().concat(Array(tournament.size - 1 - tournament.games.length).fill(null));
	const arrangedGames: TournamentGame[][] = rounds.reduce((acc: TournamentGame[][], gamesCount) => [...acc, gamesCopy.splice(0, gamesCount)], [])

	return { tournament, arrangedGames };
}