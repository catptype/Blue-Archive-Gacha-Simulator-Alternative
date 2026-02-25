<script setup lang="ts">
  import { ref } from 'vue';
  import apiClient from '@/services/client';
  import RarityRadialChart from '../base/RarityRadialChart.vue'; // Adjust path
  import { type SummaryCollectionResponse } from '@/types/web';
  

  // Fetch the data
  const response = await apiClient('/dashboard/summary/collection');
  const collection = ref<SummaryCollectionResponse>(response.data)
  
  const rarityOrder = ['3', '2', '1'] as const;
</script>

<template>
  <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
    <!-- Loop through the defined order to ensure 3rd stars are first -->
    <template v-for="rarity in rarityOrder" :key="rarity">
      <RarityRadialChart
        v-if="collection.data[rarity]"
        :rarity="rarity"
        :obtained="collection.data[rarity].obtained"
        :total="collection.data[rarity].total"
      />
    </template>
  </div>
</template>