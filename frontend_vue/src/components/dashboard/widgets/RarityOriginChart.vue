<script setup lang="ts">
    import { ref, computed } from 'vue';
    import apiClient from '@/services/client';

    // 1. Fetch the same data as before
    const { data: apiData } = await apiClient.get('/dashboard/summary/chart-banner-breakdown');

    // 2. Transform the data into the structure ApexCharts needs for a stacked bar chart
    const chartSeries = computed(() => {
        const banners = Object.keys(apiData.data);
        return banners.map(bannerName => ({
            name: bannerName,
            data: [
                apiData.data[bannerName].r3_count,
                apiData.data[bannerName].r2_count,
                apiData.data[bannerName].r1_count,
            ]
        }));
    });

    const chartCategories = computed(() => ['★★★', '★★', '★']);
    const hasData = computed(() => chartSeries.value.length > 0);

    // 3. Configure the chart options for a horizontal stacked bar chart
    const chartOptions = ref({
        chart: {
            type: 'bar',
            stacked: true, // This is the key to make it a stacked chart
            stackType: '100%', // Optional: Shows percentage composition. Use 'normal' for raw counts.
            background: 'transparent',
            toolbar: { show: false },
        },
        dataLabels: {
            enabled: true,
            formatter: function(_val: number, opts: { seriesIndex: number, dataPointIndex: number }) {
                // 1. Guard against a potential out-of-bounds index
                const seriesItem = chartSeries.value[opts.seriesIndex];
                if (!seriesItem) {
                    return ''; // Or handle as an error
                }
                
                // 2. Now that we know seriesItem exists, we can safely access its data
                const rawValue = seriesItem.data[opts.dataPointIndex];
                
                return rawValue > 0 ? rawValue : '';
            },

            // Add styling for better contrast.
            style: { 
                fontSize: '16px',
                colors: ['#fff'], 
                fontWeight: 'bold'
            },
            dropShadow: {
                enabled: true,
                top: 1,
                left: 1,
                blur: 1,
                color: '#000',
                opacity: 0.8,
            }
        },

        plotOptions: {
            bar: {  horizontal: true, barHeight: '80%' },
        },
        xaxis: {
            categories: chartCategories.value,
            labels: { 
                style: { colors: '#94a3b8' }, 
                formatter: function (val: string) { return val + "%"; } 
            }
        },
        yaxis: {
            labels: { style: { fontSize: '16px', colors: '#94a3b8' } }
        },
        tooltip: {
            y: { formatter: (val: number) => `${val} pulls`}
        },
        fill: { opacity: 1 },
        legend: {
            position: 'top',
            horizontalAlign: 'center',
            fontSize: '18px',
            labels: {  colors: '#cbd5e1' },
            markers: { size: 10 },
        },
        grid: {
            borderColor: '#475569',
            strokeDashArray: 4
        },
        theme: { mode: 'dark' },
    });
</script>

<template>
  <div class="p-4 bg-slate-700/50 rounded-lg h-full flex flex-col">
    <h3 class="text-xl font-semibold mb-4">Rarity Origins by Banner</h3>
    <div class="flex-grow min-h-0">
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