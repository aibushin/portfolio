<script setup lang="ts">
	import type { IndexCollectionItem } from '@nuxt/content';

	defineProps<{
		page: IndexCollectionItem;
	}>();

	const { data: posts } = await useAsyncData('index-blogs', () =>
		queryCollection('blog').order('date', 'DESC').limit(3).all()
	);
	if (!posts.value) {
		throw createError({
			statusCode: 404,
			message: 'blogs posts not found',
			fatal: true,
		});
	}
</script>

<template>
	<UPageSection
		:title="page.blog.title"
		:description="page.blog.description"
		:ui="{
			container: 'px-0 !pt-0 sm:gap-6 lg:gap-8',
			title: 'text-left text-xl sm:text-xl lg:text-2xl font-medium',
			description: 'text-left mt-2 text-sm sm:text-md lg:text-sm text-muted',
		}"
	>
		<UBlogPosts
			v-if="posts?.length"
			orientation="vertical"
			class="gap-4 lg:gap-y-4"
		>
			<UBlogPost
				v-for="(post, index) in posts"
				:key="index"
				orientation="horizontal"
				variant="naked"
				v-bind="post"
				:to="post.path"
				:ui="{
					root: 'group relative lg:items-start lg:flex ring-0 hover:ring-0',
					body: '!px-0',
					header: 'hidden',
				}"
			>
				<template #footer>
					<UButton size="xs" variant="link" class="gap-0 px-0" label="Читать">
						<template #trailing>
							<UIcon
								name="i-lucide-arrow-right"
								class="text-primary size-4 opacity-0 transition-all group-hover:translate-x-1 group-hover:opacity-100"
							/>
						</template>
					</UButton>
				</template>
			</UBlogPost>
		</UBlogPosts>
	</UPageSection>
</template>
