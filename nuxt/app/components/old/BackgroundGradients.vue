<template>
  <div class="pointer-events-none absolute inset-0 z-0">
    <!-- 🔹 Верхний градиент -->
    <div class="absolute inset-x-0 top-0 h-[300px] bg-gradient-primary opacity-20"></div>

    <!-- 🔹 Нижний градиент (перевёрнутый) -->
    <div
      class="absolute inset-x-0 bottom-0 h-[300px] bg-gradient-primary opacity-20 transform rotate-180"
    ></div>
  </div>
</template>
