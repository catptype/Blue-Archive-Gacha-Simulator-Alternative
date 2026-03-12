<script setup lang="ts">
  // Props passed from the parent
  const props = defineProps<{
    rarity: string | number;
    obtained: number;
    total: number;
  }>();

  const rarityNum = Number(props.rarity);

  // Visual Configurations
  const config = {
    3: { color: '#f472b6', label: '★★★', title: '★★★ Collection' },
    2: { color: '#eab308', label: '★★',  title: '★★ Collection' },
    1: { color: '#60a5fa', label: '★',   title: '★ Collection' },
  }[rarityNum] || { color: '#94a3b8', label: '?', title: 'Unknown' };

  const chartSeries = [props.total > 0 ? (props.obtained / props.total) * 100 : 0];

  const chartOptions = {
    chart: { type: 'radialBar', background: 'transparent' },
    states: {
      active: { filter: { type: 'none' } },
      hover: { filter: { type: 'none' } }
    },
    colors: [config.color],
    theme: { mode: 'dark' },
    stroke: { lineCap: 'round' },
    labels: [config.label],
    plotOptions: {
      radialBar: {
        hollow: { size: '60%' },
        dataLabels: {
          name: { show: false },
          value: {
            show: true,
            fontSize: '18px',
            color: '#94a3b8',
            offsetY: 8,
            formatter: () => `${props.obtained} / ${props.total}`,
          },
        },
      },
    },
  };
</script>

<template>
  <div class="p-4 bg-slate-700/50 rounded-lg flex flex-col items-center justify-center">
    <h3 class="text-xl font-semibold mb-4">{{ config.title }}</h3>
    <apexchart
      type="radialBar"
      height="250"
      width="100%"
      :options="chartOptions"
      :series="chartSeries"
    />
  </div>
</template>