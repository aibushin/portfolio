---
title: "iOS‑Pointer курсор для Nuxt 4: полное руководство"
description: "Пошаговая реализация кастомного курсора на motion-v с делегированием событий, сбросом состояния при навигации и поддержкой ViewTransition."
date: 2025-10-14
image: /s3/blog/mouse-pointer-icons.avif
tags: ["Nuxt 4", "Nuxt UI", "motion-v", "Frontend", "UX",]
features:
  - iosPointer
---

::callout{type="info" icon="i-lucide-mouse-pointer"}
Для этой страницы кастомный курсор включён через `definePageMeta({ iosPointer: true })`, чтобы продемонстрировать поведение на практике.
::

# Кастомный iOS‑Pointer курсор для Nuxt 4

Курсор в стиле iPadOS создаёт иллюзию «прилипания» к интерактивным элементам: указатель мягко следует за мышью, меняет размер и форму при наведении, а элементы слегка смещаются к координате курсора (магнитный эффект). Все примеры совместимы с **nuxt@4.1.2**, **Nuxt UI v4**, **@nuxt/content 3** и **motion-v@1.7.2**.

---

## Установка и включение

::steps

### 1) Установка зависимостей

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

Добавить модули в `nuxt.config.ts`:

```ts
export default defineNuxtConfig({
  modules: ['@nuxt/ui', '@nuxt/content']
})
```

### 2) Включение курсора только там, где требуется

Глобальный компонент можно держать выключенным по умолчанию и включать его на отдельных страницах:

```ts
// Внутри *.vue страницы статьи
definePageMeta({ iosPointer: true })
```

::

---

## Компонент курсора

::code-collapse{title="Полный код app/components/IosPointer.vue (с комментариями)"}

