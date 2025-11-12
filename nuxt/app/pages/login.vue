<template>
  <div class="flex items-center justify-center min-h-screen bg-gray-100">
    <div class="w-full max-w-md bg-white p-6 rounded-2xl shadow">
      <h1 class="text-2xl font-bold mb-4 text-center">Вход</h1>

      <form class="space-y-4" @submit.prevent="handleLogin">
        <div>
          <label class="block mb-1 text-sm font-medium">Email</label>
          <input
            v-model="email"
            type="email"
            class="w-full border rounded-lg px-3 py-2"
            required
          />
        </div>

        <div>
          <label class="block mb-1 text-sm font-medium">Пароль</label>
          <input
            v-model="password"
            type="password"
            class="w-full border rounded-lg px-3 py-2"
            required
          />
        </div>

        <button
          type="submit"
          class="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition"
        >
          Войти
        </button>
      </form>

      <p v-if="error" class="text-red-500 text-sm mt-4 text-center">
        {{ error }}
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
const email = ref("i@abushin.ru");
const password = ref("3opmp10103A-");
const error = ref("");
const { accessToken } = useAuth();

const handleLogin = async () => {
  error.value = "";
  try {
    const res: any = await $fetch("http://localhost:5050/auth/login/", {
      method: "POST",
      body: new URLSearchParams({
        username: email.value,
        password: password.value,
      }),
      credentials: "include",
    });

    accessToken.value = res.access_token;
    await navigateTo("/");
  } catch (err: any) {
    error.value = err?.data?.detail || "Ошибка авторизации";
  }
};
</script>
