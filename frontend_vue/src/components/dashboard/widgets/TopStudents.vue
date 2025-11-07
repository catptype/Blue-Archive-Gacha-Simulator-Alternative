<template>
  <div class="relative flex h-full">
    <!-- Column 1: Vertical Rarity Tabs -->
    <div class="flex flex-col gap-1 z-20 pt-2">
      <button
        @click="loadPodiumContent(3)"
        class="rarity-tab w-10 h-24 flex items-center justify-center rounded-l-lg transition-colors duration-200 border-l border-t border-b"
        :class="activeRarity === 3
          ? 'bg-slate-700/50 border-slate-600 text-white font-semibold'
          : 'border-transparent text-slate-400 hover:bg-slate-800/50'"
      >
        <span class="transform -rotate-90 whitespace-nowrap font-semibold">★★★</span>
      </button>
      <button
        @click="loadPodiumContent(2)"
        class="rarity-tab w-10 h-24 flex items-center justify-center rounded-l-lg transition-colors duration-200 border-l border-t border-b"
        :class="activeRarity === 2
          ? 'bg-slate-700/50 border-slate-600 text-white font-semibold'
          : 'border-transparent text-slate-400 hover:bg-slate-800/50'"
      >
        <span class="transform -rotate-90 whitespace-nowrap font-semibold">★★</span>
      </button>
      <button
        @click="loadPodiumContent(1)"
        class="rarity-tab w-10 h-24 flex items-center justify-center rounded-l-lg transition-colors duration-200 border-l border-t border-b"
        :class="activeRarity === 1
          ? 'bg-slate-700/50 border-slate-600 text-white font-semibold'
          : 'border-transparent text-slate-400 hover:bg-slate-800/50'"
      >
        <span class="transform -rotate-90 whitespace-nowrap font-semibold">★</span>
      </button>
    </div>

    <!-- Column 2: Podium Content Panel -->
    <div class="relative w-full h-full z-10 flex-grow p-4 bg-slate-700/50 rounded-r-lg rounded-b-lg overflow-hidden">
      <h3 class="text-xl font-semibold mb-2">Most Pulled Students</h3>
      <div
        class="w-full h-full transition-opacity duration-300"
        :class="{ 'opacity-50': isLoading }"
      >
        <PodiumDisplay :top-students="topStudents" :rarity="activeRarity"/>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
  import { ref } from 'vue';
  import apiClient from '../../../services/client';
  import PodiumDisplay from './PodiumDisplay.vue'; // Import the new component

  interface TopStudent {
    student: {
      student_id: number;
      student_name: string;
      portrait_url: string;
    };
    count: number;
  }

  const topStudents = ref<TopStudent[]>([]);
  const activeRarity = ref<number>(3);
  const isLoading = ref(false);

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