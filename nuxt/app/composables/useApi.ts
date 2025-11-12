export const useApi = () => {
	const { accessToken } = useAuth();

	const apiFetch = async <T>(url: string, opts: any = {}): Promise<T> => {
		try {
			return await $fetch<T>(url, {
				baseURL: 'http://localhost:5050',
				credentials: 'include',
				headers: {
					...(accessToken.value
						? { Authorization: `Bearer ${accessToken.value}` }
						: {}),
					...opts.headers,
				},
				...opts,
			});
		} catch (err: any) {
			if (err?.response?.status === 401) {
				try {
					const res: any = await $fetch('/auth/refresh/', {
						baseURL: 'http://localhost:5050',
						method: 'POST',
						credentials: 'include',
						headers: useRequestHeaders(['cookie']),
					});
					accessToken.value = res.access_token;

					// повторяем запрос с новым токеном
					return await $fetch<T>(url, {
						baseURL: 'http://localhost:5050',
						credentials: 'include',
						headers: {
							Authorization: `Bearer ${res.access_token}`,
							...opts.headers,
						},
						...opts,
					});
				} catch {
					accessToken.value = null;
					navigateTo('/login');
					throw err; // пробрасываем ошибку дальше
				}
			}
			throw err;
		}
	};

	return { apiFetch };
};
