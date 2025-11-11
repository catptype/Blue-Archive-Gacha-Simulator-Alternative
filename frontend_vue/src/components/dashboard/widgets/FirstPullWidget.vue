<script setup lang="ts">
    import { computed } from 'vue';
    import apiClient from '@/services/client';
    import ResultCard from '@/components/gacha/ResultCard.vue';

    // Use async setup to fetch data. The parent's <Suspense> will handle the loading state.
    const { data } = await apiClient.get('/dashboard/summary/first-r3-pull');

    // Create a computed property to format the date nicely.
    const formattedDate = computed(() => {
        if (!data || !data.transaction_create_on) return '';
        // Use toLocaleDateString for a user-friendly date format
        return new Date(data.transaction_create_on).toLocaleDateString(undefined, {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
        });
    });
</script>

<template>
  <div class="p-4 bg-slate-700/50 rounded-lg h-full flex flex-col items-center justify-between gap-4">
    <h3 class="text-xl font-semibold text-center">Your First ★★★</h3>
    
    <!-- Data exists state -->
    <template v-if="data">
      <div >
        <!-- Reuse the ResultCard component for a consistent look -->
        <ResultCard :student="data.student" :is-flipped="true" />
      </div>
      <p class="text-sm text-slate-400 mt-2">
        Pulled on {{ formattedDate }}
      </p>
    </template>
    
    <!-- No data state -->
    <p v-else class="text-slate-400 text-center flex-grow flex items-center">
      Keep pulling to find your first 3-star!
    </p>
  </div>
</template>