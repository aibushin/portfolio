<script setup lang="ts">
const colorMode = useColorMode();
const mounted = ref(false);

onMounted(() => {
  mounted.value = true;
});

function toggleTheme() {
  colorMode.preference = colorMode.value === "dark" ? "light" : "dark";
}
</script>

<template>
  <header
    class="sticky top-0 z-50 bg-slate-200/80 dark:bg-slate-950/80 border-b-[0.5px] border-gray-700 backdrop-blur-md"
  >
    <div
      class="max-w-screen-lg mx-auto flex items-center justify-between px-4 sm:px-6 lg:px-8 py-3"
    >
      <NuxtLink to="/" class="font-bold text-lg no-underline">aibushin</NuxtLink>

      <div class="flex items-center gap-4">
        <NuxtLink to="/blog" class="no-underline hover:underline">Блог</NuxtLink>

        <!-- кнопка рендерится только на клиенте -->
        <UButton
          v-if="mounted"
          :icon="colorMode.value === 'dark' ? 'i-heroicons-sun' : 'i-heroicons-moon'"
          variant="ghost"
          color="neutral"
          aria-label="Переключить тему"
          @click="toggleTheme"
        />
      </div>
    </div>
  </header>
</template>
