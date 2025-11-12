<script setup lang="ts">
const { scrollToContacts } = useScrollTo();
</script>

<template>
  <section id="about" class="container mx-auto py-16">
    <div class="text-center max-w-2xl mx-auto">
      <h2 class="text-3xl font-bold mb-6">Обо мне</h2>
      <p class="text-lg text-gray-600 dark:text-gray-400 leading-relaxed">
        Я — <span class="font-semibold">Team Lead и fullstack-разработчик</span> с опытом
        построения архитектуры и управления командами. Люблю писать чистый код, внедрять
        современные технологии и делиться знаниями.
      </p>
      <div class="mt-6">
        <UButton
          label="Связаться"
          icon="i-heroicons-paper-airplane"
          @click="scrollToContacts"
        />
      </div>
    </div>
  </section>
</template>
