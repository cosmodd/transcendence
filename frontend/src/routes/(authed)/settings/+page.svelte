<script lang="ts">
	import PasswordField from "$lib/components/auth/PasswordField.svelte";
	import { authedFetch } from "$lib/stores/auth";
	import { user } from "$lib/stores/user";
	import { faPen } from "@fortawesome/free-solid-svg-icons";
	import { Fa } from "svelte-fa";

	let avatarAlert: string = "";
	let displayNameAlert: string = "";
	let passwordAlert: string = "";
	let processing: boolean = false;

	function handleAvatarUpdate(event: SubmitEvent) {
		const target = event.target as HTMLFormElement;
		const data = new FormData(target);

		processing = true;
		authedFetch("/api/profile/update/", {
			method: "PATCH",
			body: data,
		}).then(async (response) => {
			const json = await response.json();
			processing = false;

			if (!response.ok) {
				for (const [key, value] of Object.entries(json)) {
					const field = key.replace(/_/g, " ").replace(/(?<=\b)\w/g, (c) => c.toUpperCase());
					avatarAlert = `${field}: ${value}`;
				}
				return;
			}

			avatarAlert = "";
			if ($user.profile_image !== json.profile_image) $user.profile_image = json.profile_image;
			else fetch($user.profile_image as string);

			// Close modal
			const modalInstance = bootstrap.Modal.getInstance(document.getElementById("avatarModal"));
			if (modalInstance) modalInstance.hide();
		});
	}

	function handleUpdateDisplayName(event: SubmitEvent) {
		const target = event.target as HTMLFormElement;
		const data = new FormData(target);

		processing = true;
		authedFetch("/api/profile/update/", {
			method: "PATCH",
			body: JSON.stringify({ display_name: data.get("displayName") }),
		}).then(async (response) => {
			const json = await response.json();
			processing = false;

			if (!response.ok) {
				for (const [key, value] of Object.entries(json)) {
					const field = key.replace(/_/g, " ").replace(/(?<=\b)\w/g, (c) => c.toUpperCase());
					displayNameAlert = `${field}: ${value}`;
				}
				return;
			}

			displayNameAlert = "";
			$user.display_name = json.display_name;

			// Close modal
			const modalInstance = bootstrap.Modal.getInstance(document.getElementById("displayNameModal"));
			if (modalInstance) modalInstance.hide();
		});
	}

	function handlePasswordUpdate(event: SubmitEvent) {
		const target = event.target as HTMLFormElement;
		const data = new FormData(target);

		processing = true;
		authedFetch("/api/profile/update/", {
			method: "PATCH",
			body: JSON.stringify({
				old_password: data.get("oldPassword"),
				password: data.get("password"),
			}),
		}).then(async (response) => {
			const json = await response.json();
			processing = false;

			if (!response.ok) {
				for (const [key, value] of Object.entries(json)) {
					const field = key.replace(/_/g, " ").replace(/(?<=\b)\w/g, (c) => c.toUpperCase());
					passwordAlert = `${field}: ${value}`;
				}
				return;
			}

			passwordAlert = "";
			const modalInstance = bootstrap.Modal.getInstance(document.getElementById("passwordModal"));
			if (modalInstance) modalInstance.hide();
		});
	}

	function toggle2FA() {
		processing = true;
		authedFetch("/api/profile/update/", {
			method: "PATCH",
			body: JSON.stringify({ enabled_2FA: !$user.enabled_2FA }),
		}).then(async (response) => {
			const json = await response.json();
			processing = false;

			if (!response.ok) {
				console.error(json);
				return;
			}

			$user.enabled_2FA = json.enabled_2FA;
		});
	}
</script>

