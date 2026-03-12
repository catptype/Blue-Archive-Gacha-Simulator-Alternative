<script setup lang="ts">
  import aronaImage from '@/assets/arona.png'; // Vite handles the path aliasing '@' to '/src'
  import SvgCheckMark from '@/components/base/SvgCheckMark.vue';
  import SvgInfoMark from '@/components/base/SvgInfoMark.vue';

  const features = [
    { label: 'Gacha Simulator', desc: 'with pick-up rates similar to the mobile game.' },
    { label: 'User account', desc: 'for tracking information such as collections and achievements.' },
    { label: 'Student Collection', desc: 'in the current game version.' },
    { label: 'Guest Mode', desc: 'Jump right in and test your luck instantly.' },
    { label: 'Open Source', desc: 'A passion hobby project for learning and sharing.' },
  ];
</script>

<template>
  <div class="lg:col-span-3 flex flex-col p-6 bg-slate-900/50 backdrop-blur-lg border border-slate-700 rounded-lg shadow-2xl">
    
    <!-- Header section -->
    <div class="flex items-center mb-6 gap-4">
      <div class="relative shrink-0 w-24 h-24 overflow-hidden rounded-full border-2 border-cyan-400/50">
        <img class="absolute top-0 left-0 object-cover w-full h-full" :src="aronaImage" alt="Arona">
      </div>
      <h1 class="text-4xl font-bold text-white tracking-wide">Welcome, Sensei!</h1>
    </div>

    <!-- Introduction paragraph -->
    <p class="text-lg text-slate-300 font-light">
      An unofficial web application, serving as a Gacha Simulator for the mobile game Blue Archive, developed by Nexon Games and published by Yostar (Japan) and Nexon (Global). Experience the gacha, test your luck, and have fun without spending any Pyroxene.
    </p>

    <!-- Disclaimer Callout -->
    <div class="mt-2 p-2 bg-blue-900/30 border-l-4 border-cyan-500 rounded-r-lg flex items-start gap-3">
      <SvgInfoMark/>
      <div class="text-sm text-slate-300">
        <strong class="font-semibold text-white">Disclaimer:</strong> This is a fan-made, non-profit hobby project created purely for fun and educational purposes. It is not affiliated with, authorized, or endorsed by Nexon Games or Yostar.
      </div>
    </div>
    
    <!-- Features section -->
    <h2 class="mt-8 mb-3 text-2xl font-semibold text-white border-b-2 border-cyan-400/30 pb-2">Features</h2>
      <ul class="space-y-2 text-slate-300">
        <li v-for="item in features" :key="item.label" class="flex items-start gap-3">
          <SvgCheckMark/>
          <span><strong>{{ item.label }}:</strong> {{ item.desc }}</span>
        </li>
      </ul>
  </div>
</template>