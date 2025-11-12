<script setup lang="ts">
import { resumeData } from "~/data/resume";
</script>

<template>
  <main class="mx-auto max-w-screen-lg space-y-8 py-8">
    <!-- 🔹 Заголовок -->
    <CommonResumeHeader v-bind="resumeData.personal" class="border-l-4 pl-4" />

    <!-- 🔹 Цель -->
    <CommonResumeSection title="Цель" class="border-l-4 pl-4">
      <p
        class="text-sm leading-relaxed bg-gray-50 dark:bg-gray-800/40 border border-gray-200 dark:border-gray-700 p-4 rounded-lg italic"
      >
        {{ resumeData.objective }}
      </p>
    </CommonResumeSection>

    <!-- 🔹 Образование -->
    <CommonResumeSection title="Образование" class="border-l-4 pl-4">
      <ul class="list-disc pl-5 text-sm space-y-1">
        <li v-for="ed in resumeData.education" :key="ed.year">
          <span class="font-medium">{{ ed.year }}:</span> {{ ed.text }}
        </li>
      </ul>
    </CommonResumeSection>

    <!-- 🔹 Опыт работы -->
    <CommonResumeSection title="Опыт работы" class="border-l-4 pl-4">
      <div class="space-y-6 text-sm leading-relaxed">
        <div
          v-for="job in resumeData.experience"
          :key="job.period"
          class="p-4 rounded-lg bg-gray-50 dark:bg-gray-800/40 border border-gray-200 dark:border-gray-700"
        >
          <h3 class="text-lg font-semibold text-primary">{{ job.company }}</h3>
          <p class="text-sm text-gray-500 dark:text-gray-400">
            {{ job.period }} · {{ job.role }}
          </p>

          <CommonResumeBullets :bullets="job.bullets" :level="1" />
        </div>
      </div>
    </CommonResumeSection>

    <!-- 🔹 Навыки -->
    <CommonResumeSkills :skills="resumeData.skills" />

    <!-- 🔹 Кнопка PDF внизу -->
    <div class="flex justify-center pt-6">
      <UButton
        label="Скачать PDF"
        icon="i-heroicons-arrow-down-tray"
        @click="window.print()"
      />
    </div>
  </main>
</template>
