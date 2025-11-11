<script setup lang="ts">
    import ResultCard from '@/components/gacha/ResultCard.vue';
    defineProps<{ student: any }>();
</script>

<template>
  <div class="relative">
    <!-- Use the existing ResultCard, but always flipped -->
    <ResultCard class="mx-auto" :student="student" :is-flipped="true" :enable-effects="false" />
    
    <!-- Lock Overlay for un-obtained students -->
    <div
      v-if="!student.is_obtained"
      class="w-[220px] mx-auto absolute inset-0 flex items-center justify-center bg-black/80 rounded-lg pointer-events-none"
    >
      <svg class="h-20 w-20 text-white" viewBox="0 0 20 20" fill="currentColor">
        <path fill-rule="evenodd" d="M10 1a4.5 4.5 0 00-4.5 4.5V9H5a2 2 0 00-2 2v6a2 2 0 002 2h10a2 2 0 002-2v-6a2 2 0 00-2-2h-.5V5.5A4.5 4.5 0 0010 1zm3 8V5.5a3 3 0 10-6 0V9h6z" clip-rule="evenodd" />
      </svg>
    </div>
  </div>
</template>