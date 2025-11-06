<script setup lang="ts">
import { onMounted } from 'vue';
import Background from './components/Background.vue';
import Navbar from './components/Navbar.vue';
import { useAuthStore } from './security/auth';

onMounted(() => {
  const authStore = useAuthStore();
  // If a token exists in localStorage from a previous session,
  // this will validate it with the backend.
  authStore.fetchUser();
});
</script>

<template>
  <div class="relative min-h-screen w-full bg-black antialiased">
    <!-- Background -->
    <Background />

    <!-- Navbar -->
    <Navbar />

    <main>
      <router-view />
    </main>

  </div>
</template>