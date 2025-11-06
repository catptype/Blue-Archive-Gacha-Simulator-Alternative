<script setup lang="ts">
    import { ref } from 'vue';
    import apiClient from '../../../services/client';
    
    const topStudents = ref<any[] | null>(null);
    const activeRarity = ref(3);
    const fetchTopStudents = async (rarity: number) => {
        activeRarity.value = rarity;
        const { data } = await apiClient.get(`/dashboard/summary/top-students/${rarity}`);
        topStudents.value = data;
    };
    // Initial fetch for 3-star students
    await fetchTopStudents(3);
</script>

<template>
  <div class="p-4 bg-slate-700/50 rounded-lg">
    <h3 class="text-xl font-bold mb-4">Top Pulled Students</h3>
    <!-- Tab buttons to switch rarity -->
    <div class="flex gap-2 mb-4">
      <button @click="fetchTopStudents(3)" :class="{ 'bg-pink-500': activeRarity === 3 }">★★★</button>
      <button @click="fetchTopStudents(2)" :class="{ 'bg-yellow-500': activeRarity === 2 }">★★</button>
      <button @click="fetchTopStudents(1)" :class="{ 'bg-blue-500': activeRarity === 1 }">★</button>
    </div>
    <!-- Podium display -->
    <div v-if="topStudents" class="flex justify-around items-end">
      <!-- Logic to display the 3 top students with different heights for 1st, 2nd, 3rd -->
      <div v-for="(item, index) in topStudents" :key="item.student.student_id">
        <p>{{ item.student.student_name }} (x{{ item.count }})</p>
      </div>
    </div>
  </div>
</template>