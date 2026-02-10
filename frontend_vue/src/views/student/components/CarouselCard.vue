<script setup lang="ts">
import { computed } from 'vue';
import { type Student } from '@/types/web'

const props = defineProps<{
  student: Student;
  isActive: boolean;
  useTransition: boolean;
}>();

// Move the getCardStyle logic here
const cardStyle = computed(() => ({
  transform: `scale(${props.isActive ? 1.15 : 0.9})`,
  opacity: props.isActive ? '1' : '0.5',
  filter: props.isActive ? 'none' : 'grayscale(1)',
}));

// Move the getCardNameStyle logic here
const nameClasses = computed(() => ({
  'opacity-100 translate-x-0': props.isActive,
  'opacity-0 -translate-x-8': !props.isActive,
}));
</script>

<template>
  <div
    class="character-card shrink-0 w-[300px] h-[85%] mx-4"
    :class="{ 'transition-all duration-500 ease-in-out': useTransition }"
    :style="cardStyle"
  >
    <div class="relative w-full h-full group">
      <img 
        :src="student.portrait_url" 
        :alt="student.name" 
        class="w-full h-full object-cover rounded-lg"
      >
      
      <div
        class="character-name absolute bottom-5 left-[70px]"
        :class="[nameClasses, { 'transition-all duration-500 ease-in-out': useTransition }]"
      >
        <h2 
          class="text-5xl font-black text-white uppercase tracking-widest origin-bottom-left transform -rotate-90"
          style="text-shadow: 2px 2px 10px rgba(0, 0, 0, 0.7);"
        >
          {{ student.name }}
        </h2>
      </div>
    </div>
  </div>
</template>