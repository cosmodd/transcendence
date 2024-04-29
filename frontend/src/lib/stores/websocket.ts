import { writable } from 'svelte/store';
import WebSocket from 'ws';
import { authToken } from './auth';

const socket = new WebSocket(`ws://localhost:8000/ws/chat/`, { headers: {
    Authorization: `Bearer ${authToken()}`
} });

export const websocket = writable(socket);

socket.onopen = () => {
  console.log('WebSocket connection established');
};

socket.onclose = () => {
  console.log('WebSocket connection closed');
};

socket.onerror = (error) => {
  console.error('WebSocket error:', error);
};

socket.onmessage = (event) => {
  console.log('WebSocket message:', event.data);
};

export const send = (data: string) => {
  socket.send(data);
};