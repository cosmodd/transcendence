import { redirect } from "@sveltejs/kit";
import { isAuthed } from "$lib/stores/auth.js";

export async function load() {
	if (isAuthed()) redirect(302, '/');
}