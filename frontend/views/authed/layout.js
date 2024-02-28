import { navigateTo } from '../../scripts/router.js';

export default (container) => {

	const addCSS = () => {
		const layoutCSS = document.querySelector('style[data-dynamic]');

		layoutCSS.textContent += /*css*/ `
			body {
				display: grid;
				grid-template-rows: auto 1fr;
			}
		`;
	};

	const render = () => {
		const userInformations = JSON.parse(localStorage.getItem('user'));

		container.innerHTML = /*html*/ `
			<nav class="navbar navbar-expand mb-2">
				<div class="container">
					<a href="/" class="navbar-brand col-2 fw-bold">
						<i class="fa-solid fa-fw fa-table-tennis-paddle-ball"></i>
						Transcendence
					</a>
					<ul class="navbar-nav justify-content-center update-active">
						<li class="nav-item"><a href="/" class="nav-link">Play</a></li>
						<li class="nav-item"><a href="/tournaments" class="nav-link">Tournaments</a></li>
						<li class="nav-item"><a href="/leaderboard" class="nav-link">Leaderboard</a></li>
						<li class="nav-item"><a href="/chat" class="nav-link">Chat</a></li>
					</ul>
					<div class="d-flex justify-content-end col-2">
						<!-- TODO: Implement a search feature to find people's profile -->
						<!-- <form class="d-flex gap" role="search">
							<input
								class="form-control"
								type="search"
								placeholder="Search"
								aria-label="Search"
							/>
						</form> -->
						<div class="dropdown profile">
							<a href="#" data-bs-toggle="dropdown" class="text-decoration-none text-reset d-flex align-items-center gap-2 fw-bold">
								${userInformations?.displayname}
								<img src="${userInformations?.avatar ?? '/assets/avatars/default.jpg'}" alt="Avatar" class="rounded-circle me-2" width="32" height="32" />
							</a>
							<ul class="dropdown-menu dropdown-menu-end mt-2">
								<li><a class="dropdown-item" href="/profile">Profile</a></li>
								<li><a class="dropdown-item" href="/settings">Settings</a></li>
								<div class="dropdown-divider"></div>
								<li><a class="dropdown-item text-danger" href="/logout" id="logout">Logout</a></li>
							</ul>
						</div>
					</div>
				</div>
			</nav>
			<main id="root" class="container-fluid overflow-y-auto p-3 pt-0"></main>
		`;
	};

	const addReactivity = () => {
		const activeNavbar = document.querySelector('.update-active');
		const activeClasses = ['active', 'fw-bold'];

		window.addEventListener('routing', () => {
			const links = activeNavbar.querySelectorAll('a');
			links.forEach((link) => {
				if (link.pathname === window.location.pathname) {
					link.classList.add(...activeClasses);
				} else {
					link.classList.remove(...activeClasses);
				}
			});
		});

		document.querySelector('#logout').addEventListener('click', () => {
			localStorage.removeItem('user');
			navigateTo('/login');
		});
	};

	addCSS();
	render();
	addReactivity();
};
