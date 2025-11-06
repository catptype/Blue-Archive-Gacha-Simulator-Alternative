<script setup lang="ts">
import backgroundImage from '../assets/background.png'; // Vite handles the path aliasing '@' to '/src'
</script>

<template>
  <div class="absolute inset-0 z-0">

    <!-- The background image is made subtle with opacity and a blur filter. -->
    <img :src="backgroundImage" alt="Background" class="object-cover w-full h-full opacity-30 filter blur-sm">

    <!-- A gradient overlay ensures a smooth fade to black at the bottom. -->
    <div class="absolute inset-0 bg-gradient-to-t from-black via-black/0 to-transparent"></div>
</div>
</template>