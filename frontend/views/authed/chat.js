export default function chat(container, urlParams) {

	const render = () => {
		container.innerHTML = /*html*/ `
			<div class="container h-100">
				<div class="row gap-3 h-100">
					<div class="card col h-100 border-0">

					</div>
					<div class="card col-9 h-100 border-0">
						
					</div>
				</div>
			</div>
		`;
	}

	render();
}