<script lang="ts">
	import UserSelect from "$lib/components/chat/UserSelect.svelte";
	import Message from "$lib/components/chat/Message.svelte";
	import GameInvite from "$lib/components/chat/GameInvite.svelte";
	import { user } from "$lib/stores/user";
	import { onMount, tick } from "svelte";
    import { authedFetch } from "$lib/stores/auth";
	import { sendMessage, sendInvitation } from "$lib/stores/websocket";
	import type { Conversation, ChatMessage } from "$lib/stores/websocket";

	//	******************************************************************************************************	//
	//													Code													//
	//	******************************************************************************************************	//

	
	let list_conversation = new Map<string, Conversation>();
	let current_messages : ChatMessage[] = [];
	let selected_conversation : Conversation | null = null;
	let new_message : string = "";
	let messages_container : HTMLDivElement;

	//	******************************************************************************************************	//
	//													Part 1													//
	//	******************************************************************************************************	//
	async function loadConversationList() {
		console.log("Loading conversation list");
		const response = await authedFetch("/api/list_conversation/").catch(_ => null);
		const data = await response?.json().catch(_ => null);
		//console.log(data);
		if (data) {
			for (let element of data) {
				list_conversation.set(element.room_name, element);
			}
			list_conversation = list_conversation;
			console.log("date of this pc", new Date());
			console.log("Conversation list loaded", list_conversation);
		} else {
			console.log("Failed to load conversation list");
		}
	}
	loadConversationList();

	//	******************************************************************************************************	//
	//													Part 3													//
	//	******************************************************************************************************	//
	async function loadConversationMessages() {
		console.log("Loading conversation messages");
		let room_name = selected_conversation?.room_name;
		console.log("room :",room_name);
		if (!room_name)
			return;
		//console.log("room :",room_name);
		//console.log("selected :",selected);
		//console.log("list conversation :",list_conversation);
		const response = await authedFetch("/api/room_messages/" + room_name + '/' ).catch(_ => null);
		const data = await response?.json().catch(_ => null);
		//console.log(data);
		if (data) {
			if (data.info) {
				console.log(data.info);
			} else {
				current_messages = data;
				console.log("Conversation messages loaded", current_messages);
			}
		} else {
			console.log("Failed to load conversation messages", data);
		}
		await tick();
		scrollDownMessages();
	}

	$: if (selected_conversation) {
		loadConversationMessages();
	}

	// $: messages = selected_conversation.map(
	// 	(x: { sender: string; message: string; room_name: string }) => {
	// 		return { 
	// 			username: x.sender,
	// 			message: x.message,
	// 			room_name: x.room_name
	// 		};
	// 	});
	
	

	//	******************************************************************************************************	//
	//													Part 4													//
	//	******************************************************************************************************	//
	
	function handleWsMessage() {
		if (new_message.trim() !== "") {
			const room_name = selected_conversation?.room_name;
			if (!room_name)
				return;
			sendMessage(new_message, room_name);
			new_message = "";
		}
	}


	function scrollDownMessages() {
		if (messages_container)
			messages_container.scrollTop = messages_container.scrollHeight;
	}

	function check_invit() {
		console.log("check_invit");
		return false;
	}

</script>

<svelte:window on:wsmessage={async (e) => { 
	console.log('DispatchEvent', e);

	list_conversation.set(e.detail.room_name, {
		...(list_conversation.get(e.detail.room_name) ?? { room_name: e.detail.room_name, chatting_with: e.detail.sender}), 
		last_message: e.detail.message,
		last_message_sender: e.detail.sender
	});
	list_conversation = list_conversation;
	if (e.detail.room_name === selected_conversation?.room_name) {
		current_messages = [...current_messages, e.detail];
		if (messages_container.scrollTop >= messages_container.scrollHeight - messages_container.clientHeight - 15) {
			await tick();
			scrollDownMessages();
		}
	}

 }}/>

<div class="row h-100 m-0 gap-3">
	<div class="col-3 p-0 card border-2 d-flex flex-column h-100 overflow-auto" id="users">
		{#if list_conversation.size === 0}
			<div class="d-flex justify-content-center align-items-center h-100">
				<h2>No conversation available</h2>
			</div>
		{:else}
			{#each list_conversation.values() as conversation}
				<UserSelect {conversation} selected={selected_conversation?.room_name == conversation.room_name} on:select={() => { selected_conversation = conversation; }} />
			{/each}
		{/if}
	</div>
	<div class="col card border-2 p-3 h-100" id="chat">
		{#if selected_conversation !== null}
			<div class="header d-flex justify-content-between">
				<div class="user d-flex flex-row align-items-center gap-3">
					<img
						src="https://via.placeholder.com/128"
						class="rounded-circle"
						style="width: 48px; height: 48px"
						alt=""
					/>
					<h2 class="m-0 fw-bold">{selected_conversation.chatting_with}</h2>
					<span class="mt-2 badge rounded-pill bg-success">Online</span>
					<button type="button" class="btn btn-primary" on:click={() => { 
						//send message with type_message = 'invitation'
						const room_name = selected_conversation?.room_name;
						if (!room_name)
							return;
						sendInvitation('invitation', room_name);
					 }}>
						Invite to a game
				</div>
			</div>
			<hr />
			<div bind:this={messages_container} id="messages" class="overflow-auto d-flex flex-column gap-3">
				{#if current_messages.length === 0}
					<div class="d-flex justify-content-center align-items-center h-100">
						<h2>No messages available</h2>
					</div>
				{:else}
					{#each current_messages as message}
						{#if message.message_type === 'invitation'}
							<GameInvite game_type='casual' self={message.sender !== selected_conversation.chatting_with} invitation_date={message.timestamp} is_accepted={message.is_accepted} room_name={message.room_name} />
						{:else}
							<Message message={message.message} self={message.sender !== selected_conversation.chatting_with} />
						{/if}
					{/each}
					<!-- {#each $wsMessages as message}
						{#if message.room_name === selected_conversation.room_name}
							<Message message={message.message} self={message.sender !== selected} />
						{/if}
					{/each} -->
				{/if}
			</div>
			<form>
				<div class="input-group mt-3">
					<input
						type="text"
						class="form-control"
						placeholder="Enter message"
						aria-label="Enter message"
						aria-describedby="basic-addon2"
						bind:value={new_message}
						on:keyup={e => { if (e.key === "Enter") handleWsMessage(); }}
					/>
					<div class="input-group-append">
						<button class="btn btn-outline-secondary" type="button" on:click={handleWsMessage}>Send</button>
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
