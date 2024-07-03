interface Tournament {
	name: string;
	id: number;
	status: "looking_for_players" | "in_progress" | "over" | "cancelled";
	size: 4 | 8;
	players_count: number;
	players: string[];
	games: TournamentGame[];
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
	buttons?: ToastButton[];
	remove: () => void;
};

interface ToastButton {
	label: string;
	dismiss?: boolean;
	action: () => void;
};

interface ToastOptions {
	description: string;
	duration?: number;
	title?: string;
	type?: "info" | "success" | "warning" | "error";
	showProgress?: boolean;
	buttons?: Partial<ToastButton>[];
};