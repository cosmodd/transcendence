export default function profilePage(container, {}) {

	const user = JSON.parse(localStorage.getItem('user'));

	const render = () => {

		container.innerHTML = /*html*/ `
			<div class="d-flex flex-column justify-content-center align-items-center h-100">
				<h1 class="h3 fw-normal">Profile</h1>
				<ul>
					<li class="list-group list-group-item">Username: ${user.username}</li>
					<li class="list-group list-group-item">Email: ${user.email}</li>
				</ul>
			</div>
		`;

	};

	render();
}