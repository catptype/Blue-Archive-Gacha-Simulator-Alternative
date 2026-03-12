<script setup lang="ts">
  defineProps<{
    activeFilter: 'all' | 'obtained' | 'not-obtained';
    obtainedCount: number;
    totalCount: number;
    percentage: number;
  }>();

  const emit = defineEmits(['update:filter']);

  const getFilterButtonClass = (current: string, target: string) => {
    const base = 'px-3 py-1 rounded-md text-sm font-semibold transition-colors flex items-center border border-slate-600 gap-2';
    return current === target 
      ? `${base} bg-cyan-600 text-white` 
      : `${base} text-slate-400 hover:bg-slate-600`;
  };
</script>

<template>
  <div class="p-4 bg-slate-700/50 rounded-lg flex flex-col lg:flex-row items-center sm:justify-between gap-4">
    <h2 class="text-xl font-semibold text-slate-300 text-center sm:text-left">
      Obtained ({{ obtainedCount }} / {{ totalCount }}) - {{ percentage.toFixed(2) }}% Complete
    </h2>
    <div class="shrink-0 flex flex-wrap justify-center items-center gap-2 p-1 bg-slate-800/50 rounded-lg">
      <button @click="emit('update:filter', 'all')" :class="getFilterButtonClass(activeFilter, 'all')">
        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" /></svg>
        <span>All</span>
      </button>
      <button @click="emit('update:filter', 'obtained')" :class="getFilterButtonClass(activeFilter, 'obtained')">
        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2z M14 11V7a4 4 0 118 0" /></svg>
        <span>Obtained</span>
      </button>
      <button @click="emit('update:filter', 'not-obtained')" :class="getFilterButtonClass(activeFilter, 'not-obtained')">
        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" /></svg>
        <span>Not Obtained</span>
      </button>
    </div>
  </div>
</template>