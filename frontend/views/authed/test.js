export default (container, urlParams) => {

	// Test page that lists all the url paramters
	const render = () => {

		container.innerHTML = /*html*/ `
			<div class="d-flex flex-column justify-content-center align-items-center h-100">
				<h1 class="h3 fw-normal">URL Parameters</h1>
				<ul>
					${Object.entries(urlParams)
						.map(([key, value]) => `<li class="list-group list-group-item">${key}: ${value}</li>`)
						.join('')
					}
				</ul>
			</div>
		`;
	};

	render();
};
