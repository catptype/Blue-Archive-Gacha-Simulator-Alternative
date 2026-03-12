<script setup lang="ts">
  import { computed } from 'vue';
  const props = withDefaults(defineProps<{
    color: 'cyan' | 'gray';
    label: string;
    width?: string;  // Optional prop
    height?: string; // Optional prop
    textsize?: string;
  }>(), {
    width: 'w-55',   // Default value
    height: 'h-16',   // Default value
    textsize: 'text-2xl'
  });

  const emit = defineEmits(['click']);

  const colorMap = {
    cyan: 'bg-linear-to-br from-blue-500 to-cyan-500',
    gray: 'bg-linear-to-br from-gray-900 to-slate-500'
  };

  const colorClass = computed(() => colorMap[props.color] || '');

</script>

<template>
  <button 
    @click="emit('click')"
    class="btn-poly hover:brightness-110 transition-all active:scale-95 flex flex-col items-center justify-center relative overflow-hidden group"
    :class="[colorClass, props.width, props.height, props.textsize]">
    
    <div class="absolute inset-0 bg-white/20 translate-y-full group-hover:translate-y-0 transition-transform duration-300 skew-y-12"></div>
    <div class="flex items-center gap-1.5 mt-0.5 relative z-10">
      <!-- <span class="text-2xl text-white">{{ label }}</span> -->
      {{ label }}
    </div>
  </button>
</template>

<style lang="css" scoped>
  .btn-poly { clip-path: polygon(10% 0, 100% 0, 100% 70%, 90% 100%, 0 100%, 0 30%); }
</style>