<div class="settings card border-2 p-3 h-100">
	<h2 class="fw-bold m-0">Settings</h2>
	<hr />
	<div class="settings d-flex flex-column gap-3">
		<div class="setting d-flex flex-row gap-3 w-100 border-bottom align-items-center pb-3">
			<img src={$user.profile_image} alt="profile" class="rounded-circle" style="width: 48px; height: 48px;" />
			<div class="d-flex flex-column flex-grow-1">
				<span class="fw-bold text-capitalize">User avatar</span>
				<p class="text-muted m-0">Change your public profile picture.</p>
			</div>
			<button class="btn btn-secondary px-3" data-bs-toggle="modal" data-bs-target="#avatarModal">Edit</button>
		</div>
		<div class="setting d-flex flex-row gap-3 w-100 border-bottom align-items-center pb-3">
			<div class="d-flex flex-column flex-grow-1">
				<span class="fw-bold text-capitalize">Display name</span>
				<p class="text-muted m-0">Change your username visible to other users.</p>
			</div>
			<button class="btn btn-secondary px-3" data-bs-toggle="modal" data-bs-target="#displayNameModal"
				>Edit</button
			>
		</div>
		<div class="setting d-flex flex-row gap-3 w-100 border-bottom align-items-center pb-3">
			<div class="d-flex flex-column flex-grow-1">
				<span class="fw-bold text-capitalize">Password</span>
				<p class="text-muted m-0">Change your password.</p>
			</div>
			<button class="btn btn-secondary px-3" data-bs-toggle="modal" data-bs-target="#passwordModal">Edit</button>
		</div>
		<div class="setting d-flex flex-row gap-1 w-100 border-bottom align-items-center pb-3">
			<div class="d-flex flex-column flex-grow-1">
				<span class="fw-bold text-capitalize">Double Factor Authentication</span>
				<p class="text-muted m-0">Enable or disable 2FA via applications.</p>
			</div>
			{#if processing}
				<div class="spinner-border spinner-grow-sm spinner-border-sm" role="status">
					<span class="visually-hidden">Loading...</span>
				</div>
			{/if}
			{#if $user.enabled_2FA}
				<button class="btn btn-danger px-3" on:click={toggle2FA}>Disable</button>
				<button class="btn btn-primary px-3" data-bs-toggle="modal" data-bs-target="#qrModal">
					Show QR code
				</button>
			{:else}
				<button class="btn btn-success px-3" on:click={toggle2FA}>Enable</button>
			{/if}
		</div>
	</div>
</div>

<!-- User avatar modal -->
<div class="modal fade" id="avatarModal" tabindex="-1" aria-labelledby="avatarModalLabel" aria-hidden="true">
	<div class="modal-dialog modal-dialog-centered">
		<div class="modal-content">
			<div class="modal-header">
				<h5 class="modal-title" id="avatarModalLabel">User avatar</h5>
				<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" />
			</div>
			<div class="modal-body p-4">
				{#if avatarAlert}
					<div class="alert alert-danger" role="alert">{avatarAlert}</div>
				{/if}
				<form action="#" enctype="multipart/form-data" on:submit|preventDefault={handleAvatarUpdate}>
					<div class="mb-3">
						<label for="avatar" class="form-label visually-hidden">Upload new avatar</label>
						<input type="file" class="form-control" id="avatar" name="profile_image" required />
					</div>
					<button
						type="submit"
						class="btn btn-primary d-flex flex-row gap-2 align-items-center fw-bold w-100 justify-content-center"
					>
						{#if processing}
							<div class="spinner-border spinner-border-sm spinner-grow-sm" role="status">
								<span class="visually-hidden">Loading...</span>
							</div>
						{:else}
							<Fa icon={faPen} />
						{/if}
						Update
					</button>
				</form>
			</div>
		</div>
	</div>
</div>

<!-- Display name modal -->
<div class="modal fade" id="displayNameModal" tabindex="-1" aria-labelledby="displayNameModalLabel" aria-hidden="true">
	<div class="modal-dialog modal-dialog-centered">
		<div class="modal-content">
			<div class="modal-header">
				<h5 class="modal-title" id="displayNameModalLabel">Display name</h5>
				<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" />
			</div>
			<div class="modal-body p-4">
				{#if displayNameAlert}
					<div class="alert alert-danger" role="alert">{displayNameAlert}</div>
				{/if}
				<form action="#" on:submit|preventDefault={handleUpdateDisplayName}>
					<div class="mb-3">
						<label for="displayName" class="form-label visually-hidden">Display name</label>
						<input
							type="text"
							class="form-control"
							id="displayName"
							name="displayName"
							value={$user.display_name}
							required
							maxlength="32"
							minlength="2"
						/>
					</div>
					<button
						type="submit"
						class="btn btn-primary d-flex flex-row gap-2 align-items-center fw-bold w-100 justify-content-center"
					>
						{#if processing}
							<div class="spinner-border spinner-border-sm spinner-grow-sm" role="status">
								<span class="visually-hidden">Loading...</span>
							</div>
						{:else}
							<Fa icon={faPen} />
						{/if}
						Update
					</button>
				</form>
			</div>
		</div>
	</div>
</div>

<!-- Password modal -->
<div class="modal fade" id="passwordModal" tabindex="-1" aria-labelledby="passwordModalLabel" aria-hidden="true">
	<div class="modal-dialog modal-dialog-centered">
		<div class="modal-content">
			<div class="modal-header">
				<h5 class="modal-title" id="passwordModalLabel">Password</h5>
				<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" />
			</div>
			<div class="modal-body p-4">
				{#if passwordAlert}
					<div class="alert alert-danger" role="alert">{passwordAlert}</div>
				{/if}
				<form action="#" on:submit|preventDefault={handlePasswordUpdate} class="d-flex flex-column gap-3">
					<PasswordField askOld />
					<button
						type="submit"
						class="btn btn-primary d-flex flex-row gap-2 align-items-center fw-bold w-100 justify-content-center"
					>
						{#if processing}
							<div class="spinner-border spinner-border-sm spinner-grow-sm" role="status">
								<span class="visually-hidden">Loading...</span>
							</div>
						{:else}
							<Fa icon={faPen} />
						{/if}
						Update
					</button>
				</form>
			</div>
		</div>
	</div>
</div>

<!-- QR modal -->
{#if $user.enabled_2FA}
	<div class="modal fade" id="qrModal" tabindex="-1" aria-labelledby="qrModalLabel" aria-hidden="true">
		<div class="modal-dialog modal-dialog-centered">
			<div class="modal-content">
				<div class="modal-header">
					<h5 class="modal-title" id="qrModalLabel">QR code</h5>
					<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" />
				</div>
				<div class="modal-body p-4">
					<div class="d-flex flex-column align-items-center">
						<img
							src={$user.qrcode_2FA}
							alt="qrcode"
							class="img-fluid rounded"
							style="width: 256px; height: 256px;"
						/>
					</div>
				</div>
			</div>
		</div>
	</div>
{/if}
