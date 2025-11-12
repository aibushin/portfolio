<script setup lang="ts">
	import type { ContentNavigationItem } from '@nuxt/content';
	import { mapContentNavigation } from '@nuxt/ui/utils/content';
	import { findPageBreadcrumb } from '@nuxt/content/utils';

	const route = useRoute();

	const { data: page } = await useAsyncData(route.path, () =>
		queryCollection('blog').path(route.path).first()
	);
	if (!page.value)
		throw createError({
			statusCode: 404,
			message: 'Нет такой страницы',
			fatal: true,
		});

	const { data: surround } = await useAsyncData(`${route.path}-surround`, () =>
		queryCollectionItemSurroundings('blog', route.path, {
			fields: ['description'],
		})
	);

	const navigation = inject<Ref<ContentNavigationItem[]>>(
		'navigation',
		ref([])
	);
	const blogNavigation = computed(
		() => navigation.value.find((item) => item.path === '/blog')?.children || []
	);

	const breadcrumb = computed(() =>
		mapContentNavigation(
			findPageBreadcrumb(blogNavigation.value, page.value?.path)
		).map(({ icon, ...link }) => link)
	);

	if (page.value.image) {
		defineOgImage({ url: page.value.image });
	} else {
		defineOgImageComponent(
			'Blog',
			{
				headline: breadcrumb.value.map((item) => item.label).join(' > '),
			},
			{ fonts: ['Geist:400', 'Geist:600'] }
		);
	}

	const title = page.value?.seo?.title || page.value?.title;
	const description = page.value?.seo?.description || page.value?.description;

	useSeoMeta({
		title,
		description,
		ogDescription: description,
		ogTitle: title,
	});

	// ✅ безопасное вычисление ссылки
	const articleLink = computed(() => {
		if (process.client) return window.location.href;
		const url = useRequestURL();
		return url.href;
	});

	const formatDate = (dateString: string) => {
		return new Date(dateString).toLocaleDateString('en-US', {
			year: 'numeric',
			month: 'short',
			day: 'numeric',
		});
	};
</script>

<template>
	<UMain class="mt-20 px-2">
		<UContainer class="relative min-h-screen">
			<UPage v-if="page">
				<ULink to="/blog" class="flex items-center gap-1 text-sm">
					<UIcon name="lucide:chevron-left" />
					Блог
				</ULink>
				<div class="mt-8 flex flex-col gap-3">
					<div
						class="text-muted flex items-center justify-center gap-2 text-xs"
					>
						<span v-if="page.date">
							{{ formatDate(page.date) }}
						</span>
						<span v-if="page.date && page.minRead">-</span>
						<span v-if="page.minRead">{{ page.minRead }} MIN READ</span>
					</div>
					<NuxtImg
						:src="page.image"
						:alt="page.title"
						class="h-[300px] w-full rounded-lg object-cover object-center"
					/>
					<h1 class="mx-auto mt-4 max-w-3xl text-center text-4xl font-medium">
						{{ page.title }}
					</h1>
					<p class="text-muted mx-auto max-w-2xl text-center">
						{{ page.description }}
					</p>
					<div class="mt-2 flex items-center justify-center gap-2">
						<UUser
							orientation="vertical"
							color="neutral"
							variant="outline"
							class="items-center justify-center text-center"
							v-bind="page.author"
						/>
					</div>
				</div>
				<UPageBody class="mx-auto max-w-3xl">
					<ContentRenderer v-if="page.body" :value="page" />

					<div class="text-muted flex items-center justify-end gap-2 text-sm">
						<UButton
							size="sm"
							variant="link"
							color="neutral"
							label="Копировать ссылку"
							@click="
								copyToClipboard(
									articleLink,
									'Ссылка на статью скопирована в буфер'
								)
							"
						/>
					</div>
					<UContentSurround :surround />
				</UPageBody>
			</UPage>
		</UContainer>
	</UMain>
</template>
