import { defineTransformer } from '@nuxt/content'

console.log('✔ test transformer loaded')

export default defineTransformer({
    name: 'test-transformer',
    extensions: ['.md'],
    transform(file) {
        console.log('[test-transformer] running on', file)

        // // Добавляем параграф в начало статьи
        // if (file.body && Array.isArray(file.body.children)) {
        //     file.body.children.unshift({
        //         type: 'element',
        //         tag: 'p',
        //         props: {},
        //         children: [{ type: 'text', value: '⚡ injected by transformer ⚡' }]
        //     })
        // }

        // Меняем title для надёжности
        return {
            ...file,
            title: (file.title || 'Untitled') + ' ⚡',
        }
    }
})
