<script setup lang="ts">
import { computed } from 'vue';
import { type MileStone } from '@/types/web';

const props = defineProps<{
  milestone: MileStone;
  index: number;
}>();

const isEven = computed(() => props.index % 2 === 0);

// Consolidate the positioning logic
const positionClasses = computed(() => ({
  container: isEven.value ? 'justify-start -translate-y-[70px]' : 'justify-end translate-y-[78px]',
  marker: isEven.value ? 'bottom-0' : 'top-0',
  stem: isEven.value ? 'order-2' : 'order-1',
  content: isEven.value ? 'order-1 mb-3' : 'order-2 mt-3'
}));
</script>

<template>
  <div class="relative flex flex-col items-center" :class="positionClasses.container">
    <!-- The circular marker on the timeline track -->
    <div
      class="absolute left-1/2 -translate-x-1/2 w-4 h-4 bg-slate-800 border-2 border-cyan-400 rounded-full"
      :class="positionClasses.marker"
    ></div>

    <!-- The "Stem" -->
    <div class="h-8 w-0.5 bg-slate-600" :class="positionClasses.stem"></div>

    <!-- The Student Portrait and Info -->
    <div class="flex flex-col items-center text-center" :class="positionClasses.content">
      <div class="relative group">
        <img 
          :src="milestone.student.portrait_url" 
          :alt="milestone.student.name" 
          class="w-20 h-20 rounded-md object-cover border-2 border-slate-500 group-hover:border-cyan-400 transition-colors"
        >
      </div>
      <p class="text-sm font-bold mt-1 text-slate-200">{{ milestone.student.name }}</p>
      <p class="text-xs text-slate-400">Pull #{{ milestone.pull_number }}</p>
    </div>
  </div>
</template>