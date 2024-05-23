<script lang="ts">
	import { goto } from "$app/navigation";
	import NavLink from "$lib/components/NavLink.svelte";
	import NotificationGame from "$lib/components/notification/NotificationGame.svelte";
	import { logout } from "$lib/stores/auth";
	import { user } from "$lib/stores/user";
	import { faTableTennisPaddleBall } from "@fortawesome/free-solid-svg-icons";
	import Fa from "svelte-fa";

	function logoutButton() {
		logout();
		goto("/login");
	}
</script>

<NotificationGame />

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
						<img
							src={$user.profile_image}
							alt="Avatar"
							class="rounded-circle me-2"
							width="32"
							height="32"
						/>
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
								aria-label="Logout">Logout</button
							>
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
