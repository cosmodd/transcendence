<script lang="ts">
	import { goto } from "$app/navigation";
	import Avatar from "$lib/components/Avatar.svelte";
	import NavLink from "$lib/components/NavLink.svelte";
	import ToastContainer from "$lib/components/toasts/ToastContainer.svelte";
	import { logout } from "$lib/stores/auth";
	import toasts from "$lib/stores/toasts";
	import { user } from "$lib/stores/user";
	import { faTableTennisPaddleBall } from "@fortawesome/free-solid-svg-icons";
	import Fa from "svelte-fa";

	function logoutButton() {
		logout();
		goto("/login");
	}

	function handleNotifications(event: CustomEvent<any>) {
		const data = event.detail;

		console.log("Received notification : ", data);

		const message = data.sender === "system" ? data.message : "Join the game!";

		toasts.add({
			type: "info",
			title: "Tournament",
			description: message,
			buttons: [
				{
					label: "Go to match!",
					action: async () => {
						await goto("/");
						await goto("/game/online/");
					},
					dismiss: true,
				},
			],
			duration: 30_000, // Refer to .\backend\websockets\pong_server\gamelogic.py
		});
	}
</script>

<svelte:window on:notification={handleNotifications} />

<ToastContainer />

<div class="container-fluid d-flex flex-column vh-100">
	<nav class="navbar navbar-expand mb-2">
		<div class="container">
			<a href="/" class="navbar-brand col-2 fw-bold">
				<Fa icon={faTableTennisPaddleBall} />
				Transcendence
			</a>
			<ul class="navbar-nav justify-content-center update-active">
				<li class="nav-item">
					<NavLink href="/" strict>Play</NavLink>
				</li>
				<li class="nav-item">
					<NavLink href="/chat">Chat</NavLink>
				</li>
				<li class="nav-item">
					<NavLink href="/friends">Friends</NavLink>
				</li>
			</ul>
			<div class="d-flex justify-content-end col-2">
				<div class="dropdown profile">
					<button
						type="button"
						data-bs-toggle="dropdown"
						class="text-decoration-none text-reset d-flex align-items-center gap-2 fw-bold bg-transparent border-0"
					>
						{$user.display_name}
						<Avatar src={$user.profile_image} size={32} />
					</button>
					<ul class="dropdown-menu dropdown-menu-end mt-2">
						<li>
							<a class="dropdown-item" href="/profile">Profile</a>
						</li>
						<li>
							<a class="dropdown-item" href="/settings">Settings</a>
						</li>
						<div class="dropdown-divider"></div>
						<li>
							<button
								type="button"
								class="dropdown-item text-danger"
								on:click={logoutButton}
								aria-label="Logout"
							>
								Logout
							</button>
						</li>
					</ul>
				</div>
			</div>
		</div>
	</nav>
	<main id="root" class="container overflow-y-auto p-0 mb-3 h-100 d-flex flex-column">
		<slot />
	</main>
</div>
