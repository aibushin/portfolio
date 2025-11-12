<script setup lang="ts">
import { useRoute } from "vue-router";
import { useAsyncData } from "#app";

const route = useRoute();
const tag = route.params.tag as string;

const { data: articles } = await useAsyncData(`tag-${tag}`, async () => {
  const all = await queryCollection("blog")
    .order("date", "DESC")
    .select("title", "description", "path", "date", "tags", "image")
    .all();

  // фильтруем строго: только статьи, где tags включает наш tag
  return all.filter((post) => post.tags?.includes(tag));
});
</script>

<template>
  <section class="container mx-auto py-12">
    <h1 class="text-3xl font-bold mb-8">Статьи с тегом «{{ tag }}»</h1>

    <!-- Грид статей -->
    <div v-if="articles?.length" class="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
      <NuxtLink
        v-for="post in articles"
        :key="post.path"
        :to="post.path"
        class="block rounded-xl overflow-hidden shadow hover:shadow-lg transition-shadow bg-white dark:bg-gray-800"
      >
        <img
          v-if="post.image"
          :src="post.image"
          :alt="post.title"
          class="w-full h-44 object-cover"
          loading="lazy"
        />
        <div class="p-4">
          <h3 class="text-xl font-semibold mb-1 line-clamp-2">
            {{ post.title }}
          </h3>
          <p class="text-gray-600 dark:text-gray-400 mb-3 line-clamp-2">
            {{ post.description }}
          </p>
          <div class="flex items-center text-sm text-gray-500 dark:text-gray-400">
            <i class="pi pi-calendar mr-2" />
            {{ new Date(post.date).toLocaleDateString("ru-RU") }}
          </div>
          <div v-if="post.tags?.length" class="mt-3 flex flex-wrap gap-2">
            <NuxtLink
              v-for="t in post.tags"
              :key="t"
              :to="`/blog/tags/${t}`"
              class="text-xs bg-blue-100 text-blue-800 px-2 py-0.5 rounded-full dark:bg-blue-900 dark:text-blue-200"
            >
              {{ t }}
            </NuxtLink>
          </div>
        </div>
      </NuxtLink>
    </div>

    <!-- Если статей нет -->
    <div
      v-else
      class="bg-white dark:bg-gray-800 rounded-xl p-8 text-center text-gray-500 border border-dashed"
    >
      Статей с тегом <strong>{{ tag }}</strong> пока нет.
      <NuxtLink to="/blog" class="text-blue-600 underline">Вернуться в блог</NuxtLink>.
    </div>
  </section>
</template>
