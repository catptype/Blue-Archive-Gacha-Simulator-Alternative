<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { type Achievement } from '@/types/web';
import LoadSpinner from '@/components/base/LoadSpinner.vue';
import apiClient from '@/services/client';
import AchievementCard from '../components/achievement/AchievementCard.vue';

const isLoading = ref(true);
const error = ref('');
const allAchievements = ref<Achievement[]>([]);


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

const groupedAchievements = computed((): Record<string, Achievement[]> => {
  return allAchievements.value.reduce((groups, ach) => {
    const category = ach.category;
    // Initialize the array if it doesn't exist
    if (!groups[category]) {
      groups[category] = [];
    }
    groups[category].push(ach);
    return groups;
  }, {} as Record<string, Achievement[]>); // Type assertion on the initial value
});

// --- END OF CORRECTION ---
</script>

<template>
  <div class="flex flex-col h-full">
    <!-- Loading State -->
    <LoadSpinner v-if="isLoading" />
    
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
            :key="ach.id"
            :achievement="ach"
          />
        </div>
      </div>
    </div>
  </div>
  
</template>