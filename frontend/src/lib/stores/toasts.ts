import { defaults } from "lodash";
import { writable } from "svelte/store";

function createToastStore() {

	const store = writable<ToastData[]>([]);
	const { set, update, subscribe } = store;

	const defaultOptions = {
		duration: 3000,
		showProgress: true,
		type: "info" as ToastData["type"],
	};

	function add(options: ToastOptions) {
		const { duration, description, ...rest } = defaults(options, defaultOptions);
		const uid = Date.now();

		const object: ToastData = {
			uid,
			duration,
			description,
			...rest,
			remove: () => {
				update((toasts) => toasts.filter((toast) => toast.uid !== uid));
			},
		};

		update((toasts) => [...toasts, object]);
		if (duration > 0) setTimeout(object.remove, duration);

		return object;
	}

	return {
		subscribe,
		add,
		clear: () => set([])
	};
}

const toasts = createToastStore();
export default toasts;