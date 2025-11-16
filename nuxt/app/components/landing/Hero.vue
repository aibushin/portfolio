<script setup lang="ts">
	import type { IndexCollectionItem } from '@nuxt/content';

	const { footer, global } = useAppConfig();

	defineProps<{
		page: IndexCollectionItem;
	}>();
</script>

<template>
	<UPageHero
		:ui="{
			headline: 'flex items-center justify-center',
			title: 'text-shadow-md max-w-lg mx-auto',
			links: 'mt-4 flex-col justify-center items-center',
		}"
	>
		<template #headline>
			<Motion
				:initial="{
					scale: 1.1,
					opacity: 0,
					filter: 'blur(20px)',
				}"
				:animate="{
					scale: 1,
					opacity: 1,
					filter: 'blur(0px)',
				}"
				:transition="{
					duration: 0.6,
					delay: 0.1,
				}"
			>
				<NuxtImg
					class="ring-default size-36 rounded-full ring ring-offset-3 ring-offset-(--ui-bg)"
					:src="global.picture?.light!"
					width="150"
					height="150"
					draggable="false"
				/>
			</Motion>
		</template>

		<template #title>
			<Motion
				:initial="{
					scale: 1.1,
					opacity: 0,
					filter: 'blur(20px)',
				}"
				:animate="{
					scale: 1,
					opacity: 1,
					filter: 'blur(0px)',
				}"
				:transition="{
					duration: 0.6,
					delay: 0.1,
				}"
			>
				{{ page.title }}
			</Motion>
		</template>

		<template #description>
			<Motion
				:initial="{
					scale: 1.1,
					opacity: 0,
					filter: 'blur(20px)',
				}"
				:animate="{
					scale: 1,
					opacity: 1,
					filter: 'blur(0px)',
				}"
				:transition="{
					duration: 0.6,
					delay: 0.3,
				}"
			>
				{{ page.description }}
			</Motion>
		</template>

		<template #links>
			<Motion
				:initial="{
					scale: 1.1,
					opacity: 0,
					filter: 'blur(20px)',
				}"
				:animate="{
					scale: 1,
					opacity: 1,
					filter: 'blur(0px)',
				}"
				:transition="{
					duration: 0.6,
					delay: 0.5,
				}"
			>
				<div v-if="page.hero.links" class="flex items-center gap-2">
					<UButton v-bind="page.hero.links[0]" />
					<UButton
						:color="global.available ? 'success' : 'error'"
						variant="ghost"
						class="gap-2"
						:to="global.available ? '/about' : ''"
						:label="
							global.available
								? 'Доступен для новых проектов'
								: 'Недоступен в данный момент'
						"
					>
						<template #leading>
							<span class="relative flex size-2">
								<span
									class="absolute inline-flex size-full rounded-full opacity-75"
									:class="
										global.available ? 'bg-success animate-ping' : 'bg-error'
									"
								/>
								<span
									class="relative inline-flex size-2 scale-90 rounded-full"
									:class="global.available ? 'bg-success' : 'bg-error'"
								/>
							</span>
						</template>
					</UButton>
				</div>
			</Motion>

			<div class="mt-4 inline-flex gap-x-4">
				<Motion
					v-for="(link, index) of footer?.links"
					:key="index"
					:initial="{
						scale: 1.1,
						opacity: 0,
						filter: 'blur(20px)',
					}"
					:animate="{
						scale: 1,
						opacity: 1,
						filter: 'blur(0px)',
					}"
					:transition="{
						duration: 0.6,
						delay: 0.5 + index * 0.1,
					}"
				>
					<UButton
						v-bind="{ size: 'md', color: 'neutral', variant: 'ghost', ...link }"
					/>
				</Motion>
			</div>
		</template>

		<UMarquee pause-on-hover class="pt-16">
			<ULink
				v-for="(tech, index) in page.hero.technologies"
				:key="index"
				:to="{ path: '/blog', query: { tag: tech.name } }"
			>
				<UIcon :name="tech.icon" class="size-12 shrink-0" />
			</ULink>
		</UMarquee>

		<UMarquee pause-on-hover reverse>
			<ULink
				v-for="(tech, index) in page.hero.technologiesReverse"
				:key="index"
				:to="{ path: '/blog', query: { tag: tech.name } }"
			>
				<UIcon :name="tech.icon" class="size-12 shrink-0" />
			</ULink>
		</UMarquee>
	</UPageHero>
</template>
