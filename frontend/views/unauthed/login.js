export default (container) => {
	// Login page
	const render = () => {
		container.innerHTML = `
			<div class="d-flex flex-column justify-content-center align-items-center h-100">
				<form class="card p-5 d-flex flex-column gap-3" id="login-form" style="min-width: 400px;">
					<h1 class="h3 fw-normal">Welcome back!</h1>
					<label for="username" class="visually-hidden">Username</label>
					<input type="text" id="username" class="form-control" placeholder="Username" required autofocus />
					<label for="password" class="visually-hidden">Password</label>
					<input type="password" id="password" class="form-control" placeholder="Password" required />
					<p class="mb-0 text-muted">Don't have an account? <a href="/register">Register</a></p>
					<div class="d-flex flex-column justify-content-center gap-2">
						<button class="btn btn-primary" type="submit">Sign in</button>
						<button type="button" id="intra-login" class="btn bg-black text-white d-flex justify-content-center gap-2">
							<img src="/assets/svg/42.svg" alt="Intra" width="24" height="24" />
							Login with intra
						</button>
					</div>
				</form>
			</div>
		`;
	};

	const handleLogin = async (e) => {
		
	};

	render();
};
