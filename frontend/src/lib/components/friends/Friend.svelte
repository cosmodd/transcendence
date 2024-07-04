<script lang="ts">
	import { authedFetch } from "$lib/stores/auth";
	import toasts from "$lib/stores/toasts";
	import { faMessage, faUserMinus } from "@fortawesome/free-solid-svg-icons";
	import Fa from "svelte-fa";
	import Avatar from "../Avatar.svelte";
    import { createEventDispatcher } from "svelte";
    import { goto } from "$app/navigation";

	const dispatch = createEventDispatcher();

	export let data: FriendRelationData;
	$: friend = data.friend;

	async function sendMessage() {
		const response = await authedFetch(`/api/chat/${friend.username}/`);

		if (!response.ok) {
			const json = await response.json();
			toasts.error({
				description: json.error,
				duration: 5000,
			});
			return;
		}

		goto(`/chat/`);
	}

	async function unfriend() {
		const response = await authedFetch("/api/remove-friend/", {
			method: "DELETE",
			body: JSON.stringify({
				username: friend.username,
			})
		});

		if (!response.ok) {
			const json = await response.json();
			toasts.error({
				description: json.error,
				duration: 5000,
			});
			return;
		}

		toasts.success({
			description: "Friend removed!",
			duration: 5000,
		});

		dispatch('remove');
	}
</script>

<div class="friend-card card d-inline-flex flex-row border-2 gap-3 p-3 align-items-center">
	<Avatar src={friend.profile_image} size={48} showStatus online={friend.is_online} />
	<div class="d-flex flex-column overflow-hidden">
		<a
			class="user-link fw-bold fs-5 text-truncate text-reset text-decoration-none"
			href="/profile/{friend.username}"
		>
			{friend.display_name}
		</a>
		<span class="text-muted text-truncate">@{friend.username}</span>
	</div>
	<div class="actions d-flex flex-row gap-1 ms-auto">
		<button class="btn btn-primary btn-sm" on:click={sendMessage}><Fa icon={faMessage} /></button>
		<button class="btn btn-danger btn-sm" on:click={unfriend}><Fa icon={faUserMinus} /></button>
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
