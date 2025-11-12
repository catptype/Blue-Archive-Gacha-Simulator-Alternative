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
  <div class="flex flex-col gap-6">
    <!-- =============================================================== -->
    <!-- WIDGET 1: HEADER CARD                                           -->
    <!-- Contains the stats and filter controls in a single card.        -->
    <!-- =============================================================== -->
    <div class="p-4 bg-slate-700/50 rounded-lg">
      <div class="flex flex-col sm:flex-row items-center justify-between gap-4">
        <h2 class="text-xl font-semibold text-slate-300 whitespace-nowrap">
          Obtained ({{ collection.obtained_count }} / {{ collection.total_students }}) - {{ collection.completion_percentage.toFixed(2) }}% Complete
        </h2>
        <div class="flex items-center gap-2 p-1 bg-slate-800/50 rounded-lg">
          <button @click="activeFilter = 'all'" :class="getFilterButtonClass('all')" class="flex items-center gap-2">
            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" /></svg>
            <span>All</span>
          </button>
          <button @click="activeFilter = 'obtained'" :class="getFilterButtonClass('obtained')" class="flex items-center gap-2">
            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2z M14 11V7a4 4 0 118 0" /></svg>
            <span>Obtained</span>
          </button>
          <button @click="activeFilter = 'not-obtained'" :class="getFilterButtonClass('not-obtained')" class="flex items-center gap-2">
            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" /></svg>
            <span>Not Obtained</span>
          </button>
        </div>
      </div>
    </div>

    <!-- =============================================================== -->
    <!-- NEW: WIDGETS FOR EACH RARITY                                    -->
    <!-- We now loop over the rarities to create a card for each one.    -->
    <!-- =============================================================== -->
    <div v-for="rarity in [3, 2, 1]" :key="rarity">
      <!-- Only render the entire card if there are students to show for the current filter -->
      <div v-if="groupedStudents[rarity].length > 0" class="p-4 bg-slate-700/50 rounded-lg">
        <!-- Card Header -->
        <h3 class="text-2xl font-bold mb-4 flex items-center">
          <img v-for="i in rarity" :key="i" :src="starYellowImage" alt="star" class="w-8 h-8">
        </h3>
        <!-- Card Content: The Grid -->
        <div class="grid grid-cols-4 sm:grid-cols-6 md:grid-cols-8 lg:grid-cols-10 xl:grid-cols-12 gap-4">
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