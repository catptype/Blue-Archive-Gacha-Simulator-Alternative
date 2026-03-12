<script setup lang="ts">
  import { ref, onMounted } from 'vue';
  import { type History } from '@/types/web';
  import apiClient from '@/services/client';
  import Pagination from '../components/history/Pagination.vue';
  import HistoryRow from '../components/history/HistoryRow.vue'; // Import the row component
  import LoadSpinner from '@/components/base/LoadSpinner.vue';

  const isLoading = ref(true);
  const error = ref('');
  const history = ref<History>({
    total_pages: 1,
    current_page: 1,
    items:[]
  });

  // Define headers in the script to reduce template boilerplate
  const tableHeaders = [
    { label: 'Date', width: 'w-[25%]' },
    { label: 'Banner', width: 'w-[25%]' },
    { label: 'Rarity', width: 'w-[10%]' },
    { label: 'Student', width: 'w-[40%]' }
  ];

  const fetchHistory = async (page = 1) => {
    isLoading.value = true;
    error.value = '';
    try {
      const response = await apiClient.get(`/dashboard/history?page=${page}&limit=5`);
      history.value = response.data;
    } catch (err) {
      error.value = 'Failed to load history.';
      console.error(err);
    } finally {
      isLoading.value = false;
    }
  };

  onMounted(() => fetchHistory(1));
</script>

<template>
  <div class="flex flex-col h-full">
    <!-- Loading State -->
    <LoadSpinner v-if="isLoading"/>
    
    <!-- Error State -->
    <div v-else-if="error" class="text-red-400 p-4">{{ error }}</div>

    <!-- Content -->
    <template v-else-if="history.items.length > 0">
      <div class="grow overflow-x-auto">
        <table class="w-full text-left align-middle text-white">
          <thead class="border-b border-slate-600 text-md">
            <tr class="text-center">
              <!-- Render Headers Dynamically -->
              <th 
                v-for="header in tableHeaders" 
                :key="header.label" 
                class="p-2" 
                :class="header.width"
              >
                {{ header.label }}
              </th>
            </tr>
          </thead>
          <tbody>
            <!-- Use the Row Component -->
            <HistoryRow 
              v-for="tx in history.items" 
              :key="tx.id" 
              :tx="tx" 
            />
          </tbody>
        </table>
      </div>
      
      <!-- Pagination Controls -->
      <div class="shrink-0 mt-4">
        <Pagination
          :current-page="history.current_page"
          :total-pages="history.total_pages"
          @change-page="fetchHistory"
        />
      </div>
    </template>
    
    <!-- Empty State -->
    <div v-else class="grow flex items-center justify-center text-slate-400">
      <p>You have no gacha history yet.</p>
    </div>
  </div>
</template>