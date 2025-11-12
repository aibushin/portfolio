<script setup lang="ts">
type AlertType = "success" | "warning" | "danger";

const props = defineProps<{ type: AlertType }>();

const config: Record<AlertType, { var: string; icon: string }> = {
  success: { var: "--p-success-color", icon: "pi pi-check-circle" },
  warning: { var: "--p-warning-color", icon: "pi pi-exclamation-triangle" },
  danger: { var: "--p-danger-color", icon: "pi pi-times-circle" },
};

const current = config[props.type];
</script>

<template>
  <div
    class="flex items-center gap-3 p-4 rounded-lg border-l-4"
    :style="{
      borderColor: `var(${current.var})`,
      background: `color-mix(in srgb, var(${current.var}) 8%, transparent)`,
    }"
  >
    <!-- Иконка -->
    <i
      :class="current.icon"
      class="text-lg shrink-0"
      :style="{ color: `var(${current.var})` }"
    />

    <!-- Контент -->
    <div class="flex-1 text-sm leading-relaxed">
      <slot />
    </div>
  </div>
</template>
