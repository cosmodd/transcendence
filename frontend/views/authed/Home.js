export default (container) => {
	// Home page
	const render = () => {
		container.innerHTML = /*html*/ `
			<h1>Home</h1>
			<p>Welcome to the home page!</p>
		`;
	};

	render();
};
