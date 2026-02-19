<script setup lang="ts">
import { onMounted } from 'vue';
import { useAuthStore } from '@/security/auth';
import Background from '@/components/Background.vue';
import Navbar from '@/components/Navbar.vue';
import ToastContainer from '@/components/toasts/Container.vue';

onMounted(() => {
  const authStore = useAuthStore();
  // If a token exists in localStorage from a previous session,
  // this will validate it with the backend.
  authStore.fetchUser();
});
</script>

<template>
  <div class="relative min-h-screen w-full bg-black">
    <!-- Background -->
    <Background />

    <!-- Navbar -->
    <Navbar />

    <!-- Views -->
    <router-view class="min-h-screen w-full pt-20 mx-auto"/>

    <!-- Toast Notification -->
    <ToastContainer />
  </div>
</template>