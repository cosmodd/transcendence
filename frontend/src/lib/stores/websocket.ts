import { writable } from 'svelte/store';
import WebSocket from 'ws';
import { authToken } from './auth';

export const wsConnectionStatus = writable<'connected' | 'disconnected' | 'error'>('disconnected');
export const messages = writable<Array<{ sender: string, message: string, room_name: string }>>([]);
let socket: WebSocket | null = null;

function initWebsocket() {
	socket = new WebSocket(`ws://localhost:8000/ws/chat/`, { headers: {
		Authorization: `Bearer ${authToken()}`
	} });

	socket.onopen = () => {
		wsConnectionStatus.set('connected');
		console.log('Connected to websocket');
	};

	socket.onmessage = (event) => {
		const data = JSON.parse(event.data.toString());
		messages.update((msgs) => [...msgs, data]);
	};

	socket.onclose = () => {
		wsConnectionStatus.set('disconnected');
		console.log('Disconnected from websocket');
	};

	socket.onerror = () => {
		wsConnectionStatus.set('error');
		console.log('Error in websocket connection');
	};
}
initWebsocket();

export function sendMessage(message: string, room_name: string) {
	if (socket) {
		socket.send(JSON.stringify({ message, room_name }));
	} else {
		console.log('Websocket not connected');
	}
}