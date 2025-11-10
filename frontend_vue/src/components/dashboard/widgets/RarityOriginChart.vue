<script setup lang="ts">
    import { ref, computed } from 'vue';
    import apiClient from '../../../services/client';

    // 1. Fetch the same data as before
    const { data: apiData } = await apiClient.get('/dashboard/summary/chart-banner-breakdown');

    // 2. Transform the data into the structure ApexCharts needs for a stacked bar chart
    const { chartSeries, chartCategories } = computed(() => {
        const banners = Object.keys(apiData.data);
        if (banners.length === 0) {
            return { chartSeries: [], chartCategories: [] };
        }

        // The 'series' for a stacked bar is an array of objects.
        // Each object represents a banner and its data points correspond to the categories.
        const series = banners.map(bannerName => ({
            name: bannerName,
            data: [
                apiData.data[bannerName].r3_count,
                apiData.data[bannerName].r2_count,
                apiData.data[bannerName].r1_count,
            ]
        }));
    
        // The 'categories' are the labels for the X-axis.
        const categories = ['★★★', '★★', '★'];

        return { chartSeries: series, chartCategories: categories };
    }).value;

    const hasData = computed(() => chartSeries.length > 0);

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
            // The formatter function is the key to showing raw numbers.
            formatter: function(val, opts) {
                // `val` is the calculated percentage. We ignore it.
                // We access the original raw number from the series data.
                // `opts.seriesIndex` is the index of the banner (e.g., 0 for "Bunny Banner").
                // `opts.dataPointIndex` is the index of the rarity (e.g., 0 for R3).
                const rawValue = chartSeries[opts.seriesIndex].data[opts.dataPointIndex];
                
                // Don't show a label for zero values to keep the chart clean.
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
            categories: chartCategories,
            labels: { 
                style: { colors: '#94a3b8' }, 
                formatter: function (val) { return val + "%";} 
            }
        },
        yaxis: {
            labels: { style: { fontSize: '16px', colors: '#94a3b8' } }
        },
        tooltip: {
            y: { formatter: (val) => `${val} pulls`}
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