import { redirect } from "@sveltejs/kit";
import { authToken, isAuthed } from "$lib/stores/auth.js";
import { user } from "$lib/stores/user.js";

async function loadUser(fetch: Function) {
	const response = await fetch('/api/user/', {
		headers: {
			'Authorization': `Bearer ${authToken()}`
		}
	});

	if (!response.ok) return;

	const data = await response.json();
	user.set(data);
}

export async function load({ fetch, url }) {
	if (!isAuthed()) throw redirect(302, '/login');
	loadUser(fetch);

	if (url.pathname === '/') throw redirect(302, '/play');
}