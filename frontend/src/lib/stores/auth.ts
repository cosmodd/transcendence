import { browser } from "$app/environment";
import { get, writable } from "svelte/store";

const _auth = browser ? localStorage.getItem('auth') : null;

export const authStore = writable(_auth != null ? JSON.parse(_auth) : null)

export function login(accessToken: string, refreshToken: string): void {
	authStore.set({ accessToken, refreshToken });
	localStorage.setItem('auth', JSON.stringify({ accessToken, refreshToken }));
}

export function authedFetch(url: RequestInfo | URL, options?: RequestInit): Promise<Response> {
	return fetch(url, Object.assign({
		headers: {
			'Authorization': `Bearer ${get(authStore)?.accessToken}`,
			'Content-Type': 'application/json'
		}
	}, options));
}

export async function refreshAccessToken(): Promise<boolean> {
	const response = await fetch('/api/token/refresh/', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({
			refresh: get(authStore)?.refreshToken
		})
	});

	if (!response.ok) {
		logout();
		return false;
	}

	const data = await response.json();
	login(data.access, get(authStore)?.refreshToken);
	return true;
}

export function logout(): void {
	authStore.set(null);
	localStorage.removeItem('auth');
}

export function isAuthed(): boolean {
	return get(authStore) != null;
}

export function authToken(): string | null {
	return get(authStore)?.accessToken;
}