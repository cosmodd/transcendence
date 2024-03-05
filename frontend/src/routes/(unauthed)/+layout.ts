import { redirect } from "@sveltejs/kit";

export async function load({ url }) {
	if (localStorage.getItem('token')) {
		throw redirect(302, '/play');
	}
}