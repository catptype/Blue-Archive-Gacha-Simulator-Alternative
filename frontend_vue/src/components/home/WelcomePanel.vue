<script setup lang="ts">
import aronaImage from '../../assets/arona.png'; // Vite handles the path aliasing '@' to '/src'
</script>

<template>
  <!-- This panel spans 3 of 5 columns on desktop screens (lg:). -->
  <div class="lg:col-span-3 flex flex-col p-6 bg-slate-900/50 backdrop-blur-lg border border-slate-700 rounded-lg shadow-2xl">
    
    <!-- Header section -->
    <div class="flex items-center mb-6 gap-4">
      <div class="relative flex-shrink-0 w-24 h-24 overflow-hidden rounded-full border-2 border-cyan-400/50">
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
      <div class="flex-shrink-0">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-cyan-400" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" /></svg>
      </div>
      <div class="text-sm text-slate-300">
        <strong class="font-semibold text-white">Disclaimer:</strong> This is a fan-made, non-profit hobby project created purely for fun and educational purposes. It is not affiliated with, authorized, or endorsed by Nexon Games or Yostar.
      </div>
    </div>
    
    <!-- Features section -->
    <h2 class="mt-8 mb-3 text-2xl font-semibold text-white border-b-2 border-cyan-400/30 pb-2">Features</h2>
      <!-- List of application features. -->
      <ul class="space-y-2 text-slate-300">
        <li class="flex items-start gap-3">
          <svg class="w-5 h-5 mt-1 text-cyan-400 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
          <span><strong>Gacha Simulator:</strong> with pick-up rates similar to the mobile game.</span>
        </li>
        <li class="flex items-start gap-3">
          <svg class="w-5 h-5 mt-1 text-cyan-400 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
          <span><strong>User account:</strong> for tracking information such as collections and achievements.</span>
        </li>
        <li class="flex items-start gap-3">
          <svg class="w-5 h-5 mt-1 text-cyan-400 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
          <span><strong>Student Collection:</strong> in the current game version.</span>
        </li>
        <li class="flex items-start gap-3">
          <svg class="w-5 h-5 mt-1 text-cyan-400 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
          <span><strong>Guest Mode:</strong> Jump right in and test your luck instantly.</span>
        </li>
        <li class="flex items-start gap-3">
          <svg class="w-5 h-5 mt-1 text-cyan-400 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
          <span><strong>Open Source:</strong> A passion hobby project for learning and sharing.</span>
        </li>
      </ul>
  </div>
</template>