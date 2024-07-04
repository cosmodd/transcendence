<script lang="ts">
	export let src: string = "/static/images/default_profile_image.jpg";
	export let size = 32;
	export let showStatus: boolean = false;
	export let online: boolean = false;
</script>

<div class="avatar position-relative" class:online class:show-status={showStatus} style="--size: {size}px;">
	<img {src} class="rounded-circle" alt="avatar" />
</div>

<style>
	.avatar img {
		width: var(--size);
		height: var(--size);
		object-fit: cover;
	}

	.avatar.show-status::after {
		content: "";
		position: absolute;
		bottom: calc(var(--size) / 8);
		right: calc(var(--size) / 8);
		transform: translate(50%, 50%);
		width: calc(var(--size) / 4);
		height: calc(var(--size) / 4);
		border-radius: 50%;
		background-color: var(--bs-success);
		border: var(--bs-body-bg) solid calc(var(--size) / 16);
		box-sizing: content-box;
	}
</style>
