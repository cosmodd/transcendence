<script lang="ts">
	import { logout } from "$lib/stores/auth";
	import { user } from "$lib/stores/user";
	import { goto } from "$app/navigation";
	import defaultAvatar from "$lib/assets/images/default.jpg";
	import NavLink from "$lib/components/NavLink.svelte";
	import Fa from "svelte-fa";
	import { faBell, faTableTennisPaddleBall } from "@fortawesome/free-solid-svg-icons";

	function logoutButton() {
		logout();
		goto("/login");
	}
</script>

<div class="container-fluid d-flex flex-column vh-100">
	<nav class="navbar navbar-expand mb-2">
		<div class="container">
			<a href="/" class="navbar-brand col-2 fw-bold">
				<Fa icon={faTableTennisPaddleBall} />
				Transcendence
			</a>
			<ul class="navbar-nav justify-content-center update-active">
				<li class="nav-item">
					<NavLink href="/play">Play</NavLink>
				</li>
				<li class="nav-item">
					<NavLink href="/friends">Friends</NavLink>
				</li>
			</ul>
			<div class="d-flex justify-content-end col-2">
				<!-- TODO: Implement a search feature to find people's profile -->
				<!-- <form class="d-flex gap" role="search">
					<input
						class="form-control"
						type="search"
						placeholder="Search"
						aria-label="Search"
					/>
				</form> -->
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
	<main id="root" class="container overflow-y-auto p-0 mb-3 h-100">
		<slot />
	</main>
</div>
