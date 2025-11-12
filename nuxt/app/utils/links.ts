import type { NavigationMenuItem } from '@nuxt/ui';

export const navLinks: NavigationMenuItem[] = [
	{
		label: 'Главная',
		icon: 'i-lucide-home',
		to: '/',
	},
	{
		label: 'Проекты',
		icon: 'i-lucide-folder',
		to: '/projects',
	},
	{
		label: 'Блог',
		icon: 'i-lucide-file-text',
		to: '/blog',
	},
	{
		label: 'Выступления',
		icon: 'i-lucide-mic',
		to: '/speaking',
	},
	{
		label: 'Обо мне',
		icon: 'i-lucide-user',
		to: '/about',
	},
];
