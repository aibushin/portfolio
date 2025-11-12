<script setup lang="ts">
	type Event = {
		title: string;
		date: string;
		location: string;
		url?: string;
		category: 'Конференция' | 'Живое выступление' | 'Подкаст';
	};

	const { data: page } = await useAsyncData('speaking', () => {
		return queryCollection('speaking').first();
	});
	if (!page.value) {
		throw createError({
			statusCode: 404,
			message: 'Нет такой страницы',
			fatal: true,
		});
	}

	useSeoMeta({
		title: page.value?.seo?.title || page.value?.title,
		ogTitle: page.value?.seo?.title || page.value?.title,
		description: page.value?.seo?.description || page.value?.description,
		ogDescription: page.value?.seo?.description || page.value?.description,
	});

	const { global } = useAppConfig();

	const categoriesMapping = {
		Конференция: 'Конференции',
		'Живое выступление': 'Живые выступления',
		Подкаст: 'Подкасты',
	};

	const groupedEvents = computed((): Record<Event['category'], Event[]> => {
		const events = page.value?.events || [];
		const grouped: Record<Event['category'], Event[]> = {
			Конференция: [],
			'Живое выступление': [],
			Подкаст: [],
		};
		for (const event of events) {
			if (grouped[event.category]) grouped[event.category].push(event);
		}
		return grouped;
	});

	function formatDate(dateString: string): string {
		return new Date(dateString).toLocaleDateString('en-US', {
			year: 'numeric',
			month: 'long',
		});
	}
</script>

<template>
	<UPage v-if="page">
		<UPageHero
			:title="page.title"
			:description="page.description"
			:ui="{
				title: '!mx-0 text-left',
				description: '!mx-0 text-left',
				links: 'justify-start',
			}"
		>
			<template #links>
				<UButton
					v-if="page.links"
					:to="`mailto:${global.email}`"
					v-bind="page.links[0]"
				/>
			</template>
		</UPageHero>
		<UPageSection
			:ui="{
				container: '!pt-0',
			}"
		>
			<div
				v-for="(eventsInCategory, category) in groupedEvents"
				:key="category"
				class="mb-16 grid grid-cols-1 last:mb-0 lg:grid-cols-3 lg:gap-8"
			>
				<div class="mb-4 lg:col-span-1 lg:mb-0">
					<h2
						class="text-highlighted text-xl font-semibold tracking-tight lg:sticky lg:top-16"
					>
						{{ categoriesMapping[category] }}
					</h2>
				</div>

				<div class="space-y-8 lg:col-span-2">
					<div
						v-for="(event, index) in eventsInCategory"
						:key="`${category}-${index}`"
						class="group border-default relative border-l pl-6"
					>
						<NuxtLink
							v-if="event.url"
							:to="event.url"
							class="absolute inset-0"
						/>
						<div class="text-muted mb-1 text-sm font-medium">
							<span>{{ event.location }}</span>
							<span v-if="event.location && event.date" class="mx-1">·</span>
							<span v-if="event.date">{{ formatDate(event.date) }}</span>
						</div>

						<h3 class="text-highlighted text-lg font-semibold">
							{{ event.title }}
						</h3>

						<UButton
							v-if="event.url"
							target="_blank"
							:label="event.category === 'Подкаст' ? 'Слушать' : 'Смотреть'"
							variant="link"
							class="gap-0 p-0 pt-2"
						>
							<template #trailing>
								<UIcon
									name="i-lucide-arrow-right"
									class="size-4 opacity-0 transition-all group-hover:translate-x-1 group-hover:opacity-100"
								/>
							</template>
						</UButton>
					</div>
				</div>
			</div>
		</UPageSection>
	</UPage>
</template>
