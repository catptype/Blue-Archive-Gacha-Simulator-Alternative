<script setup lang="ts">
import { ref, onMounted } from 'vue';
import apiClient from '@/services/client';
import Pagination from './Pagination.vue'; // Import the new component

const isLoading = ref(true);
const error = ref('');
const history = ref<any>({ items: [], total_pages: 0, current_page: 1 });

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

const rarityColor = (rarity: number) => ({
  'text-pink-400': rarity === 3,
  'text-yellow-400': rarity === 2,
  'text-blue-400': rarity === 1,
});

// Initial fetch when the component is mounted
onMounted(() => fetchHistory(1));
</script>

<template>
  <div class="flex flex-col h-full">
    <!-- Loading State -->
    <div v-if="isLoading" class="flex-grow flex items-center justify-center">
      <svg class="animate-spin h-8 w-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path></svg>
    </div>
    
    <!-- Error State -->
    <div v-else-if="error" class="text-red-400 p-4">{{ error }}</div>

    <!-- Content -->
    <template v-else-if="history.items.length > 0">
      <div class="flex-grow overflow-x-auto">
        <table class="w-full text-left align-middle">
          <thead class="border-b border-slate-600 text-md text-slate-400">
            <tr>
              <th class="p-2 w-[25%]">Date</th>
              <th class="p-2 w-[25%]">Banner</th>
              <th class="p-2 w-[10%] text-center">Rarity</th>
              <th class="p-2 w-[40%]">Student</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="tx in history.items"
              :key="tx.transaction_id"
              class="border-b border-slate-700"
              :class="{ 'font-semibold bg-gradient-to-r from-pink-500/20 via-purple-500/20 to-cyan-500/20': tx.student.student_rarity === 3 }"
            >
              <td class="p-2 text-slate-400">{{ new Date(tx.transaction_create_on).toLocaleString() }}</td>
              <td class="p-2">
                <img v-if="tx.banner.image_url" :src="tx.banner.image_url" class="w-48 h-auto rounded-md object-cover">
                <span v-else>{{ tx.banner.banner_name }}</span>
              </td>
              <td class="p-2 text-lg text-center" :class="rarityColor(tx.student.student_rarity)">
                <span v-for="i in tx.student.student_rarity" :key="i">★</span>
              </td>
              <td class="p-2 text-lg">
                {{ tx.student.student_name }}
                <span v-if="tx.student.version.version_name !== 'Original'" class="text-sm text-slate-400">
                  ({{ tx.student.version.version_name }})
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <!-- Pagination Controls -->
      <div class="flex-shrink-0 mt-4">
        <Pagination
          :current-page="history.current_page"
          :total-pages="history.total_pages"
          @change-page="fetchHistory"
        />
      </div>
    </template>
    
    <!-- Empty State -->
    <div v-else class="flex-grow flex items-center justify-center text-slate-400">
      <p>You have no gacha history yet.</p>
    </div>
  </div>
</template>