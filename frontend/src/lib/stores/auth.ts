import { browser } from "$app/environment";
import { get, writable } from "svelte/store";
import { user } from "./user";
import lodash from "lodash";

function isJSON(str: any) {
	// Check if the string is an empty string
	if (typeof str !== 'string' || str.trim() === '') {
		return false;
	}

	// Regular expression to test for a valid JSON structure
	const jsonPattern = /^[\],:{}\s]*$/;
	const jsonValid = /\\(?:["\\\/bfnrt]|u[0-9a-fA-F]{4})/g;
	const jsonEscape = /"[^"\\\n\r]*"|true|false|null|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?/g;
	const jsonBracket = /(?:^|:|,)(?:\s*\[)+/g;

	return jsonPattern.test(str.replace(jsonValid, '@')
		.replace(jsonEscape, ']')
		.replace(jsonBracket, ''));
}

const _auth = browser ? localStorage.getItem('auth') : null;

export const authStore = writable(_auth != null ? JSON.parse(_auth) : null)

export function login(accessToken: string, refreshToken: string): void {
	authStore.set({ accessToken, refreshToken });
	localStorage.setItem('auth', JSON.stringify({ accessToken, refreshToken }));
}

export function authedFetch(url: RequestInfo | URL, options?: RequestInit): Promise<Response> {
	let headers: HeadersInit = {
		'Content-Type': 'application/json',
		'Authorization': `Bearer ${get(authStore)?.accessToken}`
	};

	// If body is FormData, remove Content-Type header
	if (!isJSON(options?.body))
		delete headers['Content-Type'];

	return fetch(url, lodash.merge({ headers }, options));
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
	user.set({});
	authStore.set(null);
	localStorage.removeItem('auth');
}

export function isAuthed(): boolean {
	return get(authStore) != null;
}

export function authToken(): string | null {
	return get(authStore)?.accessToken;
}