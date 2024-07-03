<script lang="ts">
	import Fa from "svelte-fa";
	import { faCircleCheck, faExclamationCircle, faInfoCircle, faXmarkCircle } from "@fortawesome/free-solid-svg-icons";
	import { tweened } from "svelte/motion";
	import { linear } from "svelte/easing";
	import { onMount } from "svelte";

	export let data: ToastData;

	const Title = {
		error: "Error",
		success: "Success",
		warning: "Warning",
		info: "Information",
	};

	const colorClass = {
		error: "danger",
		success: "success",
		warning: "warning",
		info: "info",
	};

	const progress = tweened(1, {
		duration: data.duration,
		easing: linear,
	});

	onMount(() => {
		progress.set(0, { duration: data.duration });
	});
</script>

<div class="toast show" role="alert" aria-live="assertive" aria-atomic="true">
	<div class="toast-header">
		{#if data.type === "error"}
			<Fa icon={faXmarkCircle} class="text-danger me-2" />
		{:else if data.type === "success"}
			<Fa icon={faCircleCheck} class="text-success me-2" />
		{:else if data.type === "warning"}
			<Fa icon={faExclamationCircle} class="text-warning me-2" />
		{:else}
			<Fa icon={faInfoCircle} class="text-info me-2" />
		{/if}
		<span class="text-light fw-bold me-auto">{data.title ?? Title[data.type]}</span>
		<button type="button" class="btn-close" aria-label="Close" on:click={data.remove}></button>
	</div>
	<div class="toast-body">
		{data.description ?? ""}
		{#if data.buttons}
			<div class="buttons d-grid mt-2">
				{#each data.buttons as button}
					<button
						class="btn btn-primary btn-sm"
						on:click={() => {
							button?.action();
							if (button?.dismiss)
								data.remove();
						}}
					>
						{button.label ?? "OK"}
					</button>
				{/each}
			</div>
		{/if}
	</div>
	{#if data.showProgress && data.duration > 0}
		<div class="progress" style="height: 2px;">
			<div
				class="progress-bar bg-{colorClass[data.type]}"
				role="progressbar"
				style="width: {Math.round($progress * 100)}%; transition: none !important;"
				aria-valuenow={$progress * 100}
				aria-valuemin="0"
				aria-valuemax="100"
			/>
		</div>
	{/if}
</div>


<style>
	.toast {
		--bs-toast-bg: rgb(var(--bs-body-bg-rgb));
	}
</style>