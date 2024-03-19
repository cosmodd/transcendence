import { redirect } from "@sveltejs/kit";
import { isAuthed } from "$lib/stores/auth.js";

export async function load({ url }) {
	if (!isAuthed()) throw redirect(302, '/login');
	if (url.pathname === '/') throw redirect(302, '/play');
}