<script setup lang="ts">
  defineProps<{
    label: string;
    isActive: boolean;
  }>();

  const emit = defineEmits<{
    (e: 'select'): void;
  }>();
</script>

<template>
  <button
    @click="emit('select')"
    class="rarity-tab w-10 h-24 flex items-center justify-center rounded-l-lg transition-colors duration-200 border-l border-t border-b"
    :class="isActive
      ? 'bg-slate-700/50 border-slate-600 text-white font-semibold'
      : 'border-transparent text-slate-400 hover:bg-slate-800/50'"
  >
    <span class="transform -rotate-90 whitespace-nowrap font-semibold">
      {{ label }}
    </span>
  </button>
</template>