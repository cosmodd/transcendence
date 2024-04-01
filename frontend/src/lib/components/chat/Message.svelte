<script lang="ts">
	export let message: string;
	export let self: boolean = false;
</script>

<div class="d-flex flex-row {self ? 'justify-content-end' : ''}">
	<div class="message {self ? 'bg-primary text-white' : 'bg-secondary'}">{message}</div>
</div>

<style>
	.message {
		max-width: 75%;
		border-radius: 10px;
		padding: 10px 12px;
	}
</style>
