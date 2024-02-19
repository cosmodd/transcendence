import { navigateTo } from '../../scripts/router.js';

export default (container) => {
	const render = () => {
		const userInformations = JSON.parse(localStorage.getItem('user'));

		container.innerHTML = /*html*/ `
			<nav class="navbar navbar-expand mb-2">
				<div class="container">
					<a href="/" class="navbar-brand col-2 fw-bold">
						<svg
							xmlns="http://www.w3.org/2000/svg"
							width="24"
							height="24"
							fill="currentColor"
							viewBox="0 0 512 512"
							class="me-2 align-text-top"
						>
							<path
								d="M496.2 296.5C527.7 218.7 512 126.2 449 63.1 365.1-21 229-21 145.1 63.1l-56 56.1 211.5 211.5c46.1-62.1 131.5-77.4 195.6-34.2zm-217.9 79.7L57.9 155.9c-27.3 45.3-21.7 105 17.3 144.1l34.5 34.6L6.7 424c-8.6 7.5-9.1 20.7-1 28.8l53.4 53.5c8 8.1 21.2 7.6 28.7-1L177.1 402l35.7 35.7c19.7 19.7 44.6 30.5 70.3 33.3-7.1-17-11-35.6-11-55.1-.1-13.8 2.5-27 6.2-39.7zM416 320c-53 0-96 43-96 96s43 96 96 96 96-43 96-96-43-96-96-96z"
							/>
						</svg>
						Transcendence
					</a>
					<ul class="navbar-nav justify-content-center update-active">
						<li class="nav-item"><a href="/play" class="nav-link">Play</a></li>
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
							<a href="#" data-bs-toggle="dropdown" class="text-decoration-none text-reset d-flex align-items-center gap-2">
								${userInformations?.username}
								<img src="${
									userInformations?.avatar ?? '/assets/avatars/default.jpg'
								}" alt="Avatar" class="rounded-circle me-2" width="32" height="32" />
							</a>
							<ul class="dropdown-menu dropdown-menu-end mt-2">
								<li>
									<a class="dropdown-item" href="/profile">Profile</a>
								</li>
								<li>
									<a class="dropdown-item" href="/settings">Settings</a>
								</li>
								<div class="dropdown-divider"></div>
								<li>
									<a class="dropdown-item text-danger" href="/logout" id="logout">Logout</a>
								</li>
							</ul>
						</div>
					</div>
				</div>
			</nav>
			<main id="root" class="container h-100"></main>
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

	render();
	addReactivity();
};
