import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [sveltekit()],
	server: {
		proxy: {
			'^/api/': {
				target: 'http://backend:3000',
				changeOrigin: false,
				secure: false,
				ws: false,
			}
		}
	}
});
