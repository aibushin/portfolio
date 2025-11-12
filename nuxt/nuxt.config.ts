export default defineNuxtConfig({
	// debug: true,
	runtimeConfig: {
		public: {
			backendURL: process.env.BACKEND_URL,
		},
	},

	modules: [
		'@nuxt/eslint',
		'@nuxt/ui',
		'@nuxt/content',
		'@nuxt/image',
		'@vueuse/nuxt',
		'nuxt-og-image',
		'motion-v/nuxt',
	],

	image: {
		domains: ['s3.twcstorage.ru'],
		alias: {
			s3: 'https://s3.twcstorage.ru/bca1d335-310481f2-d271-4185-ab38-48a49fcdd7ce/aibushin/nuxt',
		},
	},

	css: ['~/assets/css/main.css'],

	compatibilityDate: '2025-08-31',

	nitro: {
		prerender: {
			routes: ['/'],
			crawlLinks: true,
		},
	},

	content: {
		watch: {
			port: 4000,
			showURL: true,
		},
		build: {
			markdown: {
				highlight: {
					theme: {
						// Default theme (same as single string)
						default: 'github-light',
						// Theme used if `html.dark`
						dark: 'github-dark',
						// Theme used if `html.sepia`
						sepia: 'monokai',
					},
				},
			},
			// transformers: [
			// 	'~~/transformers/sections',
			// ],
		},
	},

	eslint: {
		config: {
			stylistic: {
				commaDangle: 'never',
				braceStyle: '1tbs',
			},
		},
	},
});
