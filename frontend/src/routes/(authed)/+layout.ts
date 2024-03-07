import { redirect } from "@sveltejs/kit";
import { user } from "../../lib/stores/user.js";

export async function load({ url }) {
	if (!localStorage.getItem('token')) throw redirect(302, '/login');
	if (url.pathname === '/') throw redirect(302, '/play');

	// Load user informations
	const res = await fetch('https://dummyjson.com/users/1');

	if (res.status !== 200) throw redirect(302, '/login');

	const userData = await res.json();
	user.set(userData);

	return { user: userData };
}