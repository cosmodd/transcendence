export default (container) => {
	// Play page for Pong
	// This page will display the different game modes available to the user
	// The user will be able to click on a game mode card to start a game
	// The game mode cards will be displayed in a grid
	// The game mode cards will contain the following information:
	// - A title: gamemode name
	// - A description: a brief description of the game mode
	// - A thumbnail: a visual representation of the game mode
	// - A button: to start the game
	// - A gradient background: to make the card more visually appealing

	const render = () => {
		container.innerHTML = /*html*/ `
		<div class="container gap-3">
			<div class="row gap-3">
				<div class="col card d-flex flex-column p-3 bg-primary bg-gradient" style="flex: 1 1;">
					<div class="card-body d-flex flex-column">
						<h2 class="card-title fw-bold">Singleplayer</h2>
						<p class="card-text">
							The classic game mode where you play against a computer
						</p>
						<button class="btn btn-dark mt-auto">Play</button>
					</div>
				</div>
				<div class="col card d-flex flex-column p-3 bg-success bg-gradient" style="flex: 1 1;">
					<div class="card-body d-flex flex-column">
						<h2 class="card-title fw-bold">Multiplayer</h2>
						<p class="card-text">
							Play against other players in real-time
						</p>
						<button class="btn btn-dark mt-auto">Play</button>
					</div>
				</div>
				<div class="col card d-flex flex-column p-3 bg-danger bg-gradient" style="flex: 1 1;">
					<div class="card-body d-flex flex-column">
						<h2 class="card-title fw-bold">Ranked</h2>
						<p class="card-text">
							Compete against other players to climb the leaderboard
						</p>
						<button class="btn btn-dark mt-auto">Play</button>
					</div>
				</div>
			</div>
		</div>
		`;
	};

	render();
};
