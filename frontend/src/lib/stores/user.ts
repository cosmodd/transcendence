import { writable, type Writable } from "svelte/store";
import { authedFetch } from "./auth";

interface User {
	id: number;
	display_name: string;
	username: string;
	profile_image: string;
	enabled_2FA: boolean;
	qrcode_2FA: string;
	third_party_auth: boolean;
}

export const user: Writable<Partial<User>> = writable({});

export async function fetchUser() {
	const response = await authedFetch('/api/user/');

	if (!response.ok) return;

	const data = await response.json();
	user.set(data);
}