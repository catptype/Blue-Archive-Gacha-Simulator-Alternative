<script setup lang="ts">
    import { ref, computed } from 'vue';
    import apiClient from '../../../services/client';

    // Use async setup to fetch the data
    const { data: apiData } = await apiClient.get('/dashboard/summary/chart-banner-breakdown');

    // --- State Management ---
    const bannerNames = computed(() => Object.keys(apiData.data).sort());
    const selectedBanner = ref(bannerNames.value[0] || null);
    const hasData = computed(() => bannerNames.value.length > 0);

    // --- Reactive Chart Data ---
    const chartSeries = computed(() => {
        if (!selectedBanner.value || !apiData.data[selectedBanner.value]) {
            return [0, 0, 0];
        }
        const currentData = apiData.data[selectedBanner.value];
        return [currentData.r3_count, currentData.r2_count, currentData.r1_count];
    });

    // --- Chart Configuration ---
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
  <div class="relative p-4 bg-slate-700/50 rounded-lg h-full flex flex-col">
    <!-- =============================================================== -->
    <!-- NEW: WIDGET HEADER                                              -->
    <!-- This flex container neatly aligns the title and the dropdown. -->
    <!-- =============================================================== -->
    <div class="flex justify-between items-center mb-4">
      <h3 class="text-xl font-semibold">Breakdown</h3>
      
      <div v-if="hasData" class="flex items-center gap-2">
        <label for="banner-select" class="text-xs text-slate-400">Banner:</label>
        <select
          v-model="selectedBanner"
          id="banner-select"
          class="bg-slate-800 border border-slate-600 rounded-md text-white p-1 text-sm focus:ring-2 focus:ring-cyan-500 focus:outline-none"
        >
          <option v-for="bannerName in bannerNames" :key="bannerName" :value="bannerName">
            {{ bannerName }}
          </option>
        </select>
      </div>
    </div>
    
    <!-- =============================================================== -->
    <!-- CHART AREA (Now simplified)                                     -->
    <!-- The chart no longer needs a relative parent for the selector. -->
    <!-- =============================================================== -->
    <div class="relative flex-grow min-h-0">
      <apexchart
        v-if="hasData"
        type="donut"
        height="100%"
        :options="chartOptions"
        :series="chartSeries"
      />
      <div v-else class="w-full h-full flex items-center justify-center text-slate-400">
        No pulls yet to display data.
      </div>

      <!-- The absolute positioned div for the old selector is now completely gone. -->
    </div>
  </div>
</template>