import { redirect } from "@sveltejs/kit";
import { authToken, isAuthed, logout, refreshAccessToken } from "$lib/stores/auth.js";
import { user } from "$lib/stores/user.js";

async function loadUser(fetch: Function) {
	let response = await fetch('/api/user/', {
		headers: {
			'Authorization': `Bearer ${authToken()}`
		}
	});

	if (!response.ok) {
		if (!refreshAccessToken()) {
			logout();
			throw redirect(302, '/login');
		}
		response = await fetch('/api/user/', {
			headers: {
				'Authorization': `Bearer ${authToken()}`
			}
		});
	}

	const data = await response.json();
	user.set(data);
}

export async function load({ fetch, url }) {
	if (!isAuthed()) throw redirect(302, '/login');
	loadUser(fetch);

	if (url.pathname === '/') throw redirect(302, '/play');
}