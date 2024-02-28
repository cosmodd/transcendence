export default function settingsPage(container, urlParams) {
	const settingsPages = {
		'account': {
			name: 'Account',
			fields: [
				{
					name: 'Display Name',
					description: 'The name that will be displayed to other users',
				}
			]
		}
	}

	let currentSettingsPage = Object.keys(settingsPages)[0];

	const render = () => {
		const userInformations = JSON.parse(localStorage.getItem('user'));

		container.innerHTML = /*html*/ `
			<div class="container gap-3 h-100">
				<div class="row gap-3 h-100">
					<div class="col-3 card border-2 p-2 gap-1" id="navigation">
						${Object.keys(settingsPages).map(page => /*html*/ `
							<button class="btn btn-dark ${currentSettingsPage == page ? 'active' : ''}">${settingsPages[page].name}</button>
						`).join('')}
					</div>
					<div class="col card border-2 p-2 gap-1">
						<h3 class="fw-bold p-2 m-0">${settingsPages[currentSettingsPage].name} Settings</h3>
						<hr class="m-0 ms-2 me-2">
						<div class="p-2 d-flex flex-column gap-2">
							<div class="field d-flex justify-content-between align-items-center">
								<div class="d-flex flex-column">
									<span class="fw-bold text-muted">Display Name</span>
									<span>${userInformations.displayname}</span>
								</div>
								<button class="btn btn-secondary px-4" data-bs-toggle="modal" data-bs-target="#editDisplayName">Edit</button>
								<div class="modal fade" id="editDisplayName" tabindex="-1" aria-labelledby="editDisplayNameLabel" aria-hidden="true">
									<div class="modal-dialog modal-dialog-centered">
										<div class="modal-content">
											<div class="modal-header">
												<h5 class="modal-title" id="editDisplayNameLabel">Edit Display Name</h5>
												<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
											</div>
											<div class="modal-body d-flex flex-column gap-3">
												<div class="form-floating">
													<input type="text" class="form-control" id="displayName" placeholder="Display Name" value="${userInformations.displayname}">
													<label for="displayName">New Display Name</label>
												</div>
												<button class="btn btn-primary" data-save="displayname">Save</button>
											</div>
										</div>
									</div>
								</div>
							</div>
							<div class="field d-flex justify-content-between align-items-center">
								<div class="d-flex flex-column">
									<span class="fw-bold text-muted">Username</span>
									<span>${userInformations.username}</span>
								</div>
								<button class="btn btn-secondary px-4" data-bs-toggle="modal" data-bs-target="#editUsername">Edit</button>
								<div class="modal fade" id="editUsername" tabindex="-1" aria-labelledby="editUsernameLabel" aria-hidden="true">
									<div class="modal-dialog modal-dialog-centered">
										<div class="modal-content">
											<div class="modal-header">
												<h5 class="modal-title" id="editUsernameLabel">Edit Display Name</h5>
												<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
											</div>
											<div class="modal-body d-flex flex-column gap-3">
												<div class="form-floating">
													<input type="text" class="form-control" id="Username" placeholder="Display Name" value="${userInformations.username}">
													<label for="Username">New Username</label>
												</div>
												<button class="btn btn-primary" data-save="username">Save</button>
											</div>
										</div>
									</div>
								</div>
							</div>
							<div class="field d-flex justify-content-between align-items-center">
								<div class="d-flex flex-column">
									<span class="fw-bold text-muted">Email</span>
									<span>${userInformations.email}</span>
								</div>
								<button class="btn btn-secondary px-4" data-bs-toggle="modal" data-bs-target="#editEmail">Edit</button>
								<div class="modal fade" id="editEmail" tabindex="-1" aria-labelledby="editEmailLabel" aria-hidden="true">
									<div class="modal-dialog modal-dialog-centered">
										<div class="modal-content">
											<div class="modal-header">
												<h5 class="modal-title" id="editEmailLabel">Edit Display Name</h5>
												<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
											</div>
											<div class="modal-body d-flex flex-column gap-3">
												<div class="form-floating">
													<input type="text" class="form-control" id="Email" placeholder="Display Name" value="${userInformations.email}">
													<label for="Email">New Email</label>
												</div>
												<button class="btn btn-primary" data-save="email">Save</button>
											</div>
										</div>
									</div>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>
		`;
	}

	const handleSaves = () => {
		document.querySelectorAll('[data-save]').forEach(button => {
			button.addEventListener('click', (e) => {
				e.preventDefault();
				const modal = button.closest('.modal');
				const field = button.getAttribute('data-save');
				console.log(field, modal.querySelector('input').value);
				localStorage.setItem('user', JSON.stringify({
					...JSON.parse(localStorage.getItem('user')),
					[field]: modal.querySelector('input').value
				}));
				bootstrap.Modal.getInstance(modal).hide();
				updatePage();
			});
		});
	}

	const updatePage = () => {
		render();
		handleSaves();
	}

	updatePage();
}