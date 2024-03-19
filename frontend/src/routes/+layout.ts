import { goto } from "$app/navigation";
import { isAuthed } from "$lib/stores/auth";

export const ssr = false;

export async function load({ url }) {
	if (url.pathname === "/") {
		if (!isAuthed()) {
			console.log("redirecting to login");
			goto("/login");
		} else {
			goto("/play");
		}
	}
}