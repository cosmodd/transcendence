import { writable } from "svelte/store";

export const user = writable({});

export const setUser = (data) => user.set(data);