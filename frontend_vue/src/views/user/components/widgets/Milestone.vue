<script setup lang="ts">
import { ref, computed } from 'vue';
import apiClient from '@/services/client';
import { type MileStone } from '@/types/web';
import TimelineNode from '../base/TimelineNode.vue';

// 1. Data Fetching
const response = await apiClient.get('/dashboard/summary/milestone-timeline');
const milestones = ref<MileStone[]>(response.data);

// 2. Dynamic Container Sizing
const timelineStyle = computed(() => {
  const WIDTH_PER_NODE = 120; // Adjusted for breathing room
  const MIN_WIDTH = 100;
  const calculatedWidth = (milestones.value?.length || 0) * WIDTH_PER_NODE;
  return { width: `${Math.max(MIN_WIDTH, calculatedWidth)}px` };
});
</script>

<template>
  <div class="p-4 bg-slate-700/50 rounded-lg h-full flex flex-col">
    <h3 class="text-xl text-center font-semibold mb-4 shrink-0 text-slate-100">
      ★★★ Recruitment Journey
    </h3>

    <!-- Data State -->
    <div v-if="milestones.length > 0" class="grow w-full overflow-x-auto overflow-y-hidden custom-scrollbar">
      <div class="relative h-full flex items-center mx-auto" :style="timelineStyle">
        
        <!-- The Central Track -->
        <div class="absolute top-1/2 translate-y-1/2 w-full h-1 bg-slate-600/50"></div>

        <!-- The Milestones -->
        <div class="relative w-full h-full flex justify-between py-20 px-10">
          <TimelineNode 
            v-for="(item, index) in milestones" 
            :key="item.student.id"
            :milestone="item"
            :index="index"
          />
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="grow w-full flex items-center justify-center text-slate-400 bg-slate-800/30 rounded-lg border border-dashed border-slate-600">
      <p>Pull a 3-star student to start your timeline!</p>
    </div>
  </div>
</template>
