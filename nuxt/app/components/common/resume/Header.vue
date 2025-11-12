<script setup lang="ts">
defineProps<{
  name: string
  age: number
  city: string
  phone: string
  email: string
}>()

function printPage() {
  if (import.meta.client) window.print()
}
</script>

<template>
  <UCard>
    <div class="flex flex-col sm:flex-row sm:items-center gap-6">
      <div class="flex-1">
        <h1 class="text-2xl sm:text-3xl font-bold">{{ name }}</h1>
        <p class="mt-2 text-sm opacity-80">{{ age }} года · {{ city }}</p>

        <div class="mt-2 text-sm">
          <p class="flex items-center gap-2 text-sm opacity-80">
            <UIcon name="i-heroicons-phone" class="text-primary" /> {{ phone }}
          </p>
          <p class="flex items-center gap-2 text-sm opacity-80">
            <UIcon name="i-heroicons-envelope" class="text-primary" /> {{ email }}
          </p>
        </div>
      </div>

      <div class="flex gap-2">
        <UButton label="Скачать PDF" @click="printPage" />
      </div>
    </div>
  </UCard>
</template>
