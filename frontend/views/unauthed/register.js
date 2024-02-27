import { navigateTo } from '../../scripts/router.js';

export default (container) => {
	// Register page
	const render = () => {
		container.innerHTML = /*html*/ `
			<div class="d-flex flex-column justify-content-center align-items-center h-100">
				<form class="card p-5 d-flex flex-column gap-3" id="register-form" style="min-width: 400px;">
					<h1 class="h3 fw-normal">Register</h1>
					<label for="username" class="visually-hidden">Username</label>
					<input type="text" id="username" class="form-control" placeholder="Username" value="username" required autofocus />
					<label for="email" class="visually-hidden">Email</label>
					<input type="email" id="email" class="form-control" placeholder="mail@domain.ext" value="username@user.com" required />
					<label for="password" class="visually-hidden">Password</label>
					<input type="password" id="password" class="form-control" placeholder="Password" value="password" required />
					<label for="password-confirm" class="visually-hidden">Confirm Password</label>
					<input type="password" id="password-confirm" class="form-control" placeholder="Confirm Password" value="password" required />
					<p class="mb-0 text-muted">Already have an account? <a href="/login">Login</a></p>
					<div class="d-flex flex-column justify-content-center gap-2">
						<button class="btn btn-primary" type="submit">Register</button>
						<button type="button" id="intra-login" class="btn bg-black text-white d-flex justify-content-center gap-2">
							<img src="/assets/svg/42.svg" alt="Intra" width="24" height="24" />
							Register with intra
						</button>
					</div>
				</form>
			</div>
		`;
	};

	const handleRegistration = async (e) => {
		e.preventDefault();
		const username = document.querySelector('#username').value;
		const email = document.querySelector('#email').value;
		const password = document.querySelector('#password').value;

		localStorage.setItem('user', JSON.stringify({ username, email, password }));
		navigateTo('/play');
	};

	render();
	document
		.querySelector('#register-form')
		.addEventListener('submit', handleRegistration);
};
