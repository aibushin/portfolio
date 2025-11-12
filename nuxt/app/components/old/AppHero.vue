<script setup lang="ts">
const { scrollToContacts } = useScrollTo();
</script>

<template>
  <section class="relative flex flex-col items-center text-center py-20">
    <img src="/blog/me.jpg" alt="Антон" class="w-32 h-32 rounded-full shadow-lg mb-6" />

    <h1 class="text-4xl font-bold tracking-tight">Привет, я Антон 👋</h1>

    <p class="mt-3 text-lg text-gray-400">
      Team Lead · Python/JS · Архитектура и продакшн
    </p>

    <div class="mt-6 flex gap-4">
      <UButton to="/resume" icon="i-heroicons-document-text" label="Резюме" />

      <UButton
        icon="i-heroicons-paper-airplane"
        label="Связаться"
        variant="outline"
        @click="scrollToContacts"
      />
    </div>
  </section>
</template>
