export default (container, code) => {
	const codes = {
		404: 'Page not found'
	};

	const render = () => {
		container.innerHTML = /*html*/ `
			<div class="d-flex flex-column justify-content-center align-items-center h-100">
				<h1 class="mt-3 fw-bold">Error ${code}</h1>
				<p>${codes[code]}</p>
			</div>
		`;
	};

	render();
};
