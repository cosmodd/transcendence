import { redirect } from "@sveltejs/kit";
import { authToken, authedFetch, isAuthed, logout, refreshAccessToken } from "$lib/stores/auth.js";
import { user } from "$lib/stores/user.js";

async function loadUser(fetch: Function) {
	let response = await authedFetch('/api/user/');

	if (!response.ok) {
		const tokenRefreshed = await refreshAccessToken();

		if (!tokenRefreshed) {
			console.log("Couldn't fetch a new token. Logging out.");
			logout();
			throw redirect(302, '/login');
		}

		response = await authedFetch('/api/user/');
	}

	const data = await response.json();
	user.set(data);
}

export async function load({ fetch, url }) {
	if (!isAuthed()) throw redirect(302, '/login');
	await loadUser(fetch);
}