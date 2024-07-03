<script lang="ts">
	import toasts from "$lib/stores/toasts";
	import { fade, fly } from "svelte/transition";
	import Toast from "./Toast.svelte";
	import { flip } from "svelte/animate";
</script>

<div class="toast-container position-fixed w-100 bottom-0 end-0 p-3 d-flex flex-column align-items-end gap-3 z-3">
	{#each $toasts as toast (toast.uid)}
		<div in:fade={{ duration:200 }} out:fly={{ x: 50, duration: 200 }} animate:flip={{ duration: 200 }}>
			<Toast data={toast} />
		</div>
	{/each}
</div>
