---
title: "Создание iOS‑Pointer курсора для Nuxt 4"
description: "Подробное руководство по созданию анимированного кастомного курсора в стиле iOS Pointer с использованием Motion One, Vue 3 Composition API и Nuxt UI v4."
date: 2025-10-13
image: /s3/blog/mouse-pointer-icons.avif
tags:
  - Nuxt 4
  - Motion One
  - Nuxt UI v4
  - Frontend
  - UX Design
---

::callout{type="info" icon="i-lucide-mouse-pointer"}
Эта статья демонстрирует работу **кастомного курсора**, поэтому для нЕго включён `definePageMeta({ iosPointer: true })`.
::

# Создание iOS‑Pointer курсора для Nuxt 4

Механика курсора — часть визуальной идентичности интерфейса.  
В системах Apple курсор «прилипает» к интерактивным элементам, расширяется и мягко двигается вслед за мышью. Такой подход создаёт эффект тактильности даже в веб‑среде.

В этой статье описывается, как реализовать похожий UX‑эффект в **Nuxt 4 + Nuxt UI v4**.

---

## Концепция

- курсор плавно следует за мышью;
- реагирует на кликабельные элементы;
- изменяет размер и форму при наведении;
- не мешает кликам и не блокирует события;
- сбрасывает состояние при навигации и смене темы.

---

## Этапы реализации

::steps
### 1. Подготовка окружения

Убедиться, что в проекте установлены:

```bash
npm install motion-v @nuxt/ui @nuxt/content
```

Добавить в `nuxt.config.ts`:

```ts
export default defineNuxtConfig({
  modules: ['@nuxt/content', '@nuxt/ui'],
})
```

### 2. Создание компонента `IosPointer.vue`

Курсор строится на Motion One и реактивных координатах `pos` и `target`.  
Анимация выполняется с помощью `requestAnimationFrame`.

::code-collapse{title="Полный код IosPointer.vue"}

```vue
<script setup lang="ts">
import { animate } from 'motion-v'
const colorMode = useColorMode()
const router = useRouter()

const props = defineProps({ enabled: { type: Boolean, default: false } })
const pointer = ref<HTMLElement | null>(null)
const pos = reactive({ x: 0, y: 0 })
const target = reactive({ x: 0, y: 0 })
let hoveredEl: HTMLElement | null = null
let hoverRect: DOMRect | null = null
let localX = 0, localY = 0, followActive = false
const SELECTOR = 'a, button, [role="button"], .clickable, [data-cursor]'

function animateMotion(t: HTMLElement, p: Record<string, any>, o?: Record<string, any>) {
  return animate(t, p as any, o)
}

const onMove = (e: MouseEvent) => {
  target.x = e.clientX; target.y = e.clientY
  if (hoveredEl && hoverRect) {
    localX = e.clientX - (hoverRect.left + hoverRect.width / 2)
    localY = e.clientY - (hoverRect.top + hoverRect.height / 2)
  }
}

const animateCursor = () => {
  if (!pointer.value) return requestAnimationFrame(animateCursor)
  pos.x += (target.x - pos.x) * 0.25
  pos.y += (target.y - pos.y) * 0.25
  const w = pointer.value.offsetWidth / 2
  const h = pointer.value.offsetHeight / 2
  pointer.value.style.translate = `${pos.x - w}px ${pos.y - h}px`
  requestAnimationFrame(animateCursor)
}

function handleEnter(el: HTMLElement) {
  if (!pointer.value) return
  hoveredEl = el; hoverRect = el.getBoundingClientRect()
  const width = hoverRect.width + 10
  const height = hoverRect.height + 10
  const isRound = Math.abs(hoverRect.width - hoverRect.height) < 10
  animateMotion(pointer.value, { width, height, borderRadius: isRound ? '50%' : '12px',
    backgroundColor: 'rgba(255,255,255,0.12)' }, { duration: 0.25, easing: 'ease-out' })
  followActive = true
  let lastX = 0, lastY = 0
  const follow = () => {
    if (!hoveredEl || !followActive || !hoverRect) return
    const tx = localX * 0.1, ty = localY * 0.1
    lastX += (tx - lastX) * 0.15; lastY += (ty - lastY) * 0.15
    hoveredEl.style.transform = `translate(${lastX}px, ${lastY}px)`
    requestAnimationFrame(follow)
  }
  requestAnimationFrame(follow)
}

function handleLeave(el?: HTMLElement) {
  if (!pointer.value) return
  followActive = false; hoveredEl = null; hoverRect = null
  localX = 0; localY = 0; el && (el.style.transform = 'translate(0, 0)')
  animateMotion(pointer.value, {
    width: 12, height: 12, borderRadius: '50%',
    backgroundColor: 'rgba(255,255,255,1)'
  }, { duration: 0.25, easing: 'ease-out' })
}

function handleClick() {
  if (!pointer.value) return
  requestAnimationFrame(() => animate(pointer.value!, { scale: [1, 0.85, 1.15, 1] } as any, {
    duration: 0.35, easing: 'ease-out'
  }))
}

const onDelegatedOver = (e: Event) => {
  const t = e.target as HTMLElement
  if (!(t instanceof HTMLElement)) return
  const el = t.closest(SELECTOR) as HTMLElement | null
  if (el && el !== hoveredEl) handleEnter(el)
}

const onDelegatedOut = (e: Event) => {
  const to = (e as MouseEvent).relatedTarget as HTMLElement | null
  if (!hoveredEl) return
  if (!to || !hoveredEl.contains(to)) handleLeave(hoveredEl)
}

onMounted(() => {
  if (!props.enabled) return
  document.body.classList.add('cursor-active')
  document.addEventListener('mousemove', onMove, { passive: true })
  document.addEventListener('mouseover', onDelegatedOver, true)
  document.addEventListener('mouseout', onDelegatedOut, true)
  document.addEventListener('mousedown', handleClick)
  animateCursor()
})

onUnmounted(() => {
  document.body.classList.remove('cursor-active')
  document.removeEventListener('mousemove', onMove)
  document.removeEventListener('mouseover', onDelegatedOver, true)
  document.removeEventListener('mouseout', onDelegatedOut, true)
  document.removeEventListener('mousedown', handleClick)
})

router.afterEach(() => handleLeave())
</script>

<template>
  <ClientOnly>
    <div ref="pointer" data-ios-cursor
      class="fixed top-0 left-0 z-[99999] h-3 w-3 rounded-full bg-white will-change-transform shadow-[0_0_6px_rgba(0,0,0,0.25)]"
      style="pointer-events:none;user-select:none;-webkit-user-drag:none;mix-blend-mode:normal;"
    />
  </ClientOnly>
</template>
```
::

