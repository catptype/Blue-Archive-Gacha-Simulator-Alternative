<script setup lang="ts">
  import { ref } from 'vue';
  import apiClient from '@/services/client';
  import PodiumDisplay from '../base/PodiumDisplay.vue'; // Import the new component
  import TabVerticalButton from '../base/TabVerticalButton.vue';
  import { type Top3Student } from '@/types/web';

  const topStudents = ref<Top3Student[]>([]);
  const activeRarity = ref<number>(3);
  const isLoading = ref(false);

  // Define the tab configuration
  const tabs = [
    { value: 3, label: '★★★' },
    { value: 2, label: '★★' },
    { value: 1, label: '★' },
  ];

  const loadPodiumContent = async (rarity: number) => {
    if (isLoading.value) return;

    isLoading.value = true;
    activeRarity.value = rarity;
    try {
      const { data } = await apiClient.get(`/dashboard/summary/top-students/${rarity}`);
      topStudents.value = data;
    } catch (error) {
      console.error("Failed to load podium data:", error);
      topStudents.value = [];
    } finally {
      isLoading.value = false;
    }
  };

  // Initial data load for the default (3-star) tab, which works with <Suspense>
  await loadPodiumContent(3);
</script>

<template>
  <div class="relative flex h-full">
    <!-- Column 1: Vertical Rarity Tabs -->
    <div class="flex flex-col gap-1 z-20 my-auto">
      <TabVerticalButton 
        v-for="tab in tabs" 
        :key="tab.value"
        :label="tab.label"
        :is-active="activeRarity === tab.value"
        @select="loadPodiumContent(tab.value)"
      />
    </div>

    <!-- Column 2: Podium Content Panel -->
    <div class="relative w-full h-full z-10 grow p-4 bg-slate-700/50 rounded-lg overflow-hidden">
      <h3 class="text-center text-xl font-semibold">Most Pulled Students</h3>
      <div
        class="w-full h-full transition-opacity duration-300 mx-auto"
        :class="{ 'opacity-50': isLoading }"
      >
        <PodiumDisplay :top-students="topStudents" :rarity="activeRarity"/>
      </div>
    </div>
  </div>
</template>