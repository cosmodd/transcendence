import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

// implement a proxy to the backend server for websockets
export default defineConfig({
	plugins: [sveltekit()],
	server: {
		https: {
			key: '/certification/key.pem',
			cert: '/certification/cert.pem'
		},
		proxy: {
			'/api': 'http://django:8000',
			'/static': 'http://django:8000',
			'/media': 'http://django:8000',
			'/ws': 'ws://django:8000'
		}
	}
});
