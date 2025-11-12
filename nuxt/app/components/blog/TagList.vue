<script setup lang="ts">
import { ref, computed } from "vue";

interface TagItem {
  name: string;
  count: number;
}

interface Props {
  tags: TagItem[];
  mode?: "filter" | "link";
  selected?: string | null;
  limit?: number; // сколько тегов показывать сразу
}

const props = withDefaults(defineProps<Props>(), {
  mode: "link",
  selected: null,
  limit: 0,
});

const emit = defineEmits<{
  (e: "select", tag: string): void;
}>();

// состояние для переключения "все/только limit"
const showAll = ref(false);

const visibleTags = computed(() => {
  if (!props.limit || showAll.value) {
    return props.tags;
  }
  return props.tags.slice(0, props.limit);
});
</script>

<template>
  <div class="flex flex-col gap-2">
    <!-- Режим фильтра -->
    <template v-if="mode === 'filter'">
      <button
        v-for="tag in visibleTags"
        :key="tag.name"
        @click="emit('select', tag.name)"
        class="flex items-center justify-between px-3 py-1 rounded-lg text-sm font-medium transition"
        :class="[
          selected === tag.name
            ? 'bg-blue-600 text-white'
            : 'bg-gray-200 text-gray-800 hover:bg-gray-300 dark:bg-gray-700 dark:text-gray-200 dark:hover:bg-gray-600',
        ]"
      >
        <span>#{{ tag.name }}</span>
        <span class="opacity-70">{{ tag.count }}</span>
      </button>
    </template>

    <!-- Режим ссылок -->
    <template v-else>
      <NuxtLink
        v-for="tag in visibleTags"
        :key="tag.name"
        :to="`/blog/tags/${tag.name}`"
        class="flex items-center justify-between px-3 py-1 rounded-lg text-sm font-medium bg-gray-200 text-gray-800 hover:bg-gray-300 dark:bg-gray-700 dark:text-gray-200 dark:hover:bg-gray-600 transition"
      >
        <span>#{{ tag.name }}</span>
        <span class="opacity-70">{{ tag.count }}</span>
      </NuxtLink>
    </template>

    <!-- Кнопка "Показать все / Свернуть" -->
    <button
      v-if="limit && props.tags.length > limit"
      @click="showAll = !showAll"
      class="mt-2 text-sm text-blue-600 hover:underline dark:text-blue-400 self-start"
    >
      {{ showAll ? "Свернуть" : "Показать все" }}
    </button>
  </div>
</template>
