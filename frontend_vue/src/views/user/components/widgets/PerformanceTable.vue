<script setup lang="ts">
  import { ref } from 'vue';
  import { type LuckPerformance } from '@/types/web';
  import apiClient from '@/services/client';
  import LuckTableRow from '../base/LuckTableRow.vue'; // Adjust path accordingly

  const response = await apiClient.get('/dashboard/summary/performance-table');
  const performances = ref<LuckPerformance[]>(response.data)

  const columns = [
    { label: 'Banner', align: 'text-left' },
    { label: 'Total Pulls', align: 'text-center' },
    { label: '★★★ Count', align: 'text-center' },
    { label: 'Your Rate', align: 'text-center' },
    { label: 'Banner Rate', align: 'text-center' },
    { label: 'Luck Variance', align: 'text-center' },
    { label: 'Shortest Gap', align: 'text-center' },
    { label: 'Average Gap', align: 'text-center' },
    { label: 'Longest Gap', align: 'text-center' },
  ];
</script>

<template>
  <div class="p-4 bg-slate-700/50 rounded-lg">
    <h3 class="text-xl text-center font-semibold mb-4">Luck Performance</h3>
    <div class="overflow-x-auto">
      <table class="w-full text-left text-sm whitespace-nowrap">
        <thead class="border-b border-slate-600">
          <tr>
            <th v-for="col in columns" 
              :key="col.label" 
              class="p-2" 
              :class="col.align">
              {{ col.label }}
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="!performances || performances.length === 0">
            <td :colspan="columns.length" class="text-center p-4 text-slate-400">
              No pull data available yet.
            </td>
          </tr>
          <LuckTableRow 
            v-for="data in performances" 
            :key="data.banner_name" 
            :performance="data" 
          />
        </tbody>
      </table>
    </div>
  </div>
</template>
