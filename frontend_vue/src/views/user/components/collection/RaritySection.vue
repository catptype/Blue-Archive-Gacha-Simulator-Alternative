<script setup lang="ts">
  import { type Student } from '@/types/web';
  import PortraitCard from './PortraitCard.vue';
  import starYellowImage from '@/assets/student_card/star_yellow.png';

  defineProps<{
    rarity: number;
    students: Student[];
  }>();
</script>

<template>
  <div v-if="students.length > 0" class="p-4 bg-slate-700/50 rounded-lg">
    <h3 class="text-2xl font-bold mb-4 flex items-center">
      <img v-for="i in rarity" :key="i" :src="starYellowImage" alt="star" class="w-8 h-8">
    </h3>
    
    <div class="grid grid-cols-4 md:grid-cols-6 xl:grid-cols-8 gap-4">
      <div v-for="student in students" :key="student.id" class="relative">
        <PortraitCard :student="student" />
      </div>
    </div>
  </div>
</template>