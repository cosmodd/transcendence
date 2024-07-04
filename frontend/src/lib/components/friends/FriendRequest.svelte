<script lang="ts">
	import { authedFetch } from "$lib/stores/auth";
	import toasts from "$lib/stores/toasts";
	import { faCheck, faXmark } from "@fortawesome/free-solid-svg-icons";
	import { createEventDispatcher } from "svelte";
	import Fa from "svelte-fa";
	import Avatar from "../Avatar.svelte";
	
	export let data: FriendRequestData;
	$: fromUser = data.from_user;

	const dispatch = createEventDispatcher();

	async function accept() {
		const response = await authedFetch('/api/accept-friend-request/', {
			method: 'PUT',
			body: JSON.stringify({
				username: fromUser?.username,
			})
		});

		if (!response.ok) {
			toasts.error({
				description: `Failed to accept friend request: ${await response.text()}`,
			});
			return;
		}

		toasts.success({
			description: `${fromUser?.display_name} is now your friend!`,
		});

		dispatch('accept', fromUser);
	}
	
	async function decline() {
		const response = await authedFetch('/api/reject-friend-request/', {
			method: 'DELETE',
			body: JSON.stringify({
				username: fromUser?.username,
			})
		});

		if (!response.ok) {
			toasts.error({
				description: `Failed to decline friend request: ${await response.text()}`,
			});
			return;
		}

		toasts.success({
			description: `Declined friend request from ${fromUser?.display_name}`,
		});

		dispatch('decline', fromUser);
	}
</script>

<div class="friend-card card d-inline-flex flex-row border-2 gap-3 p-3 align-items-center">
	<Avatar src={fromUser?.profile_image} size={48} showStatus online={fromUser?.is_online} />
	<div class="d-flex flex-column overflow-hidden">
		<a
			class="user-link fw-bold fs-5 text-truncate text-reset text-decoration-none"
			href="/profile/{fromUser?.username}"
		>
			{fromUser?.display_name}
		</a>
		<span class="text-muted text-truncate">@{fromUser?.username}</span>
	</div>
	<div class="actions d-flex flex-row gap-1 ms-auto">
		<button class="btn btn-success btn-sm" on:click={accept}><Fa icon={faCheck} /></button>
		<button class="btn btn-danger btn-sm" on:click={decline}><Fa icon={faXmark} /></button>
	</div>
</div>

<style>
	.friend-card {
		transition: background 0.1s ease-in-out;
	}

	.friend-card:hover {
		background-color: rgba(255, 255, 255, 0.1);
	}

	.user-link:hover {
		text-decoration: underline !important;
	}
</style>
