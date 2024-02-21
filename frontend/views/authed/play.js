export default (container) => {
	const render = () => {
		container.innerHTML = /*html*/ `
		<div class="container gap-3">
			<div class="row gap-3">
				<div class="col card d-flex flex-column p-3 bg-primary bg-gradient border-0" style="flex: 1 1;">
					<div class="card-body d-flex flex-column">
						<h2 class="card-title fw-bold text-light">Local</h2>
						<p class="card-text text-light">
							Play against your fake IRL friends
						</p>
						<button class="btn btn-dark mt-auto">Play</button>
					</div>
				</div>
				<div class="col card d-flex flex-column p-3 bg-success bg-gradient border-0" style="flex: 1 1;">
					<div class="card-body d-flex flex-column">
						<h2 class="card-title fw-bold text-light">Multiplayer</h2>
						<p class="card-text text-light">
							Play against other players in real-time
						</p>
						<button class="btn btn-dark mt-auto">Play</button>
					</div>
				</div>
				<div class="col card d-flex flex-column p-3 bg-danger bg-gradient border-0" style="flex: 1 1;">
					<div class="card-body d-flex flex-column">
						<h2 class="card-title fw-bold text-light">Ranked</h2>
						<p class="card-text text-light">
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
