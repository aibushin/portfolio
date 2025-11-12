<script setup lang="ts">
	defineProps<{
		image: {
			src: string;
			alt: string;
		};
		index: number;
	}>();
</script>

<template>
	<div
		class="flex flex-col bg-white p-2 drop-shadow-2xl transition-transform duration-300 ease-in-out hover:z-10 hover:scale-105 hover:rotate-0"
		:class="[
			index % 2 === 0 ? '-rotate-5' : 'rotate-5',
			index % 2 === 0 ? 'hover:-translate-x-4' : 'hover:translate-x-4',
		]"
	>
		<img :src="image.src" :alt="image.alt" class="size-32 object-cover" />
		<span
			class="mt-2 w-32 text-center font-serif text-xs font-medium text-black"
		>
			{{ image.alt }}
		</span>
	</div>
</template>
