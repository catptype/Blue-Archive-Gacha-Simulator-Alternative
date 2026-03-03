<script setup lang="ts">
import { computed } from 'vue';
import { type Achievement } from '@/types/web';

const props = defineProps<{ achievement: Achievement }>();

const formattedDate = computed(() => {
  if (!props.achievement.unlocked_on) return '';
  return new Date(props.achievement.unlocked_on).toLocaleDateString(undefined, {
    year: 'numeric', month: 'short', day: 'numeric',
  });
});

// A computed property to handle all state-based styling
const unlockedClass = computed(() => {
  if (props.achievement.is_unlocked) {
    return 'border-cyan-400';
  } else {
    return 'opacity-50 grayscale border-transparent';
  }
});
</script>

<template>
  <div
    class="flex items-start gap-4 p-4 bg-slate-700/50 rounded-lg border-l-4 transition-all duration-300"
    :class="unlockedClass"
  >
    <!-- Icon Column -->
    <div class="relative shrink-0 w-20 h-20 bg-slate-800 rounded-md">
      <img v-if="achievement.image_url" :src="achievement.image_url" :alt="achievement.name" class="w-full h-full object-contain rounded-md">
      
      <div v-if="!achievement.is_unlocked" class="absolute inset-0 flex items-center justify-center bg-black/90 rounded-md">
        <svg class="h-8 w-8 text-white" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M10 1a4.5 4.5 0 00-4.5 4.5V9H5a2 2 0 00-2 2v6a2 2 0 002 2h10a2 2 0 002-2v-6a2 2 0 00-2-2h-.5V5.5A4.5 4.5 0 0010 1zm3 8V5.5a3 3 0 10-6 0V9h6z" clip-rule="evenodd" />
        </svg>
      </div>
    </div>

    <!-- Details Column -->
    <div class="grow">
      <h3 class="font-bold text-white text-lg">{{ achievement.name }}</h3>
      <p class="text-sm text-slate-300 mt-1">{{ achievement.description }}</p>
      
      <p v-if="achievement.is_unlocked && achievement.unlocked_on" class="text-xs text-cyan-400 mt-2">
        Unlocked on: {{ formattedDate }}
      </p>
    </div>
  </div>
</template>