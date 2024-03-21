import { writable, type Writable } from "svelte/store";

interface User {
	id: number;
	display_name: string;
	username: string;
	profile_image: string;
}

// Populate the user store with the current user information at `/api/user/`


export const user: Writable<Partial<User>> = writable({});