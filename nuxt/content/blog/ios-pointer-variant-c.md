---
title: "iOS‑Pointer курсор: архитектура, устойчивость и отладка"
description: "Разбор архитектуры: делегирование, фильтрация интерактивных элементов, сброс при навигации, исключение из ViewTransition, устойчивость к SSR/CSR."
date: 2025-10-14
image: /s3/blog/mouse-pointer-icons.avif
tags: ["Nuxt 4", "Nuxt UI", "motion-v", "Architecture", "Debugging"]
---

::callout{type="info"}
Демонстрационный курсор включён метой: `definePageMeta({ iosPointer: true })`.
::

# Архитектурные решения

## Почему делегирование

::callout{type="neutral"}
Компоненты Nuxt UI (например, `UBlogPost`) содержат вложенные слои. Переходы между дочерними узлами без делегирования дают дребезг. Делегирование на документ + `closest(SELECTOR)` устраняют проблему.
::

::code-collapse{title="Фильтрация ложных кликов"}

```ts
function isTrulyClickable(el: HTMLElement): boolean {
  return !(el.tagName === 'A' && el.children.length === 1
    && el.children[0].tagName === 'SPAN'
    && el.children[0].classList.contains('absolute'))
}
```

::

## Сброс состояния при навигации

::callout{type="info"}
`router.afterEach(() => handleLeave())` гарантирует «чистый» курсор на новой странице, даже если `pointerleave` не успел сработать.
::

## Исключение из ViewTransition

::code-collapse{title="CSS для исключения кастомного слоя из snapshot"}

```css
[data-ios-cursor] { view-transition-name: none !important; }
```

::

## Полный компонент и интеграция

::code-collapse{title="Подключение в app/app.vue"}

```vue
<IosPointer :enabled="useRuntimeConfig().public.iosPointerEnabled && useRoute().meta.iosPointer !== false" blendMode="difference" />
```

::

::code-collapse{title="app/assets/css/cursor.css"}

```css
/* см. полный вариант в руководстве A */
```

::

## Отладка

::callout{type="warning"}
При уходе указателя за пределы окна убеждаться, что обработчики проверяют типы: `if (!(e.target instanceof HTMLElement)) return`.
::

::callout{type="success"}
Для плавности держать анимационный цикл в одном `requestAnimationFrame` и не смешивать с CSS-трансишнами позиции.
::

::badge{label="Nuxt 4" color="primary"}::badge{label="Nuxt UI v4" color="success"}::badge{label="motion-v@1.7.2"}
