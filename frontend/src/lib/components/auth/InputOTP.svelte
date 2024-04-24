<script lang="ts">
    import { onMount } from "svelte";

	export let maxLength = 6;
	export let name: string = "otp";
	export let autofocus: boolean = false;

	let value: string = "";
	let input: HTMLInputElement | null = null;

	let prevSelection: {
		start: number;
		end: number;
		direction: "forward" | "backward" | "none";
	} = { start: -1, end: -1, direction: "none" };

	let selection = {
		start: -1,
		end: -1,
	};

	function handleSelection() {
		if (input == null) return;

		const start = input.selectionStart ?? -1;
		const end = input.selectionEnd ?? -1;
		const direction = input.selectionDirection ?? "none";

		if (start < 0 || end < 0) return;
		if (start === 0 && end === 0 && start === end) input.setSelectionRange(1, 1);

		if (prevSelection.start === prevSelection.end && start !== end) {
			const newStart = Math.max(0, start - +(direction !== "none"));
			input.setSelectionRange(newStart, end, direction);
			prevSelection = { start, end, direction };
		}

		if (prevSelection.start === start && prevSelection.end > end && start === end)
			input.setSelectionRange(start + 1, start + 1, "forward");

		if (start === end) {
			selection = {
				start: Math.max(start - 1, 0),
				end: Math.max(end - 1, 0),
			};
		} else {
			selection = {
				start: Math.max(start, 0),
				end: Math.max(end - 1, 0),
			};
		}
		prevSelection = { start, end, direction };
	}

	onMount(() => {
		handleSelection();
	});
</script>

<!-- Handle selection change event -->
<svelte:window on:selectionchange={handleSelection} />

<div class="otp-field input-group position-relative d-inline-flex align-items-center user-select-none pe-none">
	<div class="d-flex align-items-center border-1">
		{#each Array(maxLength) as _, i}
			<div
				class="d-flex align-items-center justify-content-center border border-1
					{i !== maxLength - 1 ? 'border-end-0' : 'rounded-end'}
					{i === 0 ? 'rounded-start' : ''}
					{i >= selection.start && i <= selection.end ? 'hightlight' : ''}"
				style="width: 2.5rem; height: 2.5rem"
			>
				{value[i] ?? ""}
			</div>
		{/each}
	</div>
	<div class="position-absolute pe-none w-100 h-100 font-monospace">
		<input
			bind:this={input}
			on:focus={handleSelection}
			on:blur={() => (selection = { start: -1, end: -1 })}
			class="otp-input w-100 h-100 bg-transparent pe-auto"
			{name}
			{autofocus}
			type="text"
			maxlength={maxLength}
			inputmode="numeric"
			pattern="^\d+$"
			autocomplete="one-time-code"
			bind:value
			required
		/>
	</div>
</div>

<style>
	.otp-input {
		appearance: none;
		border: none;
		outline: none;
		caret-color: transparent;
		color: transparent;
		letter-spacing: 3ch;
		font-variant-numeric: tabular-nums;
	}

	.otp-input::selection {
		background-color: transparent;
		color: transparent;
	}

	.hightlight {
		z-index: 10;
		box-shadow: 0 0 0 0.125rem hsl(0, 0%, 80%);
		border-color: hsl(0, 0%, 80%) !important;
	}
</style>
