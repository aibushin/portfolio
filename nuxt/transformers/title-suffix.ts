import { defineTransformer } from '@nuxt/content'

console.log('✅ title-suffix transformer loaded')

export default defineTransformer({
  name: 'title-suffix',
  extensions: ['.md'],
  transform(file) {
    console.log('[title-suffix] running on', file.id)
    return {
      ...file,
      title: file.title ? file.title + ' (suffix)' : file.title,
    }
  },
})
