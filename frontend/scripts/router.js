import HTTPError from '../views/errors/error.js';
import SomethingWentWrong from '../views/errors/fail.js';
import AuthedLayout from '../views/authed/layout.js';

const routing = new Event('routing');

const unauthedRoutes = [
	{
		path: /^\/register$/,
		viewPath: '../views/unauthed/register.js'
	},
	{
		path: /^\/login$/,
		viewPath: '../views/unauthed/login.js'
	}
];

const authedRoutes = [
	{
		path: /^\/play$/,
		viewPath: '../views/authed/Play.js'
	},
	{
		path: /^\/test$/,
		viewPath: '../views/errors/fail.js'
	}
];

function replaceLinks() {
	document.querySelectorAll('a').forEach((link) => {
		// Ignore links with a different origin
		if (link.origin !== window.location.origin) return;
		if (link.pathname === window.location.pathname) return;

		link.addEventListener('click', (e) => {
			console.log(`Navigating to ${link.href}`);
			e.preventDefault();
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
	let route = authedRoutes.find((route) => route.path.test(path));

	if (!authed) {
		route = unauthedRoutes.find((route) => route.path.test(path));
		if (route == null) navigateTo('/login');
		replaceLinks();
	} else if (authed) {
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
			m.default(main);
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
