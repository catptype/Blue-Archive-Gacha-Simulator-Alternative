<script setup lang="ts">
import { computed } from 'vue';
import { type Student } from '@/types/web';

// This component receives the full student object
const props = defineProps<{ student: Student }>();

// Logic
const isR3 = props.student.rarity === 3;
const isR2 = props.student.rarity === 2;
const isR1 = props.student.rarity === 1;

// --- Re-used Computed Properties for Styling ---
const rarityBorderClass = computed(() => ({
  'bg-gradient-to-br from-pink-400 via-purple-400 to-cyan-400': isR3,
  'bg-yellow-400/80': isR2,
  'bg-blue-400/80': isR1,
}));

const rarityPillClass = computed(() => ({
  'bg-gradient-to-br from-pink-400/80 via-purple-400/80 to-cyan-400/80': isR3,
  'bg-yellow-500/80 border-2 border-yellow-300/50': isR2,
  'bg-blue-500/80 border-2 border-blue-300/50': isR1,
}));
</script>

<template>
  <!-- Added the 'group' class to enable the hover effect on the overlay -->
  <div class="relative min-w-[100px] w-full aspect-[4.5/5] rounded-lg shadow-lg p-1 transition-all duration-300 group" :class="rarityBorderClass">
    <div class="relative w-full h-full bg-slate-200 rounded-sm overflow-hidden">
      
      <!-- Portrait -->
      <div class="absolute inset-1.5 overflow-hidden" style="clip-path: polygon(12px 0, 100% 0, 100% calc(100% - 12px), calc(100% - 12px) 100%, 0 100%, 0 12px);">
        <img
          v-if="student.portrait_url"
          :src="student.portrait_url"
          :alt="student.name"
          class="w-full h-full object-cover transition-transform duration-300"
          :class="{ 'grayscale': !student.is_obtained }"
        >
        <div class="absolute inset-0 pointer-events-none" style="box-shadow: inset 0 0 10px 4px rgba(0, 0, 0, 0.5);"></div>
      </div>
    </div>
    
    <!-- Info Overlay (Visible on hover for obtained students) -->
    <div
      v-if="student.is_obtained"
      class="
        w-[80%] absolute bottom-2 left-1/2 -translate-x-1/2 
        px-2 py-1 flex items-center justify-center gap-2 backdrop-blur-sm 
        rounded-full shadow-inner-sm text-center
        
        opacity-0 translate-y-4
        group-hover:opacity-100 group-hover:-translate-y-1
        transition-all duration-300 ease-in-out
      "
      :class="rarityPillClass"
    >
      <div class="flex flex-col text-white text-shadow-strong">
        <h4 class="font-bold text-xs leading-tight">{{ student.name }}</h4>
        <p class="text-[10px] opacity-80 leading-tight">
          ({{ student.version.name }})
        </p>
      </div>
    </div>

    <div v-else
      class="absolute min-w-[100px] inset-0 flex items-center justify-center bg-black/80 rounded-lg pointer-events-none"
    >
      <svg class="h-12 w-12 text-white" viewBox="0 0 20 20" fill="currentColor">
        <path fill-rule="evenodd" d="M10 1a4.5 4.5 0 00-4.5 4.5V9H5a2 2 0 00-2 2v6a2 2 0 002 2h10a2 2 0 002-2v-6a2 2 0 00-2-2h-.5V5.5A4.5 4.5 0 0010 1zm3 8V5.5a3 3 0 10-6 0V9h6z" clip-rule="evenodd" />
      </svg>
    </div>

  </div>
</template>

<style scoped>
.text-shadow-strong {
  text-shadow: 0px 1px 3px rgba(0, 0, 0, 0.7);
}
</style>