```vue
<script setup lang="ts">
import { animate } from 'motion-v'          // Библиотека анимаций (Vue-обёртка)
const router = useRouter()
const colorMode = useColorMode()

/**
 * Курсор по умолчанию выключен. Включается пропсом enabled.
 * Это позволяет подключать компонент глобально, но управлять видимостью через конфиг/мету.
 */
const props = defineProps({
  enabled: { type: Boolean, default: false },
  blendMode: { type: String, default: 'normal' }, // Можно задать 'difference' для контрастного режима
})

/** Ссылки на DOM и состояние */
const pointer = ref<HTMLElement | null>(null)
const pos = reactive({ x: 0, y: 0 })     // Текущая позиция курсора (с инерцией)
const target = reactive({ x: 0, y: 0 })  // Целевая позиция (реальные координаты мыши)

let hoveredEl: HTMLElement | null = null
let hoverRect: DOMRect | null = null
let followActive = false                 // Флаг «магнитного» эффекта

/** Селектор интерактивных элементов (без вложенных абсолютных спанов) */
const SELECTOR = 'a, button, [role="button"], .clickable, [data-cursor]'

/** Обёртка над motion для компактности */
function animateMotion(el: Element, props: Record<string, any>, options: Record<string, any> = {}) {
  return animate(el, props as any, { duration: 0.25, easing: 'ease-out', ...options })
}

/** Обработчик перемещения указателя — обновляет целевые координаты */
function onMove(e: MouseEvent) {
  target.x = e.clientX
  target.y = e.clientY
}

/**
 * Главный анимационный цикл — плавно подтягивает pos к target (инерция),
 * выставляет translate у визуального слоя курсора.
 */
function loop() {
  if (!props.enabled) return
  if (!pointer.value) { requestAnimationFrame(loop); return }

  pos.x += (target.x - pos.x) * 0.25
  pos.y += (target.y - pos.y) * 0.25

  const w = pointer.value.offsetWidth / 2
  const h = pointer.value.offsetHeight / 2

  pointer.value.style.translate = `${pos.x - w}px ${pos.y - h}px`
  requestAnimationFrame(loop)
}

/**
 * Вход на кликабельный элемент:
 * 1) сохраняет ссылку и прямоугольник элемента
 * 2) увеличивает курсор под размер элемента
 * 3) включает «магнитный» сдвиг самого элемента
 */
function handleEnter(el: HTMLElement) {
  if (!pointer.value) return
  hoveredEl = el
  hoverRect = el.getBoundingClientRect()

  const width = hoverRect.width + 10
  const height = hoverRect.height + 10
  const isRound = Math.abs(hoverRect.width - hoverRect.height) < 10

  animateMotion(pointer.value, {
    width, height,
    borderRadius: isRound ? '50%' : '12px',
    backgroundColor: 'rgba(255,255,255,0.12)',
  })

  // «Магнитный» эффект — небольшой сдвиг самого элемента к курсору
  followActive = true
  let lastX = 0, lastY = 0
  const follow = () => {
    if (!hoveredEl || !followActive || !hoverRect) return
    const localX = target.x - (hoverRect.left + hoverRect.width / 2)
    const localY = target.y - (hoverRect.top + hoverRect.height / 2)
    const tx = localX * 0.1, ty = localY * 0.1
    lastX += (tx - lastX) * 0.15
    lastY += (ty - lastY) * 0.15
    hoveredEl.style.transform = `translate(${lastX}px, ${lastY}px)`
    requestAnimationFrame(follow)
  }
  requestAnimationFrame(follow)
}

/**
 * Выход с кликабельного элемента:
 * 1) отключает «магнит» и возвращает трансформацию
 * 2) возвращает курсор к базовой круглой форме
 */
function handleLeave(el?: HTMLElement | null) {
  if (!pointer.value) return
  followActive = false
  if (hoveredEl) hoveredEl.style.transform = ''
  hoveredEl = null
  hoverRect = null

  animateMotion(pointer.value, {
    width: 12, height: 12, borderRadius: '50%', backgroundColor: 'rgba(255,255,255,1)'
  })
}

/** Короткий «bounce» на mousedown — чисто визуальный отклик */
function handleClick() {
  if (!pointer.value) return
  requestAnimationFrame(() => {
    animate(pointer.value!, { scale: [1, 0.9, 1] } as any, { duration: 0.25, easing: 'ease-out' })
  })
}

/** Безопасная фильтрация «ложных» ссылок (внутренние абсолютные спаны и т.п.) */
function isTrulyClickable(el: HTMLElement): boolean {
  if (
    el.tagName === 'A' &&
    el.children.length === 1 &&
    el.children[0].tagName === 'SPAN' &&
    el.children[0].classList.contains('absolute')
  ) return false
  return true
}

/** Делегированное наведение — устойчиво работает на вложенных структурах Nuxt UI */
function onPointerEnter(e: PointerEvent) {
  const t = e.target as HTMLElement | null
  if (!t || !(t instanceof HTMLElement)) return
  const el = t.closest(SELECTOR) as HTMLElement | null
  if (!el || !isTrulyClickable(el)) return
  if (hoveredEl === el) return
  handleEnter(el)
}

function onPointerLeave(e: PointerEvent) {
  const t = e.target as HTMLElement | null
  if (!t || !(t instanceof HTMLElement)) return
  const el = t.closest(SELECTOR) as HTMLElement | null
  if (!el || !isTrulyClickable(el)) return
  const to = (e.relatedTarget as HTMLElement) || null
  if (to && el.contains(to)) return
  if (hoveredEl && el === hoveredEl) handleLeave(el)
}

/** Сброс формы курсора после навигации — на новой странице курсор всегда «чистый» */
router.afterEach(() => {
  if (!props.enabled) return
  handleLeave()
})

/** Инициализация и подписки */
onMounted(() => {
  if (!props.enabled) { document.body.classList.remove('cursor-active'); return }
  document.body.classList.add('cursor-active')

  // Перенос визуального слоя в <body>, чтобы исключить попадание в ViewTransition snapshot
  if (pointer.value && pointer.value.parentNode !== document.body) document.body.appendChild(pointer.value)

  // Слушатели указателя:
  document.addEventListener('pointermove', onMove, { passive: true })
  document.addEventListener('pointerdown', handleClick)
  document.addEventListener('pointerenter', onPointerEnter, true)
  document.addEventListener('pointerleave', onPointerLeave, true)

  loop()

  // Плавное появление
  requestAnimationFrame(() => { if (pointer.value) pointer.value.style.opacity = '1' })
})

/** Очистка */
onUnmounted(() => {
  document.body.classList.remove('cursor-active')
  document.removeEventListener('pointermove', onMove)
  document.removeEventListener('pointerdown', handleClick)
  document.removeEventListener('pointerenter', onPointerEnter, true)
  document.removeEventListener('pointerleave', onPointerLeave, true)
})

/** Цвет заливки по теме (при желании можно заменить на CSS-переменные) */
const pointerColor = computed(() => colorMode.value === 'dark' ? 'bg-white' : 'bg-black')
</script>

<template>
  <ClientOnly>
    <div
      ref="pointer"
      data-ios-cursor
      :class="['fixed top-0 left-0 z-[2147483647] h-3 w-3 rounded-full', pointerColor, 'will-change-transform hidden md:block']"
      :style="{
        opacity: 0,
        transition: 'opacity 0.3s ease-out',
        pointerEvents: 'none',
        userSelect: 'none',
        WebkitUserDrag: 'none',
        touchAction: 'none',
        mixBlendMode: blendMode
      }"
    />
  </ClientOnly>
</template>
```

