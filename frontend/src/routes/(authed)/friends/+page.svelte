<script lang="ts">
	import UserSelect from "$lib/components/chat/UserSelect.svelte";
	import Message from "$lib/components/chat/Message.svelte";
	import GameInvite from "$lib/components/chat/GameInvite.svelte";
	import { user } from "$lib/stores/user";
	import { onMount } from "svelte";
    import { authedFetch } from "$lib/stores/auth";

	//	******************************************************************************************************	//
	//													Notes													//
	//	******************************************************************************************************	//
	// DONT REMOVE THIS NOTES THX - mzaraa
	// Part 1
	// when coming in this page, fetch the list of conversations so i will receive : 
	// list_conversation = { 
	// 						"room_name" : "room_name", 
	// 						"last_message" : "last_message", 
	// 						"last_message_sender" : "last_message_sender",
	// 						"chatting_with" : "chatting_with" }
	
	// Part 2
	// then i will display the list of conversations in the left side of the screen
	// when i click on a conversation, i will display the messages of this conversation in the right side of the screen
	// i will use the UserSelect component to display the list of conversations in the left side of the screen
	// if no conversation is available, i will display a message that no conversation is available
	
	// Part 3
	// to display the conversation selected, i will use the variable selected_conversation that will fetch the conversation using the list_conversation.room_name
	// then i will display the messages of this conversation in the right side of the screen
	// if no user is selected, i will display a message that no user is selected
	// and if no conversation is available, i will display a message that no conversation is available

	// Part 4
	// after all of this setup, i will implement the send message functionality and the receive message functionality using the websocket from ws


	//	******************************************************************************************************	//
	//													Code													//
	//	******************************************************************************************************	//

	let list_conversation : any = {"info" : "No conversation available"};
	let selected_conversation : any = {"info" : "No conversation selected"};

	//	******************************************************************************************************	//
	//													Part 1													//
	//	******************************************************************************************************	//
	async function loadConversationList() {
		console.log("Loading conversation list");
		const response = await authedFetch("/api/list_conversation/").catch(_ => null);
		const data = await response?.json().catch(_ => null);
		console.log(data);
		if (data) {
			if (data.info) {
				console.log(data.info);
			} else {
				list_conversation = data;
				console.log("Conversation list loaded");
			}
		} else {
			console.log("Failed to load conversation list");
		}
	}
	loadConversationList();

	//	******************************************************************************************************	//
	//													Part 3													//
	//	******************************************************************************************************	//
	$: if (selected) {
		async function loadConversationMessages() {
			console.log("Loading conversation messages");
			const response = await authedFetch("/api/room_messages/" + list_conversation.find((x: { chatting_with: string; }) => x.chatting_with == selected).room_name).catch(_ => null);
			const data = await response?.json().catch(_ => null);
			console.log(data);
			if (data) {
				if (data.info) {
					console.log(data.info);
				} else {
					selected_conversation = data;
					console.log("Conversation messages loaded");
				}
			} else {
				console.log("Failed to load conversation messages");
			}
		}
		loadConversationMessages();
	}

	const usernames = ["Sarah", "David", "Emma", "Michael"];

	let selected = "";

	$: messages = selected_conversation.map((x: { sender: string; message: string; }) => {
							return {
								username: x.sender,
								message: x.message,
							};
						});

	//	******************************************************************************************************	//
	//													Part 4													//
	//	******************************************************************************************************	//



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
		{#if list_conversation.info}
			<div class="d-flex justify-content-center align-items-center h-100">
				<h2>{list_conversation.info}</h2>
			</div>
		{:else}
			{#each usernames as username}
				<UserSelect {username} bind:selected on:select={scrollDownMessages} />
			{/each}
		{/if}
	</div>
	<div class="col card border-2 p-3 h-100" id="chat">
		{#if selected_conversation}
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
		{:else}
			<div class="d-flex justify-content-center align-items-center h-100">
				<h2>No conversation selected</h2>
			</div>
		{/if}
	</div>
</div>
