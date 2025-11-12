<script setup lang="ts">
defineProps<{
  skills: Record<string, string[]>
}>()

// Соответствие категорий и CSS-переменных Nuxt UI
const categoryColors: Record<string, { bg: string; text: string }> = {
  Backend: { bg: "var(--ui-info)", text: "var(--ui-info-foreground)" },
  Frontend: { bg: "var(--ui-success)", text: "var(--ui-success-foreground)" },
  "DevOps & CI/CD": {
    bg: "var(--ui-warning)",
    text: "var(--ui-warning-foreground)"
  },
  Data: {
    bg: "var(--ui-error)",
    text: "var(--ui-error-foreground)"
  }
}

function getStyle(group: string) {
  const colors =
    categoryColors[group] || {
      bg: "var(--ui-primary)",
      text: "var(--ui-primary-foreground)"
    }
  return {
    backgroundColor: colors.bg,
    color: colors.text
  }
}
</script>

<template>
  <UCard>
    <template #header>
      <h3 class="text-lg font-semibold">Навыки</h3>
    </template>

    <div class="grid sm:grid-cols-2 gap-6 text-sm">
      <div
        v-for="(list, group) in skills"
        :key="group"
        class="p-3 rounded-lg bg-[var(--ui-card)] border border-[var(--ui-border)]"
      >
        <h4 class="font-semibold mb-2">{{ group }}</h4>
        <div class="flex flex-wrap gap-2">
          <UBadge
            v-for="s in list"
            :key="s"
            class="!text-xs px-2 py-1 rounded"
            :style="getStyle(group)"
          >
            {{ s }}
          </UBadge>
        </div>
      </div>
    </div>
  </UCard>
</template>
