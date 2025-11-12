export function useScrollTo() {
    // к элементу с id
    const scrollToId = (id: string) => {
        const el = document.getElementById(id)
        if (el) {
            el.scrollIntoView({ behavior: 'smooth', block: 'start' })
        }
    }

    // произвольный селектор
    const scrollToSelector = (selector: string) => {
        const el = document.querySelector(selector)
        if (el) {
            el.scrollIntoView({ behavior: 'smooth', block: 'start' })
        }
    }

    // alias для контактов
    const scrollToContacts = () => scrollToId('contacts')

    return {
        scrollToId,
        scrollToSelector,
        scrollToContacts
    }
}
