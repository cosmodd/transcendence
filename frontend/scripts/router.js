import HTTPError from '/views/errors/error.js';
import SomethingWentWrong from '/views/errors/fail.js';
import AuthedLayout from '/views/authed/layout.js';

const routing = new Event('routing');

const unauthed = (path) => `/views/unauthed/${path}${/\.js$/.test(path) ? '' : '.js'}`;
const authed = (path) => `/views/authed/${path}${/\.js$/.test(path) ? '' : '.js'}`;

const unauthedRoutes = {
	'/register': unauthed('register'),
	'/login': unauthed('login'),
};

const authedRoutes = {
	'/play': authed('play'),
	'/test': authed('test'),
	'/chat': authed('chat'),

	// Profile routes
	'/profile': authed('profile'),
	'/profile/:username': authed('profile'),
};

/**
 * Matches a route to a path and returns the matched params
 * **Routes format**:
 * - /path
 * - /path/:param
 * @param {string} route Route to test path against
 * @param {string} path Current browser path
 * @returns {Object | null} Returns the matched params in the path or null if no match
 */
function matchRoute(route, path) {
	const routeParts = route.split(/\//g).filter(p => p !== '');
	const pathParts = path.split(/\//g).filter(p => p !== ''); dispatchEvent

	if (routeParts.length !== pathParts.length) return null;

	let params = {};

	for (let i = 0; i < routeParts.length; i++) {
		const routePart = routeParts[i];
		let pathPart = pathParts[i];
		const paramName = routePart.startsWith(':') ? routePart.slice(1) : null;

		if (/\d+\.\d+/.test(pathPart)) pathPart = parseFloat(pathPart);
		else if (/\d+/.test(pathPart)) pathPart = parseInt(pathPart);

		if (paramName) params[paramName] = pathPart;
		else if (routePart !== pathPart) return null;
	}

	return params;
}

function findRoute(routes, path) {
	for (const route in routes) {
		const params = matchRoute(route, path);
		if (params) return { viewPath: routes[route], params };
	}
};

function replaceLinks() {
	document.querySelectorAll('a').forEach((link) => {
		// Ignore links with a different origin
		if (link.origin !== window.location.origin) return;

		link.addEventListener('click', (e) => {
			e.preventDefault();

			// If the path is the same as the current one, do nothing
			if (link.pathname === window.location.pathname) return;

			console.log(`Navigating to ${link.href}`);
			navigateTo(link.href);
		});
	});
}

// Handles routing for the app
// This function is called whenever the user navigates to a new page
// If the user is not authenticated, they will be redirected to the splash screen
// If the user is authenticated, they will be redirected to the home page hydrated with the corresponding view
async function router() {
	const path = window.location.pathname;
	const authed = localStorage.getItem('user') != null;

	let main = document.body;
	let route = null

	if (!authed) {
		route = findRoute(unauthedRoutes, path);
		if (route == null) navigateTo('/login');
		replaceLinks();
	} else if (authed) {
		route = findRoute(authedRoutes, path);
		AuthedLayout(document.body);
		main = document.querySelector('main#root');
		replaceLinks();
	}

	if (route == null || route.viewPath == null) {
		HTTPError(main, 404);
		dispatchEvent(routing);
		return;
	}

	import(route.viewPath)
		.then((m) => {
			m.default(main, route.params);
			replaceLinks();
		})
		.catch((err) => SomethingWentWrong(main, err));

	dispatchEvent(routing);
}

function navigateTo(url) {
	history.pushState(null, null, url);
	router();
}

export { router, navigateTo };