::

---

## Подключение в приложение

::code-collapse{title="Подключение в app/app.vue с пояснениями"}

```vue
<script setup lang="ts">
// 1) Читаем публичный флаг из конфига: включать ли кастомный курсор глобально
const config = useRuntimeConfig()
// 2) Читаем метаданные текущего маршрута — так можно включать курсор точечно (на конкретных страницах)
const route = useRoute()
</script>

<template>
  <UApp>
    <NuxtLayout>
      <UMain>
        <NuxtPage />
      </UMain>
    </NuxtLayout>

    <!-- Курсор отрисовывается глобально, но включается только если:
         - глобальный флаг включён (NUXT_PUBLIC_IOS_POINTER_ENABLED=true)
         - и текущая страница не отключила его через meta -->
    <IosPointer :enabled="config.public.iosPointerEnabled && route.meta.iosPointer !== false" blendMode="difference" />
  </UApp>
</template>
```

::

---

## Стили

::code-collapse{title="app/assets/css/cursor.css — комментарии и правила"}

```css
/* Системный курсор скрывается ТОЛЬКО когда на <body> висит класс .cursor-active */
body.cursor-active,
body.cursor-active a,
body.cursor-active button,
body.cursor-active [role='button'],
body.cursor-active .clickable {
  cursor: none !important;
}

/* Сам кастомный курсор — изолированный fixed-слой поверх всего */
[data-ios-cursor] {
  position: fixed;
  top: 0; left: 0;
  z-index: 2147483647;
  width: 12px; height: 12px;
  border-radius: 9999px;
  pointer-events: none !important;
  isolation: isolate;
  view-transition-name: none !important; /* исключение из ViewTransition snapshot */
}

/* Слои ViewTransition не должны блокировать клики */
::view-transition-group(root),
::view-transition-image-pair(root),
::view-transition-old(root),
::view-transition-new(root) {
  pointer-events: none !important;
}
```

::

::callout{type="info" icon="i-lucide-file-code"}
Подключение файла в основной CSS проекта: добавить строку `@import './cursor.css';` в `app/assets/css/main.css` (или аналогичный входной файл стилей).
::

---

## Отладка и типичные проблемы

::callout{type="warning" icon="i-lucide-alert-triangle"}
Дребезг на карточках блога (`UBlogPost`): возникает из-за вложенных абсолютных спанов. Делегирование событий через `closest()` и фильтрация в `isTrulyClickable()` устраняют ложные срабатывания.
::

::callout{type="info" icon="i-lucide-refresh-cw"}
Сброс формы курсора при навигации: добавлен `router.afterEach(() => handleLeave())`, чтобы на новой странице курсор всегда возвращался к базовой форме.
::

::callout{type="neutral" icon="i-lucide-sun-moon"}
ViewTransition и смена темы: системный курсор мог появляться на время анимации. Решается принудительным скрытием курсора через `body.cursor-active` и исключением слоя курсора из snapshot (`view-transition-name: none`).
::

---

## Итог

Курсор в стиле iOS‑Pointer добавляет заметную тактильность и не мешает интерактивности.  
Компонент управляется через флаг и метаданные страницы, корректно работает с Nuxt UI и Nuxt Content и не конфликтует с ViewTransition.

::badge{label="Nuxt 4" color="primary"}::badge{label="Nuxt UI v4" color="success"}::badge{label="motion-v@1.7.2"}
