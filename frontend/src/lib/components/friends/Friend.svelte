<script lang="ts">
	import { faMessage, faUserPlus } from "@fortawesome/free-solid-svg-icons";
	import Avatar from "../Avatar.svelte";
	import Fa from "svelte-fa";

	export let data: FriendRelationData;
	$: friend = data.friend;

	function sendMessage() {
		// TODO: Implement message sending
		console.log("💬 Redirecting to message page with", friend.username);
	}
	
	function invite() {
		// TODO: Implement inviting
		console.log("🎮 Sending game invitation to", friend.username);
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
		<button class="btn btn-success btn-sm" on:click={invite}><Fa icon={faUserPlus} /></button>
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
