<script setup lang="ts">
import { ref, computed } from 'vue'; // <-- Make sure 'ref' is imported
import apiClient from '@/services/client';
import AchievementCard from './AchievementCard.vue';

// --- THIS IS THE CORRECTED PART ---

// 1. Create a reactive reference to hold the data. Initialize with an empty array.
const allAchievements = ref<any[]>([]);

// 2. Fetch the data and assign it to the .value of the ref.
const { data } = await apiClient.get('/dashboard/achievements');
allAchievements.value = data;

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
  <div class="flex flex-col gap-8">
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