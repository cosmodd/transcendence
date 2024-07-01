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

interface ToastData {
	uid: number;
	duration: number;
	type: "info" | "success" | "warning" | "error";
	title?: string;
	description: string;
	showProgress?: boolean;

	remove: () => void;
};

interface ToastOptions {
	duration?: number;
	title?: string;
	description: string;
	type?: "info" | "success" | "warning" | "error";
	showProgress?: boolean;
};