<script setup lang="ts">
export interface Bullet {
  text: string;
  children?: Bullet[];
}

defineProps<{
  bullets: Bullet[];
  level?: number;
}>();

function getListClass(level?: number) {
  if (level === 1) return "pl-5 mt-1 space-y-1 list-disc";
  if (level === 2) return "pl-5 mt-1 space-y-1 list-[circle]";
  if (level === 3) return "pl-5 mt-1 space-y-1 list-[square]";
  if (level && level > 3) return "pl-5 mt-1 space-y-1 list-disc text-xs opacity-80";
  return "pl-5 mt-1 space-y-1";
}
</script>

<template>
  <ul :class="getListClass(level)">
    <li v-for="(item, i) in bullets" :key="`${level ?? 1}-${i}`">
      {{ item.text }}
      <CommonResumeBullets
        v-if="item.children?.length"
        :bullets="item.children"
        :level="(level ?? 1) + 1"
      />
    </li>
  </ul>
</template>
