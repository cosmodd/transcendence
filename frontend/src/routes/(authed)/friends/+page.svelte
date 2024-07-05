<script lang="ts">
	import Friend from "$lib/components/friends/Friend.svelte";
	import FriendRequest from "$lib/components/friends/FriendRequest.svelte";
	import { authedFetch } from "$lib/stores/auth";
	import { faFaceFrown, faUserGroup, faUserPlus } from "@fortawesome/free-solid-svg-icons";
	import { onMount } from "svelte";
	import Fa from "svelte-fa";

	let friends: FriendRelationData[] = [];
	let requests: FriendRequestData[] = [];

	async function loadFriendsList() {
		const response = await authedFetch("/api/friends-list/");

		if (!response.ok) return;

		friends = await response.json();
	}

	async function loadFriendRequests() {
		const response = await authedFetch("/api/friend-requests/");

		if (!response.ok) return;

		requests = await response.json();
	}

	function reloadLists() {
		loadFriendsList();
		loadFriendRequests();
	}

	onMount(() => {
		loadFriendsList();
		loadFriendRequests();
	});
</script>

<svelte:window on:wsonlinestatus={() => reloadLists()}/>

<div class="container d-flex flex-column gap-4 h-100">
	{#if requests.length > 0}
		<div class="d-flex flex-column">
			<h4 class="fw-bold mb-3 ms-2">
				<Fa icon={faUserPlus} class="me-1" />
				Friend requests
			</h4>
			<div class="grid-container overflow-y-auto gap-3">
				{#each requests as request}
					<FriendRequest data={request} on:accept={reloadLists} on:reject={reloadLists} />
				{/each}
			</div>
		</div>
	{/if}
	<div class="d-flex flex-column flex-fill">
		<h4 class="fw-bold mb-3 ms-2">
			<Fa icon={faUserGroup} class="me-1" />
			Your friends
		</h4>
		{#if friends.length > 0}
			<div class="grid-container overflow-y-auto gap-3">
				{#each friends as relation}
					<Friend data={relation} on:remove={loadFriendsList} />
				{/each}
			</div>
		{:else}
			<div class="d-flex justify-content-center align-items-center flex-fill">
				<h4 class="text-muted">
					It's empty here...
					<Fa icon={faFaceFrown} class="ms-1" />
				</h4>
			</div>
		{/if}
	</div>
</div>

<style>
	.grid-container {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
		grid-auto-rows: min-content;
	}
</style>
