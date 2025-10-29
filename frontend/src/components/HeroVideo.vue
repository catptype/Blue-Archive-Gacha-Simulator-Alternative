<script setup lang="ts">
import gachaVideo from '../assets/gacha.mov';
</script>

<template>
  <div class="relative lg:col-span-2 w-full min-h-[300px] lg:min-h-0 overflow-hidden bg-slate-900 border border-slate-700 rounded-lg shadow-2xl">
    <video autoplay muted loop class="absolute top-0 left-0 w-full h-full object-cover z-0">
      <source :src="gachaVideo" type="video/mp4">
      Your browser does not support the video tag.
    </video>
    <div class="absolute inset-0 bg-gradient-to-t from-black/60 via-black/20 to-transparent z-10"></div>
    <div class="absolute inset-0 flex items-center justify-center z-20">
      <h2 class="text-6xl font-black text-white uppercase tracking-widest" style="text-shadow: 2px 2px 10px rgba(0, 0, 0, 0.7);">
        SALTY
      </h2>
    </div>
  </div>
</template>