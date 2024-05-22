<script lang="ts">
	import { page } from "$app/stores";

	export let href: string;
	export let strict: boolean = false;

	$: isActive = strict ? $page.url.pathname === href : $page.url.pathname.startsWith(href);
	$: classes = isActive ? "active fw-bold" : "";
</script>

<a {href} class="nav-link {classes}">
	<slot />
</a>