interface Tournament {
	name: string;
	id: number;
	status: string;
	size: 4 | 8;
	players_count: number;
	players: string[];
};

interface TournamentGame {
	winner: string;
	players: string[];
	scores: number[]
	type: 'duel' | 'tournament';
	round: 'none' | 'quarter' | 'semi' | 'final';
	status: 'in_progress' | 'over' | 'cancelled';
	timeout: boolean;
	date_begin: string;
};