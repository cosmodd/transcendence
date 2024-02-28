export default function settingsPage(container, urlParams) {
	const settingsPages = {
	}

	let currentSettingsPage = Object.keys(settingsPages)[0];

	const render = () => {
		container.innerHTML = /*html*/ `
			<div class="container gap-3 h-100">
				<div class="row gap-3 h-100">
					<div class="col-3 card border-2 p-2 gap-1" id="navigation">
						${Object.keys(settingsPages).map(page => /*html*/ `
							<button class="btn btn-dark ${currentSettingsPage == page ? 'active' : ''}">${settingsPages[page].name}</button>
						`).join('')}
					</div>
					<div class="col card border-2 p-2 gap-1">
						<h3 class="fw-bold p-2 m-0">Settings</h3>
						<hr class="m-0 ms-2 me-2">
						<form class="p-2">
						</form>
					</div>
				</div>
			</div>
		`;
	}

	render();
}