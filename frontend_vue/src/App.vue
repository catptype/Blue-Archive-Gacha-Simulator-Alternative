<script setup lang="ts">
import Background from './components/Background.vue';
import Navbar from './components/Navbar.vue';
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