<template>
  <main class="mx-auto max-w-screen-lg px-4 py-12 space-y-12">
    <h1 class="text-2xl font-bold mb-6">Demo: Glow и Waves без PrimeVue</h1>

    <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-8">
      <!-- Только Glow -->
      <div class="rounded-xl glow-hover bg-white dark:bg-gray-800 p-8 text-center">
        <h2 class="font-semibold text-lg mb-2">Только Glow</h2>
        <p class="text-sm text-gray-600 dark:text-gray-400">Мягкое свечение при hover</p>
      </div>

      <!-- Только Waves -->
      <div
        class="rounded-xl waves-soft bg-white dark:bg-gray-800 p-8 text-center relative overflow-hidden"
      >
        <div class="waves"></div>
        <h2 class="font-semibold text-lg mb-2 relative z-10">Только Waves</h2>
        <p class="text-sm text-gray-600 dark:text-gray-400 relative z-10">
          Волны всегда активны, исчезают при hover
        </p>
      </div>

      <!-- Glow + Waves -->
      <div
        class="rounded-xl glow-hover waves-soft bg-white dark:bg-gray-800 p-8 text-center relative overflow-hidden"
      >
        <div class="waves"></div>
        <h2 class="font-semibold text-lg mb-2 relative z-10">Glow + Waves</h2>
        <p class="text-sm text-gray-600 dark:text-gray-400 relative z-10">
          Glow при hover, волны плавно растворяются
        </p>
      </div>
    </div>
  </main>
</template>
