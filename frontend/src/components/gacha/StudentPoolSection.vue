<script setup lang="ts">
    import { computed } from 'vue';

    const props = defineProps<{
        title: string;
        totalRate: number;
        students: any[];
        viewMode: 'grid' | 'list';
        individualRate: number;
        isPickup: boolean;
    }>();

    const gridItemBorderClass = computed(() => ({
        'border-cyan-400/50 hover:border-cyan-300': props.isPickup,
        'border-slate-700 hover:border-slate-500': !props.isPickup,
    }));
</script>

<template>
  <div class="mb-6">
    <!-- Section Header -->
    <div class="flex items-center justify-between mb-2">
      <h3 class="text-xl font-semibold">{{ title }}</h3>
      <span class="text-md font-mono text-slate-400">
        ({{ totalRate.toFixed(2) }}%)
      </span>
    </div>

    <!-- Grid View -->
    <div v-if="viewMode === 'grid'" class="flex flex-wrap gap-2 group/list">
      <div
        v-for="student in students"
        :key="student.student_id"
        class="group/item relative w-16 h-16 transition-all duration-300 group-hover/list:opacity-50 group-hover/list:grayscale hover:!opacity-100 hover:!grayscale-0"
      >
        <div class="w-full h-full bg-slate-900 rounded-lg border overflow-hidden transition-all duration-200 hover:scale-120" :class="gridItemBorderClass">
          <img :src="student.portrait_url" :alt="student.student_name">
        </div>
        <div class="absolute -bottom-2 left-1/2 -translate-x-1/2 px-2 py-0.5 bg-black/80 rounded-md text-xs text-white opacity-0 group-hover/item:opacity-100 transition-opacity pointer-events-none whitespace-nowrap">
          {{ individualRate.toFixed(4) }}%
        </div>
      </div>
    </div>

    <!-- List View -->
    <div v-else class="flex flex-col gap-1">
      <div
        v-for="student in students"
        :key="student.student_id"
        class="flex items-center justify-between p-2 rounded-lg hover:bg-slate-700/50"
      >
        <div class="flex items-center gap-3">
          <img :src="student.portrait_url" class="w-16 h-16 rounded-md object-cover">
          <div>
            <span class="font-semibold text-lg">{{ student.student_name }}</span>
            <span v-if="student.version.version_name !== 'Original'" class="ml-2 font-semibold text-sm text-slate-400">
              ({{ student.version.version_name }})
            </span>
          </div>
        </div>
        <span class="font-mono text-sm text-slate-400">{{ individualRate.toFixed(4) }}%</span>
      </div>
    </div>
  </div>
</template>