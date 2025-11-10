<script setup lang="ts">
import { ref, computed } from 'vue';
import apiClient from '../../../services/client';

// Use async setup to fetch the data. The parent <Suspense> handles the loading state.
const { data } = await apiClient.get('/dashboard/summary/chart-overall-rarity');

// --- Transform the API data into the format ApexCharts expects ---

// The `series` for a doughnut chart is a simple array of numbers.
const chartSeries = computed(() => [
  data.r3_count,
  data.r2_count,
  data.r1_count
]);

// A helper computed property to check if there is any data to display.
const hasData = computed(() => chartSeries.value.some(value => value > 0));

// The `options` object contains all the configuration for ApexCharts.
// read https://apexcharts.com/docs/options/plotoptions/pie/
const chartOptions = ref({
        labels: ['★★★', '★★', '★'],
        colors: ['#f472b6', '#eab308', '#3b82f6'],
        chart: { type: 'donut', background: 'transparent' },
        plotOptions: {
          pie: { donut: { size: '33%' } }
        },
        
        legend: {
            position: 'top',
            labels: { colors: '#cbd5e1' }, // slate-300
            markers: { width: 12, height: 12 },
            itemMargin: { horizontal: 5 }
        },


        dataLabels: {
          enabled: true,
          formatter: function (val, opts) {
            const seriesValue = chartSeries.value[opts.seriesIndex];
            return seriesValue;
          },
          style: {
            fontSize: '1rem',
            fontWeight: 'bold',
            colors: ['#fff']
          },
          dropShadow: {
              enabled: true,
              top: 1,
              left: 1,
              blur: 1,
              color: '#000',
              opacity: 0.7
          }
        },

        stroke: { show: false },
    });
</script>

<template>
  <div class="p-4 bg-slate-700/50 rounded-lg h-full flex flex-col">
    <h3 class="text-xl font-semibold mb-4">Overall Rarity</h3>
    <div class="flex-grow min-h-0"> <!-- Added min-h-0 to help flexbox resizing -->
      <apexchart
        v-if="hasData"
        type="donut"
        height="100%"
        :options="chartOptions"
        :series="chartSeries"
      />
      <!-- Fallback message for when there are no pulls yet -->
      <div v-else class="w-full h-full flex items-center justify-center text-slate-400">
        No pulls yet to display data.
      </div>
    </div>
  </div>
</template>