<script lang="ts">
	import { page } from "$app/stores";

	export let href: string;

	$: classes = $page.url.pathname.startsWith(href) ? "active fw-bold" : "";
</script>

<a {href} class="nav-link {classes}">
	<slot />
</a>