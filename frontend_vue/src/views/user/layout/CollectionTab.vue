<script setup lang="ts">
  import { ref, computed, onMounted } from 'vue';
  import { type Collection, type Student } from '@/types/web';
  import LoadSpinner from '@/components/base/LoadSpinner.vue';
  import apiClient from '@/services/client';

  // Imported Components
  import CollectionHeader from '../components/collection/CollectionHeader.vue';
  import RaritySection from '../components/collection/RaritySection.vue';

  const isLoading = ref(true);
  const error = ref('');
  const collection = ref<Collection>();
  const activeFilter = ref<'all' | 'obtained' | 'not-obtained'>('all');

  const filteredStudents = computed(() => {
    if (!collection.value) return [];
    if (activeFilter.value === 'obtained') return collection.value.students.filter(s => s.is_obtained);
    if (activeFilter.value === 'not-obtained') return collection.value.students.filter(s => !s.is_obtained);
    return collection.value.students;
  });

  const groupedStudents = computed(() => {
    const groups: Record<number, Student[]> = { 3: [], 2: [], 1: [] };
    filteredStudents.value.forEach(student => {
      const r = student.rarity;
      if (groups[r]) groups[r].push(student);
    });
    return groups;
  });

  onMounted(async () => {
    try {
      const response = await apiClient.get('/dashboard/collection');
      collection.value = response.data;
    } catch (err) {
      error.value = 'Failed to load collection data.';
    } finally {
      isLoading.value = false;
    }
  });
</script>

<template>
  <div class="flex flex-col h-full">
    <!-- Loading State -->
    <LoadSpinner v-if="isLoading" />

    <!-- Error State -->
    <div v-else-if="error" class="text-red-400 p-4">{{ error }}</div>

    <!-- Content -->
    <div v-else-if="collection" class="flex flex-col gap-6">
      <CollectionHeader 
        :active-filter="activeFilter"
        :obtained-count="collection.obtained_count"
        :total-count="collection.total_count"
        :percentage="collection.completion_percentage"
        @update:filter="activeFilter = $event"
      />

      <RaritySection 
        v-for="rarity in [3, 2, 1]" 
        :key="rarity"
        :rarity="rarity"
        :students="groupedStudents[rarity] ?? []"
      />
    </div>
  </div>
  
</template>