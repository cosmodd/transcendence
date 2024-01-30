export default (container, err) => {
	const render = () => {
		container.innerHTML = `
		<div class="d-flex flex-column justify-content-center align-items-center h-100">
			<h1 class="mt-3">Something went wrong 😟</h1>
			<p>Sorry, something went wrong. Please try again later.</p>
			<pre class="bg-danger px-3 py-2 rounded">${err}</pre>
		</div>
		`;
	};

	render();
};
