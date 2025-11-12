<script setup lang="ts">
	import type { NavigationMenuItem } from '@nuxt/ui';

	defineProps<{
		links: NavigationMenuItem[];
	}>();
</script>

<template>
	<div
		class="fixed top-2 left-1/2 z-10 mx-auto -translate-x-1/2 transform sm:top-4"
	>
		<UNavigationMenu
			:items="links"
			variant="link"
			color="neutral"
			class="bg-muted/80 border-muted/50 rounded-full border px-2 shadow-lg shadow-neutral-950/5 backdrop-blur-sm sm:px-4"
			:ui="{
				link: 'px-2 py-1',
				linkLeadingIcon: 'hidden',
			}"
		>
			<template #list-trailing>
				<ColorModeButton />
			</template>
		</UNavigationMenu>
	</div>
</template>
