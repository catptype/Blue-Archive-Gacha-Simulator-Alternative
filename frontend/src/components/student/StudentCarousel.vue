<script setup lang="ts">
import LoadingSpinner from '../LoadingSpinner.vue';

interface Student {
  student_id: string;
  student_name: string;
  image_url: string;
}

defineProps<{
  students: Student[];
  isLoading: boolean;
}>();
</script>

<template>
  <div class="h-full relative overflow-hidden">
    <div class="w-full h-full">
      <!-- Show spinner if loading -->
      <LoadingSpinner v-if="isLoading" />
      
      <!-- Show student list if not loading -->
      <div v-else class="w-full h-full flex items-center p-8 gap-4 overflow-x-auto">
        <div v-for="student in students" :key="student.student_id" class="flex-shrink-0 text-center">
           <!-- Placeholder for a student card -->
           <div class="w-48 h-64 bg-slate-800/50 rounded-lg flex flex-col items-center justify-center border-2 border-slate-700">
             <img :src="student.image_url" alt="Student Art" class="w-32 h-32 rounded-full object-cover mb-4">
             <p class="font-bold text-white">{{ student.student_name }}</p>
           </div>
        </div>
      </div>
    </div>
  </div>
</template>

