<script setup lang="ts">
defineProps<{ level?: number }>();
</script>

<template>
  <section :class="`level-${level}`">
    <slot />
  </section>
</template>
