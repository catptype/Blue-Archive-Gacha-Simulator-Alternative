<script setup lang="ts">
    const emit = defineEmits<{
        (e: 'showDetails'): void;
        (e: 'pull', amount: 1 | 10): void;
    }>();
</script>

<template>
  <div class="row-span-3 w-full h-full bg-black/30 backdrop-blur-sm border border-slate-700 rounded-lg p-6 flex items-center justify-between">
    <button @click="emit('showDetails')" class="px-6 py-3 text-lg font-semibold border-2 border-slate-500 hover:border-cyan-400 hover:text-cyan-400 rounded-lg transition-colors">
      Banner Details
    </button>
    <div class="flex items-center gap-4">
      <div class="flex flex-col items-center gap-1">
        <button @click="emit('pull', 1)" class="w-40 px-4 py-3 flex justify-center bg-slate-600 hover:bg-slate-500 rounded-lg text-xl font-bold transition-colors gap-2">
          PULL x1
        </button>
        <span class="text-sm text-slate-400">120 Pyroxene</span>
      </div>
      <div class="flex flex-col items-center gap-1">
        <button @click="emit('pull', 10)" class="w-40 px-4 py-3 flex justify-center bg-cyan-600 hover:bg-cyan-500 rounded-lg text-xl font-bold transition-colors gap-2">
          PULL x10
        </button>
        <span class="text-sm text-slate-400">1200 Pyroxene</span>
      </div>
    </div>
  </div>
</template>