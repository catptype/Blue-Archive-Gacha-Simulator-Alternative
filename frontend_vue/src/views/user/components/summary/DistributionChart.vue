<script setup lang="ts">
    import { ref, computed } from 'vue';
    import apiClient from '@/services/client';
    import { type BannerDistribution } from '@/types/web';

    // 1. Fetch the same data as before
    const response = await apiClient.get('/dashboard/summary/chart-banner-breakdown');
    const apiData = ref<BannerDistribution>(response.data);
      
    const totals = computed(() => {
        // Access data via apiData.value
        const bannerValues = Object.values(apiData.value.data);
        return {
            r3: bannerValues.reduce((sum, b) => sum + b.r3_count, 0),
            r2: bannerValues.reduce((sum, b) => sum + b.r2_count, 0),
            r1: bannerValues.reduce((sum, b) => sum + b.r1_count, 0),
        };
    });
    
    const chartSeries = computed(() => {
        // Use Object.entries on apiData.value.data
        return Object.entries(apiData.value.data).map(([bannerName, counts]) => ({
            name: bannerName,
            data: [
                counts.r3_count,
                counts.r2_count,
                counts.r1_count,
            ]
        }));
    });

    const chartCategories = computed(() => [
        `★★★ (${totals.value.r3})`, 
        `★★ (${totals.value.r2})`, 
        `★ (${totals.value.r1})`
    ]);
    
    const hasData = computed(() => chartSeries.value.length > 0);

    
    // 3. Configure the chart options for a horizontal stacked bar chart
    const AXIS_COLOR = '#ffffff';
    const TEXT_COLOR = '#cbd5e1';
    const BORDER_COLOR = '#475569';
    const FONT_SIZE = '14px';
    
    const chartOptions = ref({
      chart: {
        type: 'bar',
        stacked: true, 
        stackType: '100%',
        background: 'transparent',
        toolbar: { show: true },
      },
      dataLabels: { enabled: false },
      plotOptions: { bar: {  horizontal: true, barHeight: '80%' } },
      xaxis: {
        categories: chartCategories.value,
        labels: { 
          style: { colors: AXIS_COLOR }, 
          formatter: (val: string) => `${val}%` 
        }
      },
      yaxis: { labels: { style: { fontSize: FONT_SIZE, colors: AXIS_COLOR } } },
      tooltip: { y: { formatter: (val: number) => `${val} pulls` } },
      legend: {
        position: 'top',
        horizontalAlign: 'center',
        fontSize: FONT_SIZE,
        labels: {  colors: TEXT_COLOR },
        markers: { size: 12 },
        onItemClick: { toggleDataSeries: false },
      },
      grid: { borderColor: BORDER_COLOR, strokeDashArray: 4 },
      theme: { mode: 'dark' },
    });
</script>

<template>
  <div class="p-4 bg-slate-700/50 rounded-lg h-full flex flex-col">
    <h3 class="text-xl text-center font-semibold mb-4">Student Distribution by Banner Source</h3>
    <div class="grow min-h-0">
      <apexchart
        v-if="hasData"
        type="bar"
        height="250"
        :options="chartOptions"
        :series="chartSeries"
      />
      <div v-else class="w-full h-full flex items-center justify-center text-slate-400">
        No pulls yet to display data.
      </div>
    </div>
  </div>
</template>

<style scoped>
  /* Remove the 'pointer' cursor from legend items */
  :deep(.apexcharts-legend-marker) {
    cursor: default !important;
  }

  /* Remove export chart in PNG and SVG from ApexChart*/
  :deep(.apexcharts-menu-item.exportSVG),
  :deep(.apexcharts-menu-item.exportPNG) {
    display: none !important;
  }
</style>