### 3. Подключение в `app.vue`

::code-collapse{title="Подключение компонента в app.vue"}

```vue
<script setup lang="ts">
const config = useRuntimeConfig()
const route = useRoute()
</script>

<template>
  <UApp>
    <NuxtLayout>
      <UMain>
        <NuxtPage />
      </UMain>
    </NuxtLayout>

    <IosPointer :enabled="config.public.iosPointerEnabled && route.meta.iosPointer !== false" />
  </UApp>
</template>
```
::

### 4. Стилизация курсора

::code-collapse{title="app/assets/css/cursor.css"}

```css
body.cursor-active,
body.cursor-active a,
body.cursor-active button,
body.cursor-active [role='button'],
body.cursor-active .clickable {
  cursor: none !important;
}

[data-ios-cursor] {
  position: fixed;
  top: 0;
  left: 0;
  z-index: 2147483647;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background-color: white;
  pointer-events: none !important;
  isolation: isolate;
  view-transition-name: none !important;
}

::view-transition-group(root),
::view-transition-image-pair(root),
::view-transition-old(root),
::view-transition-new(root) {
  pointer-events: none !important;
}
```
::

::/steps

---

## Проблемы и решения

::callout{type="warning" icon="i-lucide-alert-triangle"}
**Дребезг на карточках блога** — курсор «дергался» при наведении на элементы `UBlogPost` из-за вложенных `a` и `button`.  
Решение — делегирование событий `mouseover` / `mouseout` с проверкой `closest()`.
::

::callout{type="info" icon="i-lucide-refresh-cw"}
**Сброс формы курсора при навигации** реализован через `router.afterEach`, чтобы при переходе на новую страницу он возвращался к исходному виду.
::

::callout{type="neutral" icon="i-lucide-sun-moon"}
**Проблема с ViewTransition**: системный курсор появлялся во время анимации смены темы.  
Исправлено за счёт скрытия системного курсора через `html, body, ::view-transition-* { cursor: none !important }`.
::

---

## Вывод

Реализация iOS‑Pointer курсора добавляет интерактивности без потери производительности.  
Компонент не мешает событиям, корректно реагирует на навигацию и смену темы, а также может быть легко включён только для выбранных страниц:

```ts
definePageMeta({ iosPointer: true })
```

---

::badge{label="Nuxt 4" color="primary"}::badge{label="Motion One"}::badge{label="Nuxt UI v4" color="success"}
