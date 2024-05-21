import { writable } from 'svelte/store';
import { authToken } from './auth';
export type ChatMessage = {
	sender: string;
	message: string;
	room_name: string;
	timestamp: string;
	message_type?: string;
	is_accepted?: boolean;
};

export type Conversation = {
	room_name: string;
	last_message: string | null;
	last_message_sender: string | null;
	chatting_with: string;
	message_type?: string;
};

export const wsConnectionStatus = writable<'connected' | 'disconnected' | 'error'>('disconnected');
let socket: WebSocket | null = null;

let token = authToken();

function initWebsocket() {

	socket = new WebSocket(`wss://localhost/ws/chat/${token}/`);

	socket.onopen = () => {
		wsConnectionStatus.set('connected');
		console.log('Connected to websocket');
	};

	socket.onmessage = (event) => {
		const data = JSON.parse(event.data.toString());
		let notificationEvent = new CustomEvent('notification', {
			detail: data,
		});

		let wsMessageEvent = new CustomEvent('wsmessage', {
			detail: data,
		});

		if (data.message_type === 'notification') {
			window.dispatchEvent(notificationEvent);
			console.log('Received notification :', data);
			return;
		}
		else {
			window.dispatchEvent(wsMessageEvent);
			console.log('Received message :', data);
		}
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
		console.log('Sending message :', JSON.stringify({message, room_name }));
		socket.send(JSON.stringify({ message, room_name }));
	} else {
		console.log('Websocket not connected');
	}
}

export function sendInvitation(message_type: string, room_name:string) {
	if (socket) {
		console.log('Sending invitation :', JSON.stringify({ message_type, room_name}));
		socket.send(JSON.stringify({ message_type, room_name }));
	} else {
		console.log('Websocket not connected');
	}
}