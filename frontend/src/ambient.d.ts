// ------------------------------------------ //
// Users                                      //
// ------------------------------------------ //
interface SimpleUser {
	display_name: string;
	username: string;
	profile_image: string;
	is_online: boolean;
};

// ------------------------------------------ //
// Tournaments                                //
// ------------------------------------------ //
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


// ------------------------------------------ //
// Toasts                                     //
// ------------------------------------------ //
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
	buttons?: ToastButton[];
};

// ------------------------------------------ //
// Friends                                    //
// ------------------------------------------ //
interface FriendRelationData {
	id: number;
	user: SimpleUser;
	friend: SimpleUser;
	created_at: string;
};

interface FriendRequestData {
	id: number;
	from_user: SimpleUser;
	to_user: SimpleUser;
	created_at: string;
}