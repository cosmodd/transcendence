<script lang="ts">
	import UserSelect from "$lib/components/chat/UserSelect.svelte";
	import Message from "$lib/components/chat/Message.svelte";
	import GameInvite from "$lib/components/chat/GameInvite.svelte";
	import { user } from "$lib/stores/user";
	import { onMount } from "svelte";
    import { authedFetch } from "$lib/stores/auth";
	
	let list_conversation = {};
	let selected_conversation : string = "";

	async function loadConversationList() {
		console.log("Loading conversation list");
		const response = await authedFetch("/api/list_conversation/").catch(_ => null);
		const data = await response?.json().catch(_ => null);
		console.log(data);
		if (data) {
			list_conversation = data;
		} else {
			console.log("Failed to load conversation list");
		}
	}
	loadConversationList();

	const usernames = ["Sarah", "David", "Emma", "Michael"];

	let selected = "";

	$: messages = [
		{
			username: selected,
			message: "Hello",
		},
		{
			username: $user.username,
			message: "Hi",
		},
		{
			username: selected,
			message: "Hey",
		},
		{
			username: $user.username,
			message: "Yo",
		},
		{
			username: selected,
			message: "Why are you gay?",
		},
		{
			username: $user.username,
			message: "I'm not gay",
		},
		{
			username: selected,
			message:
				"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
		},
		{
			username: selected,
			message:
				"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
		},
		{
			username: $user.username,
			message:
				"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
		},
		{
			username: $user.username,
			message:
				"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
		},
		{
			username: $user.username,
			message:
				"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
		},
		{
			username: $user.username,
			message:
				"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
		},
		{
			username: selected,
			message:
				"I'm creating a tournament later, I'll send you an invite if you're interested!",
		},
	];

	function scrollDownMessages() {
		const element = document.getElementById("messages") as HTMLDivElement;
		element.scrollTop = element.scrollHeight;
	}

	onMount(() => {
		scrollDownMessages();
	});
</script>

<div class="row h-100 m-0 gap-3">
	<div class="col-3 p-0 card border-2 d-flex flex-column h-100 overflow-auto" id="users">
		{#each usernames as username}
			<UserSelect {username} bind:selected on:select={scrollDownMessages} />
		{/each}
	</div>
	<div class="col card border-2 p-3 h-100" id="chat">
		<div class="header d-flex justify-content-between">
			<div class="user d-flex flex-row align-items-center gap-3">
				<img
					src="https://via.placeholder.com/128"
					class="rounded-circle"
					style="width: 48px; height: 48px"
					alt=""
				/>
				<h2 class="m-0 fw-bold">{selected}</h2>
				<span class="mt-2 badge rounded-pill bg-success">Online</span>
			</div>
		</div>
		<hr />
		<div id="messages" class="overflow-auto d-flex flex-column gap-3">
			{#each messages as message}
				<Message message={message.message} self={message.username !== selected} />
			{/each}
			<GameInvite type="tournament" />
			<GameInvite />
			<GameInvite />
		</div>
		<form>
			<div class="input-group mt-3">
				<input
					type="text"
					class="form-control"
					placeholder="Enter message"
					aria-label="Enter message"
					aria-describedby="basic-addon2"
				/>
				<div class="input-group-append">
					<button class="btn btn-outline-secondary" type="button">Send</button>
				</div>
			</div>
		</form>
	</div>
</div>
