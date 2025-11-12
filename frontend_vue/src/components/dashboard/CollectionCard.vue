<script setup lang="ts">
    defineProps<{ student: any }>();
</script>

<template>
  <div class="relative aspect-square rounded-lg overflow-hidden group transition-all duration-300">
    <!-- Student Portrait (Full color if obtained, grayscale if not) -->
    <img
      :src="student.portrait_url"
      :alt="student.student_name"
      class="w-full h-full object-cover transition-transform duration-300 group-hover:scale-110"
      :class="{ 'grayscale': !student.is_obtained }"
    />

    <!-- Lock Overlay (for un-obtained students) -->
    <div
      v-if="!student.is_obtained"
      class="absolute inset-0 flex items-center justify-center bg-black/60"
    >
      <svg class="h-12 w-12 text-slate-400" viewBox="0 0 20 20" fill="currentColor">
        <path fill-rule="evenodd" d="M10 1a4.5 4.5 0 00-4.5 4.5V9H5a2 2 0 00-2 2v6a2 2 0 002 2h10a2 2 0 002-2v-6a2 2 0 00-2-2h-.5V5.5A4.5 4.5 0 0010 1zm3 8V5.5a3 3 0 10-6 0V9h6z" clip-rule="evenodd" />
      </svg>
    </div>

    <!-- Info Overlay (Visible on hover for obtained students) -->
    <div
      v-if="student.is_obtained"
      class="absolute inset-0 bg-gradient-to-t from-black/80 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 p-2 flex flex-col justify-end"
    >
      <h4 class="font-bold text-white text-sm truncate">{{ student.student_name }}</h4>
      <div class="flex">
        <span v-for="i in student.student_rarity" :key="i" class="text-yellow-400">★</span>
      </div>
    </div>
  </div>
</template>