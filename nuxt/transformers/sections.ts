import { defineTransformer } from '@nuxt/content'

export default defineTransformer({
    name: 'nested-headings-simple',
    extensions: ['.md'],
    transform(file) {
        console.log("Оригинальный file.body.value:", file.body.value)

        const body = file.body
        if (!body || body.type !== 'minimark' || !Array.isArray(body.value)) return file

        const wrap = (heading: any, lvl: number) => [
            'div',
            { class: `level-${lvl}` },
            heading,
        ]

        const stack: [any[], number][] = []
        const result: any[] = []

        const pushNode = (node: any) => {
            if (stack.length) stack[stack.length - 1][0].push(node)
            else result.push(node)
        }

        for (const node of body.value) {
            if (Array.isArray(node)) {
                const [tag] = node
                const match = /^h([2-6])$/.exec(tag)

                if (match) {
                    const lvl = Number(match[1])

                    // Закрываем все блоки >= текущего уровня
                    while (stack.length && stack[stack.length - 1][1] >= lvl) {
                        const [block] = stack.pop()!
                        pushNode(block)
                    }

                    const block = wrap(node, lvl)
                    stack.push([block, lvl])
                    continue
                }
            }
            pushNode(node)
        }

        while (stack.length) {
            const [block] = stack.pop()!
            pushNode(block)
        }

        file.body.value = result

        console.log("file.body.value в результате работы трансформера:", file.body.value)
        return file
    },
})
