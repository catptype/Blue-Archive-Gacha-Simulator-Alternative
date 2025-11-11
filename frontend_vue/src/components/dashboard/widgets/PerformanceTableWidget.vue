<script setup lang="ts">
    import apiClient from '@/services/client';

    const { data } = await apiClient.get('/dashboard/summary/performance-table');

    // Helper function to determine the color for the luck variance
    const getLuckVarianceClass = (variance: number) => {
        if (variance > 0) return 'text-green-400';
        if (variance < 0) return 'text-red-400';
        return 'text-slate-400';
    };
</script>

<template>
  <div class="p-4 bg-slate-700/50 rounded-lg">
    <h3 class="text-xl font-semibold mb-4">Luck Performance</h3>
    <div class="overflow-x-auto">
      <table class="w-full text-left text-sm whitespace-nowrap">
        <thead class="border-b border-slate-600">
          <tr>
            <th class="p-2">Banner</th>
            <th class="p-2 text-center">Total Pulls</th>
            <th class="p-2 text-center">★★★ Count</th>
            <th class="p-2 text-center">Your Rate</th>
            <th class="p-2 text-center">Banner Rate</th>
            <th class="p-2 text-center">Luck Variance</th>
            <th class="p-2 text-center">Shortest Gap</th>
            <th class="p-2 text-center">Longest Gap</th>
            <th class="p-2 text-center">Average Gap</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="data.length === 0">
            <td colspan="9" class="text-center p-4 text-slate-400">No pull data available yet.</td>
          </tr>
          <tr v-for="analysis in data" :key="analysis.banner_name" class="border-b border-slate-700/50">
            <td class="p-2 font-bold">{{ analysis.banner_name }}</td>
            <td class="p-2 text-center">{{ analysis.total_pulls }}</td>
            <td class="p-2 text-center text-yellow-300 font-bold">{{ analysis.r3_count }}</td>
            <td class="p-2 text-center">{{ analysis.user_rate.toFixed(2) }}%</td>
            <td class="p-2 text-center">{{ analysis.banner_rate.toFixed(2) }}%</td>
            <td class="p-2 text-center font-bold" :class="getLuckVarianceClass(analysis.luck_variance)">
              {{ analysis.luck_variance > 0 ? '+' : '' }}{{ analysis.luck_variance.toFixed(2) }}%
            </td>
            <td class="p-2 text-center">{{ analysis.gaps?.min ?? 'N/A' }}</td>
            <td class="p-2 text-center">{{ analysis.gaps?.max ?? 'N/A' }}</td>
            <td class="p-2 text-center">{{ analysis.gaps?.avg ?? 'N/A' }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
