export default function testPage(container, urlParams) {

	const render = () => {
		container.innerHTML = /*html*/ `
			<div class="card p-3 d-flex flex-column gap-3 overflow-y-auto h-100">
				${Array.from({ length: 20 }, () => {
					return /*html*/ `
						<div class="card p-3">
							<h5 class="card-title">Card title</h5>
							<p class="card-text">This is a longer card with supporting text below as a natural lead-in to additional content. This content is a little bit longer.</p>
							<p class="card-text"><small class="text-muted">Last updated 3 mins ago</small></p>
						</div>
					`;
				}).join("")}
			</div>
		`;
	};

	render();
};
