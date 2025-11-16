<script setup lang="ts">
	const { data: page } = await useAsyncData('blog-page', () => {
		return queryCollection('pages').path('/blog').first();
	});
	if (!page.value) {
		throw createError({
			statusCode: 404,
			message: 'Нет такой страницы',
			fatal: true,
		});
	}

	const { data: posts } = await useAsyncData('blogs', () =>
		queryCollection('blog').order('date', 'DESC').all()
	);
	if (!posts.value) {
		throw createError({
			statusCode: 404,
			message: 'blogs posts not found',
			fatal: true,
		});
	}

	const route = useRoute();

	const activeTag = computed(() => {
		const raw = route.query.tag;
		if (!raw) return undefined;
		return Array.isArray(raw) ? raw[0] : String(raw);
	});

	const filteredPosts = computed(() => {
		if (!posts.value) return [];
		if (!activeTag.value) return posts.value;

		const tagLower = activeTag.value.toLowerCase();

		return posts.value.filter((post: any) =>
			Array.isArray(post.tags)
				? post.tags.some((t: string) => t.toLowerCase() === tagLower)
				: false
		);
	});

	// Базовые значения из страницы
	const baseTitle = computed(() => page.value?.seo?.title || page.value?.title);
	const baseDesc = computed(
		() => page.value?.seo?.description || page.value?.description
	);

	// Динамический SEO: заголовок меняется при смене tag
	useSeoMeta({
		title: () =>
			activeTag.value
				? `${activeTag.value} · ${baseTitle.value}`
				: baseTitle.value,
		ogTitle: () =>
			activeTag.value
				? `${activeTag.value} · ${baseTitle.value}`
				: baseTitle.value,
		description: baseDesc,
		ogDescription: baseDesc,
	});
</script>

<template>
	<UPage v-if="page">
		<UPageHero
			:title="page.title"
			:description="page.description"
			:links="page.links"
			:ui="{
				title: '!mx-0 text-left',
				description: '!mx-0 text-left',
				links: 'justify-start',
			}"
		/>

		<UPageSection :ui="{ container: '!pt-0' }">
			<!-- Индикация активного фильтра по тегу -->
			<div class="mb-4 flex flex-wrap items-center gap-2">
				<span v-if="activeTag" class="text-sm text-gray-400">
					Фильтр по тегу:
				</span>
				<UBadge v-if="activeTag" color="primary" variant="subtle">
					{{ activeTag }}
				</UBadge>

				<ULink
					v-if="activeTag"
					to="/blog"
					class="text-xs text-gray-400 hover:text-gray-200"
				>
					Сбросить фильтр
				</ULink>
			</div>

			<!-- Если нечего показать под фильтром -->
			<div v-if="!filteredPosts.length" class="text-sm text-gray-400">
				По тегу «{{ activeTag }}» пока нет статей.
			</div>

			<UBlogPosts v-else orientation="vertical">
				<Motion
					v-for="(post, index) in filteredPosts"
					:key="index"
					:initial="{ opacity: 0, transform: 'translateY(10px)' }"
					:while-in-view="{ opacity: 1, transform: 'translateY(0)' }"
					:transition="{ delay: 0.2 * index }"
					:in-view-options="{ once: true }"
				>
					<UBlogPost
						variant="naked"
						orientation="horizontal"
						:to="post.path"
						v-bind="post"
						:ui="{
							root: 'md:grid md:grid-cols-2 group overflow-visible transition-all duration-300',
							image: 'group-hover/blog-post:scale-105 rounded-lg',
							header:
								index % 2 === 0
									? 'sm:-rotate-1 overflow-visible'
									: 'sm:rotate-1 overflow-visible',
						}"
					/>
				</Motion>
			</UBlogPosts>
		</UPageSection>
	</UPage>
</template>
