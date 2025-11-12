<script setup lang="ts">
import type { Bullet } from "./Bullets.vue";

defineProps<{
  item: string | Bullet;
  level: number;
  index: number;
}>();
</script>

<template>
  <li :key="`${level}-${index}`">
    <!-- если обычная строка -->
    <span v-if="typeof item === 'string'">{{ item }}</span>

    <!-- если объект -->
    <template v-else>
      <span>{{ item.text }}</span>
      <CommonResumeBullets
        v-if="item.children && item.children.length"
        :bullets="item.children"
        :level="level + 1"
      />
    </template>
  </li>
</template>
