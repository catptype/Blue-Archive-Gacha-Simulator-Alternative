<script setup lang="ts">
import apiClient from '@/services/client';

interface ProgressionEntry {
  rarity: number;
  obtained: number;
  total: number;
}

// Use async setup to fetch data
const { data: progressionData } = await apiClient.get('/dashboard/summary/collection-progression');

// Helper to get the correct color based on rarity
const getRarityColor = (rarity: number) => {
  if (rarity === 3) return '#f472b6'; // Pink
  if (rarity === 2) return '#eab308'; // Yellow
  return '#60a5fa'; // Blue
};

// Helper to get the correct label text
const getRarityLabel = (rarity: number) => {
  if (rarity === 3) return '★★★';
  if (rarity === 2) return '★★';
  return '★';
};

const getRarityTitle = (rarity: number) => {
  if (rarity === 3) return '★★★ Collection';
  if (rarity === 2) return '★★ Collection';
  return '★ Collection';
};

// Function to generate the series array for a given item
const getChartSeries = (item: ProgressionEntry) => {
  if (item.total === 0) return [0];
  // Series is the percentage value
  return [(item.obtained / item.total) * 100];
};

// Function to dynamically generate chart options for each radial bar
const getChartOptions = (item: ProgressionEntry) => {
  return {
    chart: { type: 'radialBar', background: 'transparent' },

    states: {
    // Configuration for the "active" state (when a data point is clicked)
      // This tells the chart to not apply any filter when a series is clicked.
      active: { filter: { type: 'none' } },
    
      // Optional: You can also disable the hover effect if you want
      hover: { filter: { type: 'none' } }
    },

    plotOptions: {
      radialBar: {
        hollow: { size: '60%' }, // Controls the thickness
        dataLabels: {
          name: {
            show: false,
            fontSize: '22px',
            fontWeight: 'bold',
            color: '#cbd5e1', // slate-300
          },
          value: {
            show: true,
            fontSize: '18px',
            color: '#94a3b8', // slate-400
            offsetY: 8,
            formatter: (val: number) => `${item.obtained} / ${item.total}`,
          },
        },
      },
    },
    labels: [getRarityLabel(item.rarity)],
    colors: [getRarityColor(item.rarity)],
    theme: { mode: 'dark' },
    stroke: { lineCap: 'round' },
  };
};
</script>

<template>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <div
        v-for="item in progressionData"
        :key="item.rarity"
        class="p-4 bg-slate-700/50 rounded-lg flex flex-col items-center justify-center"
      >
        <h3 class="text-xl font-semibold mb-4">{{ getRarityTitle(item.rarity) }}</h3>
        <apexchart
          type="radialBar"
          height="250"
          width="100%"
          :options="getChartOptions(item)"
          :series="getChartSeries(item)"
        />
      </div>
    </div>
</template>