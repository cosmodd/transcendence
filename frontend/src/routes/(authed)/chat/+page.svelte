<script lang="ts">
	import Avatar from "$lib/components/Avatar.svelte";
	import GameInvite from "$lib/components/chat/GameInvite.svelte";
	import Message from "$lib/components/chat/Message.svelte";
	import UserSelect from "$lib/components/chat/UserSelect.svelte";
	import { authedFetch } from "$lib/stores/auth";
	import type { ChatMessage, Conversation } from "$lib/stores/websocket";
	import { sendInvitation, sendMessage } from "$lib/stores/websocket";
    import { faUserPlus } from "@fortawesome/free-solid-svg-icons";
	import { tick } from "svelte";
    import Fa from "svelte-fa";

	//	******************************************************************************************************	//
	//													Code													//
	//	******************************************************************************************************	//

	let list_conversation = new Map<string, Conversation>();
	let current_messages: ChatMessage[] = [];
	let selected_conversation: Conversation | null = null;
	let new_message: string = "";
	let messages_container: HTMLDivElement;
	let online_status: boolean = false;

	//	******************************************************************************************************	//
	//													Part 1													//
	//	******************************************************************************************************	//
	async function loadConversationList() {
		console.log("Loading conversation list");
		const response = await authedFetch("/api/list_conversation/").catch((_) => null);
		const data = await response?.json().catch((_) => null);
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
		console.log("room :", room_name);
		if (!room_name) return;
		//console.log("room :",room_name);
		//console.log("selected :",selected);
		//console.log("list conversation :",list_conversation);
		const response = await authedFetch("/api/room_messages/" + room_name + "/").catch((_) => null);
		const data = await response?.json().catch((_) => null);
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

	//	******************************************************************************************************	//
	//													Part 4													//
	//	******************************************************************************************************	//

	function handleWsMessage() {
		if (new_message.trim() !== "") {
			const room_name = selected_conversation?.room_name;
			if (!room_name) return;
			sendMessage(new_message, room_name);
			new_message = "";
		}
	}

	function scrollDownMessages() {
		if (messages_container) messages_container.scrollTop = messages_container.scrollHeight;
	}
</script>

<svelte:window
	on:wsmessage={async (event) => {
		console.log("DispatchEvent", event);

		const details = event.detail;

		list_conversation.set(details.room_name, {
			...(list_conversation.get(details.room_name) ?? {
				room_name: details.room_name,
				chatting_with: details.sender,
			}),
			last_message: details.message,
			last_message_sender: details.sender,
		});
		list_conversation = list_conversation;

		if (details.room_name === selected_conversation?.room_name) {
			current_messages = [...current_messages, event.detail];
			await tick();
			scrollDownMessages();
		}
	}}
	on:wsonlinestatus={async (e) => {
		console.log("OnlineStatus", e.detail);
		online_status = e.detail;
	}}
/>

<div class="row h-100 m-0 gap-3">
	<div class="col-3 p-0 card border-2 d-flex flex-column h-100 overflow-y-auto" id="users">
		{#if list_conversation.size === 0}
			<div class="d-flex justify-content-center align-items-center h-100">
				<h2>No conversation available</h2>
			</div>
		{:else}
			{#each list_conversation.values() as conversation}
				<UserSelect
					{conversation}
					selected={selected_conversation?.room_name == conversation.room_name}
					on:select={() => {
						selected_conversation = conversation;
					}}
				/>
			{/each}
		{/if}
	</div>
	<div class="col card border-2 p-3 h-100 overflow-auto" id="chat">
		{#if selected_conversation !== null}
			<div class="header d-flex justify-content-between">
				<div class="user d-flex flex-row align-items-center gap-3 w-100">
					<Avatar
						src={selected_conversation.chatting_with.profile_image}
						size={48}
						showStatus={true}
						online={online_status}
					/>
					<a
						class="m-0 fw-bold h2 text-decoration-none"
						href="/profile/{selected_conversation.chatting_with.username}"
					>
						{selected_conversation.chatting_with.display_name}
					</a>
					<button
						type="button"
						class="btn btn-primary ms-auto"
						on:click={() => {
							const room_name = selected_conversation?.room_name;
							if (!room_name) return;
							sendInvitation("invitation", room_name);
						}}
					>
						<Fa icon={faUserPlus} class="me-1" />
						Invite to a game
					</button>
				</div>
			</div>
			<hr />
			<div bind:this={messages_container} id="messages" class="overflow-y-auto d-flex flex-column gap-3 mt-auto">
				{#if current_messages.length === 0}
					<div class="d-flex justify-content-center align-items-center h-100">
						<h2>No messages available</h2>
					</div>
				{:else}
					{#each current_messages as message}
						{#if message.message_type === "invitation"}
							<GameInvite
								game_type="casual"
								self={message.sender !== selected_conversation.chatting_with.username}
								invitation_date={message.timestamp}
								is_accepted={message.is_accepted}
								room_name={message.room_name}
							/>
						{:else}
							<Message
								message={message.message}
								self={message.sender !== selected_conversation.chatting_with.username}
							/>
						{/if}
					{/each}
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
						on:keyup={(e) => {
							if (e.key === "Enter") handleWsMessage();
						}}
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
