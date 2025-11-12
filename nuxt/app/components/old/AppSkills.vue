<script setup lang="ts">
const skills = [
  {
    title: "Backend",
    icon: "i-heroicons-code-bracket",
    color: "text-blue-600",
    description:
      "Python (FastAPI, Django), REST/GraphQL, архитектура микросервисов, оптимизация БД.",
  },
  {
    title: "Frontend",
    icon: "i-heroicons-computer-desktop",
    color: "text-purple-600",
    description:
      "Vue 3, Nuxt 3, TailwindCSS, Nuxt UI, SSR/SPA, оптимизация производительности.",
  },
  {
    title: "DevOps",
    icon: "i-heroicons-cloud",
    color: "text-green-600",
    description:
      "Docker, CI/CD (GitHub Actions, GitLab CI), Kubernetes, облачные сервисы (AWS, GCP).",
  },
];
</script>

<template>
  <section id="skills" class="py-16">
    <div class="container mx-auto">
      <h2 class="text-3xl font-bold text-center mb-10">Навыки</h2>
      <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-8">
        <UCard
          v-for="skill in skills"
          :key="skill.title"
          class="shadow hover:shadow-lg transition"
        >
          <template #header>
            <div class="flex items-center gap-2 text-lg font-semibold">
              <UIcon :name="skill.icon" :class="['text-xl', skill.color]" />
              {{ skill.title }}
            </div>
          </template>
          <p class="text-gray-600 dark:text-gray-400">
            {{ skill.description }}
          </p>
        </UCard>
      </div>
    </div>
  </section>
</template>
