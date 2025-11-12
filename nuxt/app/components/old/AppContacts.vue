<script setup lang="ts">
import * as v from "valibot";
import type { FormSubmitEvent } from "@nuxt/ui";

const schema = v.object({
  name: v.pipe(v.string(), v.minLength(2, "Имя обязательно")),
  email: v.pipe(v.string(), v.email("Некорректный email")),
  message: v.pipe(v.string(), v.minLength(10, "Сообщение должно быть длиннее")),
  agree: v.boolean(),
});

type Schema = v.InferOutput<typeof schema>;

const state = reactive<Schema>({
  name: "",
  email: "",
  message: "",
  agree: false,
});

const loading = ref(false);
const toast = useToast();

async function onSubmit(event: FormSubmitEvent<Schema>) {
  if (!event.data.agree) {
    toast.add({
      title: "Требуется согласие",
      description: "Подтвердите согласие на обработку данных",
      color: "warning",
    });
    return;
  }

  try {
    loading.value = true;
    await $fetch("/api/contact", { method: "POST", body: event.data });
    toast.add({
      title: "Отправлено",
      description: "Спасибо! Я свяжусь с вами.",
      color: "success",
    });
    Object.assign(state, { name: "", email: "", message: "", agree: false });
  } catch (e) {
    toast.add({
      title: "Ошибка",
      description: "Не удалось отправить сообщение",
      color: "error",
    });
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <section id="contacts" class="py-16">
    <div class="container mx-auto">
      <h2 class="text-3xl font-bold text-center mb-10">Контакты</h2>

      <!-- Кнопки соцсетей -->
      <div class="flex flex-wrap justify-center gap-3 mb-10">
        <UButton
          to="https://github.com/aibushin"
          target="_blank"
          icon="i-simple-icons-github"
          variant="outline"
          label="GitHub"
        />
        <UButton
          to="https://linkedin.com/in/your_linkedin"
          target="_blank"
          icon="i-simple-icons-linkedin"
          color="primary"
          variant="outline"
          label="LinkedIn"
        />
        <UButton
          to="https://t.me/your_telegram"
          target="_blank"
          icon="i-simple-icons-telegram"
          color="primary"
          variant="outline"
          label="Telegram"
        />
        <UButton
          as="a"
          href="mailto:you@example.com"
          icon="i-heroicons-envelope"
          color="neutral"
          variant="outline"
          label="Email"
        />
      </div>

      <!-- Форма -->
      <UCard>
        <template #header>
          <h3 class="text-xl font-semibold">Написать мне</h3>
        </template>

        <UForm
          :schema="schema"
          :state="state"
          class="grid gap-4 md:grid-cols-2"
          @submit="onSubmit"
        >
          <UFormField label="Имя" name="name" class="col-span-1">
            <UInput v-model="state.name" placeholder="Ваше имя" />
          </UFormField>

          <UFormField label="Email" name="email" class="col-span-1">
            <UInput v-model="state.email" type="email" placeholder="you@example.com" />
          </UFormField>

          <UFormField label="Сообщение" name="message" class="col-span-2">
            <UTextarea
              v-model="state.message"
              :rows="6"
              placeholder="Коротко опишите вопрос"
            />
          </UFormField>

          <div class="col-span-2 flex items-center gap-2">
            <UCheckbox v-model="state.agree" />
            <span class="text-sm">Соглашаюсь на обработку персональных данных</span>
          </div>

          <div class="col-span-2 flex justify-end gap-3">
            <UButton type="reset" variant="outline" color="neutral" label="Сбросить" />
            <UButton
              type="submit"
              :loading="loading"
              icon="i-heroicons-paper-airplane"
              label="Отправить"
            />
          </div>
        </UForm>
      </UCard>
    </div>
  </section>
</template>
