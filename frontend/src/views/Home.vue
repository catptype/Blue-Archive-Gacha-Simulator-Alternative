<script setup lang="ts">
import WelcomePanel from '../components/WelcomePanel.vue';
import HeroVideo from '../components/HeroVideo.vue';
import Footer from '../components/Footer.vue';
</script>

<template>
  <div class="relative z-10 w-full max-w-7xl mx-auto px-4 py-8 pt-30">
    
    <!-- Outer Flex Container -->
    <div class="flex flex-col gap-4">

      <!-- Upper Row Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-5 gap-4">
        
        <WelcomePanel />
        
        <HeroVideo />

      </div>

      <!-- Footer Row -->
      <Footer />
      
    </div>
  </div>
</template>

