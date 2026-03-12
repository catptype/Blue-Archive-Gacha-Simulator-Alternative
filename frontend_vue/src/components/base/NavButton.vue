<script setup lang="ts">
import { computed } from 'vue';

// Define props: direction can only be 'left' or 'right'
const props = defineProps<{
  direction: 'left' | 'right';
}>();

const emit = defineEmits(['click']);

// Dynamic classes based on direction
const positionClass = computed(() => 
  props.direction === 'left' ? 'left-6' : 'right-6'
);

// SVG Paths for arrows
const arrowPath = computed(() => 
  props.direction === 'left' 
    ? 'M15 19l-7-7 7-7' // Left arrow
    : 'M9 5l7 7-7 7'    // Right arrow
);
</script>

<template>
  <button 
    @click="emit('click')"
    type="button"
    class="absolute top-1/2 -translate-y-1/2 z-40 p-3 rounded-full bg-black/40 hover:bg-sky-500/50 text-white transition-colors border border-white/10"
    :class="positionClass"
  >
    <svg class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path 
        stroke-linecap="round" 
        stroke-linejoin="round" 
        stroke-width="2" 
        :d="arrowPath" 
      />
    </svg>
  </button>
</template>