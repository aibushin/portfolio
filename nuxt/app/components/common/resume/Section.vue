<script setup lang="ts">
defineProps<{ title: string }>()
</script>

<template>
  <UCard>
    <template #header>
      <h3 class="text-lg font-semibold">{{ title }}</h3>
    </template>

    <slot />
  </UCard>
</template>
