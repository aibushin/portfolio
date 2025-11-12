export default {
	darkMode: 'class',
	content: [
		'./app/**/*.{vue,js,ts}',
		'./components/**/*.{vue,js,ts}',
		'./layouts/**/*.vue',
		'./pages/**/*.vue',
		'./content/**/*.{md,yml,json}',
		'./app.vue',
		'./assets/css/**/*.{css}',
	],
	theme: {
		extend: {
			typography: (theme) => ({
				DEFAULT: {
					css: {
						/* --- Общие стили статьи --- */
						color: 'var(--ui-foreground)',
						a: {
							color: 'var(--ui-primary)',
							'&:hover': { color: 'var(--ui-primary-hover)' },
							textDecoration: 'underline',
						},
						p: {
							marginTop: theme('spacing.4'),
							marginBottom: theme('spacing.4'),
							lineHeight: theme('lineHeight.relaxed'),
						},
						h2: {
							color: 'var(--ui-foreground)',
							fontWeight: '600',
							marginTop: theme('spacing.8'),
							marginBottom: theme('spacing.4'),
						},
						ul: { paddingLeft: theme('spacing.6') },
						li: { marginTop: theme('spacing.2') },
						code: {
							backgroundColor: 'var(--ui-muted)',
							color: 'var(--ui-error)',
							borderRadius: theme('borderRadius.md'),
							padding: '0.2em 0.4em',
						},

						/* --- Стили для alert-блоков --- */
						'.success': {
							backgroundColor:
								'color-mix(in srgb, var(--ui-success) 15%, transparent)',
							borderLeft: `4px solid var(--ui-success)`,
							padding: theme('spacing.4'),
							borderRadius: theme('borderRadius.lg'),
							margin: `${theme('spacing.6')} 0`,
						},
						'.warning': {
							backgroundColor:
								'color-mix(in srgb, var(--ui-warning) 15%, transparent)',
							borderLeft: `4px solid var(--ui-warning)`,
							padding: theme('spacing.4'),
							borderRadius: theme('borderRadius.lg'),
							margin: `${theme('spacing.6')} 0`,
						},
						'.danger': {
							backgroundColor:
								'color-mix(in srgb, var(--ui-error) 15%, transparent)',
							borderLeft: `4px solid var(--ui-error)`,
							padding: theme('spacing.4'),
							borderRadius: theme('borderRadius.lg'),
							margin: `${theme('spacing.6')} 0`,
						},
					},
				},
				invert: {
					css: {
						color: 'var(--ui-foreground)',
						code: {
							backgroundColor: 'var(--ui-card)',
							color: 'var(--ui-warning)',
						},

						'.success': {
							backgroundColor:
								'color-mix(in srgb, var(--ui-success) 10%, transparent)',
							borderLeft: `4px solid var(--ui-success)`,
						},
						'.warning': {
							backgroundColor:
								'color-mix(in srgb, var(--ui-warning) 10%, transparent)',
							borderLeft: `4px solid var(--ui-warning)`,
						},
						'.danger': {
							backgroundColor:
								'color-mix(in srgb, var(--ui-error) 10%, transparent)',
							borderLeft: `4px solid var(--ui-error)`,
						},
					},
				},
			}),
		},
	},
	plugins: [require('@tailwindcss/typography')],
};
