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
	chatting_with: SimpleUser;
	message_type?: string;
};

export let socket: WebSocket | null = null;

export function initWebsocket() {
	const token = authToken();

	socket = new WebSocket(`wss://${window.location.host}/ws/chat/${token}/`);

	socket.onopen = () => {
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
		let wsOnlineStatusEvent = new CustomEvent('wsonlinestatus', {
			detail: data,
		});

		if (data.message_type === 'notification') {
			window.dispatchEvent(notificationEvent);
			console.log('Received notification :', data);
			return;
		} else if (data.message_type === 'online_status') {
			window.dispatchEvent(wsOnlineStatusEvent);
			console.log('Received message :', data);
		} else {
			window.dispatchEvent(wsMessageEvent);
			console.log('Received message :', data);
		}
	};

	socket.onclose = () => {
		console.log('Disconnected from websocket');
	};

	socket.onerror = () => {
		console.log('Error in websocket connection');
	};
}

export function sendMessage(message: string, room_name: string) {
	if (socket) {
		console.log('Sending message :', JSON.stringify({ message, room_name }));
		socket.send(JSON.stringify({ message, room_name }));
	} else {
		console.log('Websocket not connected');
	}
}

export function sendInvitation(message_type: string, room_name: string) {
	if (socket) {
		console.log('Sending invitation :', JSON.stringify({ message_type, room_name }));
		socket.send(JSON.stringify({ message_type, room_name }));
	} else {
		console.log('Websocket not connected');
	}
}