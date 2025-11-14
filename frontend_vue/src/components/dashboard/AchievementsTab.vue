<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'; // <-- Make sure 'ref' is imported
import apiClient from '@/services/client';
import AchievementCard from './AchievementCard.vue';

// --- THIS IS THE CORRECTED PART ---

// 1. Create a reactive reference to hold the data. Initialize with an empty array.
const isLoading = ref(true);
const error = ref('');
const allAchievements = ref<any[]>([]); // Start with an empty array

// 2. Fetch the data and assign it to the .value of the ref.
// const { data } = await apiClient.get('/dashboard/achievements');
// allAchievements.value = data;

onMounted(async () => {
  isLoading.value = true;
  error.value = '';
  try {
    const { data } = await apiClient.get('/dashboard/achievements');
    allAchievements.value = data;
  } catch (err) {
    error.value = 'Failed to load achievements.';
    console.error(err);
  } finally {
    isLoading.value = false;
  }
});

// 3. The computed property now correctly accesses allAchievements.value
const groupedAchievements = computed(() => {
  // The check is now correct: it checks the ref's value.
  if (!allAchievements.value) return {}; 
  
  return allAchievements.value.reduce((groups: { [key: string]: any[] }, ach: any) => {
    const category = ach.achievement_category || 'UNCATEGORIZED';
    if (!groups[category]) {
      groups[category] = [];
    }
    groups[category].push(ach);
    return groups;
  }, {});
});

// --- END OF CORRECTION ---
</script>

<template>
  <!-- Loading State -->
  <div v-if="isLoading" class="flex h-full items-center justify-center">
    <svg class="animate-spin h-8 w-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path></svg>
  </div>
  
  <!-- Error State -->
  <div v-else-if="error" class="text-red-400 p-4">{{ error }}</div>
  <!-- Content -->
  <div v-else-if="groupedAchievements" class="flex flex-col gap-8">
    <div v-for="(achievements, category) in groupedAchievements" :key="category">
      
      <!-- Category Header with a clean bottom border -->
      <h2 class="text-2xl font-bold text-slate-300 capitalize pb-2 mb-4 border-b border-slate-600">
        {{ String(category).toLowerCase() }}
      </h2>

      <!-- 
        The grid is replaced with a single-column flex container.
        This gives our horizontal cards a clean, list-like appearance.
      -->
      <div class="flex flex-col gap-4">
        <AchievementCard
          v-for="ach in achievements"
          :key="ach.achievement_id"
          :achievement="ach"
        />
      </div>
    </div>
  </div>
</template>