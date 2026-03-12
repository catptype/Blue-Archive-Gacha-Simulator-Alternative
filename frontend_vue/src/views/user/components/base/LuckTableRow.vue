<script setup lang="ts">
  import { computed } from 'vue';
  import { type LuckPerformance } from '@/types/web';
  
  const props = defineProps<{performance: LuckPerformance}>();

  const luckInfo = computed(() => {
    const val = props.performance.luck_variance;
    if (val > 0) return { class: 'text-green-400', icon: '▲', sign: '+' };
    if (val < 0) return { class: 'text-red-400', icon: '▼', sign: '' };
    return { class: 'text-slate-400', icon: '', sign: '' };
  });
</script>

<template>
  <tr class="border-b border-slate-700/50">
    <td class="p-2 font-bold">{{ props.performance.banner_name }}</td>
    <td class="p-2 text-center">{{ props.performance.total_pulls }}</td>
    <td class="p-2 text-center text-yellow-300 font-bold">{{ props.performance.r3_count }}</td>
    <td class="p-2 text-center">{{ props.performance.user_rate.toFixed(2) }}%</td>
    <td class="p-2 text-center">{{ props.performance.banner_rate.toFixed(2) }}%</td>
    <td class="p-2 text-center font-bold" :class="luckInfo.class">
      {{ luckInfo.sign }}{{ props.performance.luck_variance.toFixed(2) }}% {{ luckInfo.icon }}
    </td>
    <td class="p-2 text-center">{{ props.performance.gaps?.min ?? '—' }}</td>
    <td class="p-2 text-center">{{ props.performance.gaps?.avg ?? '—' }}</td>
    <td class="p-2 text-center">{{ props.performance.gaps?.max ?? '—' }}</td>
  </tr>
</template>