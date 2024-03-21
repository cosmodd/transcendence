import { goto } from "$app/navigation";
import { isAuthed } from "$lib/stores/auth";
import { redirect } from "@sveltejs/kit";

export const ssr = false;

export async function load({ url }) {
	if (url.pathname === "/") {
		if (!isAuthed()) goto("/login");
		else goto("/play");
	}
}