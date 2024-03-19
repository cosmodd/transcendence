import { browser } from "$app/environment";
import { get, writable } from "svelte/store";

const _auth = browser ? localStorage.getItem('auth') : null;
console.log('auth', _auth);

export const authStore = writable(_auth != null ? JSON.parse(_auth) : null)

export function login(accessToken: string, refreshToken: string): void {
	authStore.set({ accessToken, refreshToken });
	localStorage.setItem('auth', JSON.stringify({ accessToken, refreshToken }));
}

export function logout(): void {
	authStore.set(null);
	localStorage.removeItem('auth');
}

export function isAuthed(): boolean {
	return get(authStore) != null;
}