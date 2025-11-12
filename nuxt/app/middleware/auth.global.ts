// export default defineNuxtRouteMiddleware(async (to) => {
// 	const { accessToken } = useAuth();
// 	const publicRoutes = ['/login', '/register'];

// 	if (!accessToken.value) {
// 		try {
// 			// пробуем обновить access_token из refresh_token-куки
// 			const res: any = await $fetch('http://localhost:5050/auth/refresh/', {
// 				method: 'POST',
// 				credentials: 'include',
// 				headers: useRequestHeaders(['cookie']), // важно для SSR
// 			});
// 			accessToken.value = res.access_token;
// 		} catch {
// 			accessToken.value = null;
// 		}
// 	}

// 	if (!accessToken.value && !publicRoutes.includes(to.path)) {
// 		return navigateTo('/login');
// 	}
// });

export default defineNuxtRouteMiddleware((to, from) => {
	// Middleware временно отключено
});
