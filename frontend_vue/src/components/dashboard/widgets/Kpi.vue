<script setup lang="ts">
    import apiClient from '../../../services/client';
    // This component fetches its own data using async setup
    const { data } = await apiClient.get('/dashboard/summary/kpis');
</script>

<template>

<div id="kpi-widget-container" class="mb-6"><!-- This is a partial template containing only the KPI widget's HTML. -->
  <!-- The outer container is a flexbox that will stack on small screens -->
  <div class="flex flex-col gap-4">
      
      <!-- Row 1: Primary Metrics (Total Pulls & Pyroxene) -->
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div class="p-4 bg-slate-700/50 rounded-lg text-center flex flex-col justify-center">
              <div class="text-3xl font-bold">30</div>
              <div class="text-sm text-slate-400">Total Pulls</div>
          </div>
          <div class="sm:col-span-2 p-4 bg-slate-700/50 rounded-lg text-center flex flex-col justify-center">
              <div class="flex items-center justify-center gap-2 text-3xl font-bold">
                  <img src="" class="h-8 w-8">
                  <span>3,600</span>
              </div>
              <div class="text-sm text-slate-400">Pyroxene Spent</div>
          </div>
      </div>

      <!-- Row 2: Rarity Breakdown -->
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div class="p-4 bg-gradient-to-br from-pink-400/50 via-purple-400/50 to-cyan-400/50 rounded-lg text-center">
              <div class="text-3xl font-bold text-white">1</div>
              <div class="text-sm font-semibold text-pink-300">★★★ Students</div>
          </div>
          <div class="p-4 bg-yellow-500/50 rounded-lg text-center">
              <div class="text-3xl font-bold text-white">5</div>
              <div class="text-sm font-semibold text-yellow-300">★★ Students</div>
          </div>
          <div class="p-4 bg-blue-500/50 rounded-lg text-center">
              <div class="text-3xl font-bold text-white">24</div>
              <div class="text-sm font-semibold text-blue-300">★ Students</div>
          </div>
      </div>
  </div>
</div>



  <div class="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
    <div class="p-4 bg-slate-700/50 rounded-lg">
      <p class="text-sm text-slate-400">Total Pulls</p>
      <p class="text-3xl font-bold">{{ data.total_pulls }}</p>
    </div>
    <!-- ... other KPI boxes -->
  </div>
</template>
