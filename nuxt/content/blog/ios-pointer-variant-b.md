---
title: "Быстрый старт: iOS‑Pointer курсор на Nuxt 4 за 5 шагов"
description: "Минимальный набор шагов для запуска кастомного курсора с motion-v и Nuxt UI v4 + важные примечания по интеграции."
date: 2025-10-14
image: /s3/blog/mouse-pointer-icons.avif
tags: ["Nuxt 4", "motion-v", "Quick Start"]
---

::callout{type="info" icon="i-lucide-mouse-pointer"}
На этой странице курсор включён через `definePageMeta({ iosPointer: true })`.
::

# Быстрый старт

::steps

### 1) Установка

::code-group

```bash [npm]
npm i motion-v @nuxt/ui @nuxt/content
```

```bash [pnpm]
pnpm add motion-v @nuxt/ui @nuxt/content
```

```bash [yarn]
yarn add motion-v @nuxt/ui @nuxt/content
```

```bash [bun]
bun add motion-v @nuxt/ui @nuxt/content
```

::

`nuxt.config.ts`:

```ts
export default defineNuxtConfig({
  modules: ['@nuxt/ui', '@nuxt/content']
})
```

### 2) Компонент

::code-collapse{title="Минимальный IosPointer.vue"}

```vue
<script setup lang="ts">
import { animate } from 'motion-v'
const props = defineProps({ enabled: { type: Boolean, default: false } })
const pointer = ref<HTMLElement | null>(null)
const pos = reactive({ x: 0, y: 0 }); const target = reactive({ x: 0, y: 0 })

function onMove(e: MouseEvent){ target.x=e.clientX; target.y=e.clientY }
function loop(){ if(!pointer.value) return requestAnimationFrame(loop); pos.x+=(target.x-pos.x)*0.25; pos.y+=(target.y-pos.y)*0.25; const w=pointer.value.offsetWidth/2, h=pointer.value.offsetHeight/2; pointer.value.style.translate = `${pos.x-w}px ${pos.y-h}px`; requestAnimationFrame(loop) }

onMounted(()=>{ if(!props.enabled) return; document.body.classList.add('cursor-active'); document.addEventListener('pointermove', onMove, { passive:true }); loop() })
onUnmounted(()=>{ document.body.classList.remove('cursor-active'); document.removeEventListener('pointermove', onMove) })
</script>

<template>
  <ClientOnly><div ref="pointer" data-ios-cursor class="fixed top-0 left-0 h-3 w-3 rounded-full bg-white"/></ClientOnly>
</template>
```

::

### 3) Подключение

```vue
<IosPointer :enabled="useRuntimeConfig().public.iosPointerEnabled && useRoute().meta.iosPointer !== false" />
```

### 4) Стили

::code-collapse{title="app/assets/css/cursor.css"}

```css
body.cursor-active, body.cursor-active a, body.cursor-active button, body.cursor-active [role='button'], body.cursor-active .clickable { cursor: none !important; }
[data-ios-cursor]{ position:fixed; top:0; left:0; z-index:2147483647; width:12px; height:12px; border-radius:9999px; pointer-events:none!important; isolation:isolate; view-transition-name:none!important; }
::view-transition-group(root), ::view-transition-image-pair(root), ::view-transition-old(root), ::view-transition-new(root){ pointer-events:none!important; }
```

::

Добавить `@import './cursor.css';` в `app/assets/css/main.css`.

### 5) Точечное включение

```ts
definePageMeta({ iosPointer: true })
```

::/steps
