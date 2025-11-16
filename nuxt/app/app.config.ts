export default defineAppConfig({
	global: {
		picture: {
			dark: '/s3/blog/hero_3.jpg',
			light: '/s3/blog/hero_3.jpg',
			alt: 'My profile picture',
		},
		meetingLink: 'https://cal.com/',
		email: 'i@abushin.ru',
		available: true,
	},
	ui: {
		prose: {
			h1: {
				slots: {
					base: 'scroll-m-20 text-4xl font-extrabold tracking-tight lg:text-5xl',
				},
			},
			p: {
				base: 'leading-7 [&:not(:first-child)]:mt-6',
			},
			codeCollapse: {
				slots: {
					root: 'relative [&_pre]:h-[200px]',
					footer:
						'h-16 absolute inset-x-px bottom-px rounded-b-md flex items-center justify-center',
					trigger: 'group',
					triggerIcon: 'group-data-[state=open]:rotate-180',
				},
				variants: {
					open: {
						true: {
							root: '[&_pre]:h-auto [&_pre]:min-h-[200px] [&_pre]:max-h-[80vh] [&_pre]:pb-12',
						},
						false: {
							root: '[&_pre]:overflow-hidden',
							footer: 'bg-gradient-to-t from-muted',
						},
					},
				},
			},
		},
		colors: {
			primary: 'purple',
			neutral: 'neutral',
		},
		pageHero: {
			slots: {
				container: 'py-18 sm:py-24 lg:py-32 gap-1 sm:gap-y-2',
				title: 'mx-auto max-w-xl text-pretty text-3xl sm:text-4xl lg:text-5xl',
				description:
					'mt-2 text-md mx-auto max-w-2xl text-pretty sm:text-md text-muted',
			},
		},
	},
	footer: {
		credits: `Built with Nuxt UI • © ${new Date().getFullYear()}`,
		colorMode: false,
		links: [
			{
				icon: 'i-simple-icons-discord',
				to: 'https://go.nuxt.com/discord',
				target: '_blank',
				'aria-label': 'Nuxt on Discord',
			},
			{
				icon: 'i-simple-icons-x',
				to: 'https://go.nuxt.com/x',
				target: '_blank',
				'aria-label': 'Nuxt on X',
			},
			{
				icon: 'i-simple-icons-github',
				to: 'https://github.com/nuxt/ui',
				target: '_blank',
				'aria-label': 'Nuxt UI on GitHub',
			},
		],
	},
});
