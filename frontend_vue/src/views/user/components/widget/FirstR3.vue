<script setup lang="ts">
    import { ref, computed } from 'vue';
    import apiClient from '@/services/client';
    import ResultCard from '@/views/gacha/components/ResultCard.vue';
    import { type FirstR3 } from '@/types/web';

    const firstStudent = ref<FirstR3>( (await apiClient.get('/dashboard/summary/first-r3-pull')).data )

    // Create a computed property to format the date nicely.
    const formattedDate = computed(() => {
        if (!firstStudent || !firstStudent.value.first_obtain_on) return '';
        return new Date(firstStudent.value.first_obtain_on).toLocaleDateString(undefined, {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
        });
    });
</script>

<template>
  <div class="p-4 bg-slate-700/50 rounded-lg h-full flex flex-col items-center justify-between gap-4">
    <h3 class="text-xl font-semibold text-center">Your First ★★★</h3>
    
    <template v-if="firstStudent">
      <div>
        <ResultCard 
          :student="firstStudent.student" 
          :is-flipped="true" 
          :enable-effects="false" />
      </div>
      <p class="text-sm text-slate-400 mt-2">
        Pulled on {{ formattedDate }}
      </p>
    </template>
    
    <p v-else class="text-slate-400 text-center grow flex items-center">
      Keep pulling to find your first 3-star!
    </p>
  </div>
</template>