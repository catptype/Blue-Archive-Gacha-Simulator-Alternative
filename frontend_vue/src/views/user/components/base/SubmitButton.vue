<script setup lang="ts">
  const props = defineProps<{ label: string }>();
</script>

<template>
  <button 
    v-bind="$attrs"
    class="w-full py-2 px-4 bg-cyan-600 hover:bg-cyan-500 rounded text-white font-bold transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
  >
  {{ label }}
  </button>
</template>
