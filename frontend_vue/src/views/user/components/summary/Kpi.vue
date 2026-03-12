<script setup lang="ts">
  import { ref } from 'vue';
  import apiClient from '@/services/client';
  import pyroxeneImage from '@/assets/pyroxene.png';
  import StatCard from '../base/StatCard.vue';
  import { type Kpi } from '@/types/web';

  const kpiData = ref<Kpi>( (await apiClient.get('/dashboard/summary/kpis')).data );
  
</script>

<template>
  <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 text-center">
    
    <!-- Uses 'default' theme by default -->
    <StatCard label="Total Pulls" :value="kpiData.total_pulls" />

    <!-- Uses 'default' theme but adds a spanning class -->
    <StatCard 
      label="Pyroxene Spent" 
      class="sm:col-span-2"
    >
      <img :src="pyroxeneImage" class="h-8 w-8" alt="pyroxene">
      <span>{{ kpiData.total_pyroxene_spent }}</span>
    </StatCard>

    <!-- Specific Rarity Themes -->
    <StatCard theme="r3" label="★★★ Students" :value="kpiData.r3_count" />
    <StatCard theme="r2" label="★★ Students" :value="kpiData.r2_count" />
    <StatCard theme="r1" label="★ Students" :value="kpiData.r1_count" />

  </div>
</template>
