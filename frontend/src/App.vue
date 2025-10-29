<script setup lang="ts">
// import HomeView from './views/Home.vue';
import Background from './components/Background.vue';
import Navbar from './components/Navbar.vue';
</script>

<!-- <template>
  <HomeView />
</template> -->

<template>
  <!-- This is your new "base.html" -->
  <div class="relative min-h-screen w-full bg-black antialiased">
    
    <!-- Components that appear on EVERY page -->
    <Background />
    <Navbar />

    <!-- 
      This is the magic component from Vue Router.
      It renders the component for the current route.
      Think of it as the new "{% block body %}"
    -->
    <main>
      <router-view />
    </main>

  </div>
</template>