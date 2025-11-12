// composables/useIntersectionObserver.ts
import { ref, onMounted, onBeforeUnmount } from 'vue'

export function useIntersectionObserver(
    options: IntersectionObserverInit = { threshold: 0.1 }
) {
    const isVisible = ref(false)
    const target = ref<HTMLElement | null>(null)
    let observer: IntersectionObserver | null = null

    onMounted(() => {
        if (target.value) {
            observer = new IntersectionObserver((entries) => {
                if (entries[0].isIntersecting) {
                    isVisible.value = true
                    observer?.disconnect()
                }
            }, options)

            observer.observe(target.value)
        }
    })

    onBeforeUnmount(() => {
        observer?.disconnect()
    })

    return { isVisible, target }
}
