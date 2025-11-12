<script setup lang="ts">
defineProps<{
  variant?: "minimal" | "glow" | "dashed";
}>();
</script>

<template>
  <div>
    <!-- Minimal -->
    <div
      v-if="variant === 'minimal' || !variant"
      class="w-full h-[1px] my-10 bg-gradient-to-r from-[var(--p-primary-color)] to-transparent opacity-70"
    />

    <!-- Glow -->
    <div v-else-if="variant === 'glow'" class="relative my-12">
      <div
        class="w-full h-[1px] bg-gradient-to-r from-transparent via-[var(--p-primary-color)] to-transparent"
      ></div>
      <div
        class="absolute inset-0 w-full h-[2px] blur-md bg-gradient-to-r from-transparent via-[var(--p-primary-color)] to-transparent opacity-40"
      ></div>
    </div>

    <!-- Dashed -->
    <div
      v-else-if="variant === 'dashed'"
      class="w-full border-t border-dashed border-[var(--p-primary-color)] my-10"
    ></div>
  </div>
</template>
