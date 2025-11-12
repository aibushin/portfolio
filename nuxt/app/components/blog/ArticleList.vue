<script setup lang="ts">
import { useAsyncData } from "#app";

interface Props {
  limit?: number;
  showAllLink?: boolean;
  title?: string;
}

const props = withDefaults(defineProps<Props>(), {
  limit: undefined,
  showAllLink: false,
  title: "Последние статьи",
});

const { data: articles } = await useAsyncData(`articles-${props.limit ?? "all"}`, () => {
  let query = queryCollection("blog")
    .order("date", "DESC")
    .select("title", "description", "path", "date", "tags", "image");

  if (props.limit) {
    query = query.limit(props.limit);
  }

  return query.all();
});
</script>

<template>
  <section class="container mx-auto">
    <!-- Заголовок и кнопка -->
    <div class="flex items-center justify-between mb-6">
      <h2 class="text-2xl md:text-3xl font-bold">
        {{ limit ? "Последние статьи" : "Блог" }}
      </h2>

      <NuxtLink v-if="showAllLink" to="/blog">
        <UButton
          label="Все статьи"
          size="sm"
          color="blue"
          variant="outline"
          class="rounded-full"
        />
      </NuxtLink>
    </div>

    <!-- Грид карточек -->
    <div v-if="articles?.length" class="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
      <NuxtLink v-for="post in articles" :key="post.path" :to="post.path" class="block">
        <div class="glow-hover rounded-xl">
          <UCard
            class="h-full rounded-xl overflow-hidden shadow-md dark:shadow-[0_2px_6px_rgba(255,255,255,0.08)]"
          >
            <template #header>
              <img
                v-if="post.image"
                :src="post.image"
                :alt="post.title"
                class="w-full h-44 object-cover"
                loading="lazy"
              />
            </template>

            <template #header-text>
              <h3 class="text-xl font-semibold line-clamp-2">
                {{ post.title }}
              </h3>
              <p class="text-gray-600 dark:text-gray-400 line-clamp-2 mt-1">
                {{ post.description }}
              </p>
            </template>

            <template #footer>
              <div
                class="flex items-center text-sm text-gray-500 dark:text-gray-400 mb-3"
              >
                <UIcon name="i-heroicons-calendar" class="mr-2" />
                {{ new Date(post.date).toLocaleDateString("ru-RU") }}
              </div>
              <div v-if="post.tags?.length" class="flex flex-wrap gap-2">
                <UBadge v-for="tag in post.tags" :key="tag" color="blue" variant="subtle">
                  {{ tag }}
                </UBadge>
              </div>
            </template>
          </UCard>
        </div>
      </NuxtLink>
    </div>

    <!-- Пусто -->
    <div
      v-else
      class="bg-white dark:bg-gray-800 rounded-xl p-8 text-center text-gray-500 border border-dashed"
    >
      Пока статей нет. Загляни позже или перейди в раздел
      <NuxtLink to="/blog" class="text-blue-600 underline">Блог</NuxtLink>.
    </div>
  </section>
</template>
