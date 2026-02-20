<script setup lang="ts">
  import { computed } from 'vue';
  import { type Top3Student, type Student } from '@/types/web';
  import PodiumSlot from './PodiumSlot.vue'; // Adjust path accordingly

  const props = defineProps<{ 
    topStudents: Top3Student[];
    rarity: number; 
  }>();

  const dummyStudent = computed<Student>(() => ({
    id: -1,
    name: 'Unknown',
    rarity: props.rarity,
    is_limited: false,
    version: { id: -1, name: '' },
    school: { id: -1, name: '', image_url: '' },
    portrait_url: '',
    artwork_url: '',
  }));

  const podiumData = computed(() => {
    return {
      first: props.topStudents[0],
      second: props.topStudents[1],
      third: props.topStudents[2]
    };
  });
</script>

<template>
  <div class="flex items-end justify-center gap-4 h-full text-center">
    <!-- Rank 1 (Order 2) -->
    <PodiumSlot 
      :rank="1" 
      :data="podiumData.first" 
      :dummy-student="dummyStudent" 
      :rarity="props.rarity" 
    />

    <!-- Rank 2 (Order 1) -->
    <PodiumSlot 
      :rank="2" 
      :data="podiumData.second" 
      :dummy-student="dummyStudent" 
      :rarity="props.rarity" 
    />

    <!-- Rank 3 (Order 3) -->
    <PodiumSlot 
      :rank="3" 
      :data="podiumData.third" 
      :dummy-student="dummyStudent" 
      :rarity="props.rarity" 
    />
  </div>
</template>