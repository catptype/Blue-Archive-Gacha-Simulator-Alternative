<script setup lang="ts">
  import { type School } from '@/types/web'

  defineProps<{
    school: School;
    isActive: boolean;
  }>();

  const emit = defineEmits<{(e: 'select'): void;}>();
  const transition = "transition-all duration-300 ease-in-out" 
</script>

<template>
  <button
    @click="emit('select')"
    class="group w-full p-2 rounded-lg flex items-center hover:bg-sky-600/70"
    :class="[
      isActive 
        ? 'ring-2 ring-sky-400 bg-sky-600/40' 
        : 'bg-gray-600/80', 
      transition
    ]">
    
    <img 
      :src="school.image_url" 
      :alt="school.name" 
      class="h-12 w-12 object-contain shrink-0"
      :class="transition"
    >
    
    <span 
      class="ml-3 font-bold text-lg whitespace-nowrap overflow-hidden"
      :class="transition"
    >
      {{ school.name }}
    </span>
  </button>
</template>

<style scoped>
img {
  filter: drop-shadow(0 0 8px rgba(56, 189, 248, 0.8));
}
</style>