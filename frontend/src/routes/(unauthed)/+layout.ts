import { redirect } from "@sveltejs/kit";
import { isAuthed } from "$lib/stores/auth.js";

export async function load({ url }) {
	url.pathname; // Executes this function when the pathname changes
	
	if (isAuthed()) redirect(302, '/');
}