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
    class="rarity-tab w-10 h-24 flex items-center justify-center rounded-l-lg transition-colors duration-200 border-l border-y border-slate-400 cursor-pointer hover:bg-slate-500"
    :class="isActive
      ? 'bg-cyan-400/40 text-white'
      : 'border-slate-400 text-slate-400'"
  >
    <span class="transform -rotate-90 whitespace-nowrap font-semibold">
      {{ label }}
    </span>
  </button>
</template>