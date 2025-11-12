<script setup lang="ts">
    import type { Toast } from '@/stores/toast';
    defineProps<{ toast: Toast }>();
    const emit = defineEmits(['close']);
</script>

<template>
  <div class="flex items-center gap-3 p-3 bg-slate-800 border border-slate-600 rounded-lg shadow-2xl w-80">
    <!-- Icon -->
    <div class="flex-shrink-0 w-16 h-16 bg-slate-700 rounded-md">
      <img v-if="toast.image_url" :src="toast.image_url" class="w-full h-full object-contain rounded-md">
    </div>
    <!-- Details -->
    <div class="flex-grow">
      <p class="text-xs text-cyan-400 font-semibold">Achievement Unlocked!</p>
      <h4 class="font-bold text-white">{{ toast.achievement_name }}</h4>
    </div>
    <!-- Close Button -->
    <button @click="emit('close')" class="flex-shrink-0 text-slate-500 hover:text-white text-2xl leading-none">&times;</button>
  </div>
</template>