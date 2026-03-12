<script setup lang="ts">
interface Props {
  size?: string;  // e.g., 'h-10 w-10'
  color?: string; // e.g., 'text-white'
  label?: string; // Optional text like "Loading..."
}

withDefaults(defineProps<Props>(), {
  size: 'h-10 w-10',
  color: 'text-white',
  label: ''
});
</script>

<template>
  <div class="w-full h-full flex flex-col items-center justify-center gap-3">
    <svg 
      :class="['animate-spin', size, color]" 
      fill="none" 
      viewBox="0 0 24 24"
    >
      <circle 
        class="opacity-25" 
        cx="12" cy="12" r="10" 
        stroke="currentColor" 
        stroke-width="4"
      ></circle>
      <path 
        class="opacity-75" 
        fill="currentColor" 
        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
      ></path>
    </svg>
    <p v-if="label" class="text-sm font-medium" :class="color">{{ label }}</p>
  </div>
</template>