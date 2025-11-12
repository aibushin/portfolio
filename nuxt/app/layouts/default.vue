<script setup lang="ts"></script>

<template>
	<div>
		<UContainer class="border-default pt-10 sm:border-x">
			<AppHeader :links="navLinks" />
			<slot />
			<AppFooter />
		</UContainer>
	</div>
</template>
