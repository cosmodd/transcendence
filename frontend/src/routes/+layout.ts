import { goto } from "$app/navigation";

export const ssr = false;

export async function load({ url }) {
	const isAuthed = localStorage.getItem('token') != null;

	if (url.pathname === '/') {
		if (isAuthed) goto('/play');
		else goto('/login');
	}
}