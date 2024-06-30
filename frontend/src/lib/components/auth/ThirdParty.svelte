<script lang="ts">
	import { user } from "$lib/stores/user";
</script>

{#if !$user.third_party_auth}
	<slot />
{:else}
	<slot name="disabled" />
{/if}