<script setup lang="ts">
	const { data: page } = await useAsyncData('about', () => {
		return queryCollection('about').first();
	});
	if (!page.value) {
		throw createError({
			statusCode: 404,
			message: 'Нет такой страницы',
			fatal: true,
		});
	}

	const { global } = useAppConfig();

	useSeoMeta({
		title: page.value?.seo?.title || page.value?.title,
		ogTitle: page.value?.seo?.title || page.value?.title,
		description: page.value?.seo?.description || page.value?.description,
		ogDescription: page.value?.seo?.description || page.value?.description,
	});
</script>

<template>
	<UPage v-if="page">
		<UPageHero
			:title="page.title"
			:description="page.description"
			orientation="horizontal"
			:ui="{
				container: 'lg:flex sm:flex-row items-center',
				title: '!mx-0 text-left',
				description: '!mx-0 text-left',
				links: 'justify-start',
			}"
		>
			<NuxtImg
				class="ring-default size-36 rounded-lg ring ring-offset-3 ring-offset-(--ui-bg) sm:rotate-4"
				:src="global.picture?.light!"
				width="150"
				height="150"
				draggable="false"
			/>
		</UPageHero>
		<UPageSection
			:ui="{
				container: '!pt-0',
			}"
		>
			<MDC :value="page.content" unwrap="p" />
			<div
				class="flex flex-row items-center justify-center space-x-[-2rem] py-10"
			>
				<PolaroidItem
					v-for="(image, index) in page.images"
					:key="index"
					:image="image"
					:index
				/>
			</div>
		</UPageSection>
	</UPage>
</template>
