<script setup lang="ts">
    import { computed } from 'vue';
    import apiClient from '@/services/client';

    const { data: milestones } = await apiClient.get('/dashboard/summary/milestone-timeline');
    // Calculate the dynamic width for the timeline container
    const timelineStyle = computed(() => {
        const WIDTH_PER_MILESTONE = 100; // Increased width for better spacing in Vue
        const MIN_WIDTH = 100;
        const calculatedWidth = milestones.length * WIDTH_PER_MILESTONE;
        return { width: `${Math.max(MIN_WIDTH, calculatedWidth)}px` };
    });

    // Helper function for clean conditional classes
    const isEven = (index: number) => index % 2 === 0;
</script>

<template>
  <div class="p-4 bg-slate-700/50 rounded-lg h-full flex flex-col">
    <h3 class="text-xl font-semibold mb-4 flex-shrink-0">★★★ First Pull Timeline</h3>
    
    <!-- Has Data State -->
    <div v-if="milestones.length > 0" class="flex-grow w-full overflow-x-auto overflow-y-hidden">
      <div class="relative h-full flex items-center mx-auto" :style="timelineStyle">
        
        <!-- The Timeline Track -->
        <div class="absolute top-1/2 translate-y-1/2 w-full h-1 bg-slate-600"></div>

        <!-- This flex container evenly spaces all the milestones -->
        <div class="relative w-full h-full flex justify-between py-20">
          
          <div
            v-for="(milestone, index) in milestones"
            :key="milestone.student.student_id"
            class="relative flex flex-col items-center"
            :class="isEven(index)
              ? 'justify-start -translate-y-[70px]'
              : 'justify-end translate-y-[78px]'"
          >
            <!-- The circular marker on the timeline track -->
            <div
              class="absolute left-1/2 -translate-x-1/2 w-4 h-4 bg-slate-800 border-2 border-cyan-400 rounded-full"
              :class="isEven(index) ? 'bottom-0' : 'top-0'"
            ></div>
            
            <!-- The "Stem" -->
            <div
              class="h-8 w-0.5 bg-slate-600"
              :class="isEven(index) ? 'order-2' : 'order-1'"
            ></div>
            
            <!-- The Student Portrait and Info -->
            <div
              class="flex flex-col items-center text-center"
              :class="isEven(index) ? 'order-1 mb-3' : 'order-2 mt-3'"
            >
              <img :src="milestone.student.portrait_url" class="w-20 h-20 rounded-md object-cover border-2 border-slate-500">
              <p class="text-sm font-bold mt-1">{{ milestone.student.student_name }}</p>
              <p class="text-xs text-slate-400">Pull #{{ milestone.pull_number }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- No Data State -->
    <div v-else class="flex-grow w-full flex items-center justify-center text-slate-400">
      <p>Pull a 3-star student to start your timeline!</p>
    </div>
  </div>
</template>
