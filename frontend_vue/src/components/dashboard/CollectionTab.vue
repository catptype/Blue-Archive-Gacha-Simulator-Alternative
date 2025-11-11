<script setup lang="ts">
import { ref, computed } from 'vue';
import apiClient from '@/services/client';
import CollectionCard from './CollectionCard.vue';
import starYellowImage from '@/assets/student_card/star_yellow.png';

// Use async setup for clean data fetching
const { data: collection } = await apiClient.get('/dashboard/collection');

// --- State Management ---
const activeFilter = ref<'all' | 'obtained' | 'not-obtained'>('all');

// --- Computed Properties for Filtering and Grouping ---
const filteredStudents = computed(() => {
  if (activeFilter.value === 'obtained') {
    return collection.students.filter(s => s.is_obtained);
  }
  if (activeFilter.value === 'not-obtained') {
    return collection.students.filter(s => !s.is_obtained);
  }
  return collection.students; // 'all'
});

const groupedStudents = computed(() => {
  const groups: { [key: number]: any[] } = { 3: [], 2: [], 1: [] };
  for (const student of filteredStudents.value) {
    groups[student.student_rarity]?.push(student);
  }
  return groups;
});

// --- Helper for dynamic button styling ---
const getFilterButtonClass = (filter: string) => {
  const base = 'px-3 py-1 rounded-md text-sm font-semibold transition-colors';
  if (activeFilter.value === filter) {
    return `${base} bg-cyan-600 text-white`;
  }
  return `${base} text-slate-400 hover:bg-slate-600`;
};
</script>

<template>
  <div>
    <!-- Header with Stats and Filters -->
    <div class="flex flex-col sm:flex-row items-center justify-between mb-6 gap-4">
      <h2 class="text-xl font-semibold text-slate-300">
        Obtained ({{ collection.obtained_count }} / {{ collection.total_students }}) - {{ collection.completion_percentage.toFixed(2) }}% Complete
      </h2>
      <div class="flex items-center gap-2 p-1 bg-slate-700/50 rounded-lg">
        <button @click="activeFilter = 'all'" :class="getFilterButtonClass('all')">All</button>
        <button @click="activeFilter = 'obtained'" :class="getFilterButtonClass('obtained')">Obtained</button>
        <button @click="activeFilter = 'not-obtained'" :class="getFilterButtonClass('not-obtained')">Not Obtained</button>
      </div>
    </div>

    <!-- Grouped Student Display -->
    <div class="flex flex-col gap-8">
      <div v-for="rarity in [3, 2, 1]" :key="rarity">
        <h3 class="text-2xl font-bold mb-4 flex items-center">
          <img v-for="i in rarity" :key="i" :src="starYellowImage" alt="star" class="w-8 h-8">
        </h3>
        <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4">
          <CollectionCard
            v-for="student in groupedStudents[rarity]"
            :key="student.student_id"
            :student="student"
          />
        </div>
      </div>
    </div>
  </div>
</template>