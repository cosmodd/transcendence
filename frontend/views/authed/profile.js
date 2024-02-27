export default function profilePage(container, params) {

	// Temporary solution
	const user = JSON.parse(localStorage.getItem('user'));

	// TODO: Fetch user data from the server
	const currentDate = new Date();
	const gameDatas = Array.from({ length: 20 }, () => ({
		scores: [
			{ username: user.username, score: Math.floor(Math.random() * 100) },
			{ username: "random", score: Math.floor(Math.random() * 100) },
		],
		date: new Date(currentDate.getTime() - Math.floor(Math.random() * 1000 * 60 * 60 * 24 * 30)).toISOString()
	})).sort((a, b) => new Date(b.date) - new Date(a.date));

	const render = () => {

		container.innerHTML = /*html*/ `
			<div class="container gap-3 pb-3 h-100">
				<div class="row gap-3 h-100">
					<div class="col-3 card border-2 p-4 gap-3">
						<div class="d-flex flex-column align-items-center">
							<img src="/assets/avatars/default.jpg" class="rounded-circle" alt="Profile Picture" style="width: 100px; height: 100px;">
							<h3 class="m-0 mt-2 fw-bold">${user.username}</h3>
							<p class="m-0 text-muted">@${user.username}</p>
							<p class="m-0 text-muted">Offline</p>
						</div>
						<hr class="m-0">
						<div class="d-flex flex-column gap-2">
							<h5>Statistics</h5>
							<div class="d-flex justify-content-between">
								<div class="col d-flex gap-2 align-items-center">
									<i class="fa-solid fa-fw fa-gamepad"></i>
									<p class="m-0">Games Played</p>
								</div>
								<p class="m-0">${Math.floor(Math.random() * 100)}</p>
							</div>
							<div class="d-flex justify-content-between">
								<div class="col d-flex gap-2 align-items-center">
									<i class="fa-solid fa-fw fa-trophy"></i>
									<p class="m-0">Wins</p>
								</div>
								<p class="m-0">${Math.floor(Math.random() * 100)}</p>
							</div>
							<div class="d-flex justify-content-between">
								<div class="col d-flex gap-2 align-items-center">
									<i class="fa-solid fa-fw fa-face-frown"></i>
									<p class="m-0">Losses</p>
								</div>
								<p class="m-0">${Math.floor(Math.random() * 100)}</p>
							</div>
						</div>
						<div class="buttons d-flex flex-column gap-2 align-items-center mt-auto">
							<button class="btn btn-success w-100"><i class="fa-solid fa-fw fa-user-plus me-1"></i> Add friend</button>
							<button class="btn btn-primary w-100"><i class="fa-solid fa-fw fa-message me-1"></i> Message</button>
							<button class="btn btn-danger w-100"><i class="fa-solid fa-fw fa-ban me-1"></i> Block</button>
						</div>
					</div>
					<div class="col card border-2 h-100 p-0">
						<h1 class="h3 fw-bold p-3 m-0">Games</h1>
						<div class="container-fluid overflow-y-scroll" id="games"></div>
					</div>
				</div>
			</div>
		`;

	};

	const populateGames = () => {
		const gamesContainer = container.querySelector('#games');

		for (const game of gameDatas) {
			const scores = [
				game.scores.find(score => score.username === user.username),
				game.scores.find(score => score.username !== user.username)
			];
			const hasWon = game.scores.sort((a, b) => b.score - a.score)[0].username === user.username;

			const date = new Date(game.date);
			const dateString = date.toLocaleDateString('fr-FR');

			const gameElement = document.createElement('div');
			gameElement.classList.add(...(`gap-3 p-3 border-start mb-1 border-3 border-${hasWon ? "success" : "danger"}`.split(/\s+/g)));
			if (hasWon) gameElement.style.background = "linear-gradient(90deg, rgba(var(--bs-success-rgb), .2) 0%, transparent 10%)";

			gameElement.innerHTML = /*html*/ `
				<div class="d-flex justify-content-between align-items-center">
					<div class="scores d-flex flex-row gap-2">
						<p class="text-muted m-0">${scores[0].username}</p>
						<p class="${hasWon ? "text-success" : "text-danger"} fw-bold m-0">${scores[0].score}</p>
						:
						<p class="${!hasWon ? "text-success" : "text-danger"} fw-bold m-0">${scores[1].score}</p>
						<p class="text-muted m-0">${scores[1].username}</p>
					</div>
					<p class="m-0 text-muted">${dateString}</p>
				</div>
			`;

			gamesContainer.appendChild(gameElement);
		}
	}

	render();
	populateGames();
}