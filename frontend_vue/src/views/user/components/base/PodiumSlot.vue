<!-- @/views/gacha/components/PodiumSlot.vue -->
<script setup lang="ts">
import { computed } from 'vue';
import { type Top3Student, type Student } from '@/types/web';
import ResultCard from '@/views/gacha/components/ResultCard.vue';
import rank1Image from '@/assets/rank1.png';
import rank2Image from '@/assets/rank2.png';
import rank3Image from '@/assets/rank3.png';

const props = defineProps<{
  rank: 1 | 2 | 3;
  data: Top3Student | undefined;
  dummyStudent: Student;
  rarity: number;
}>();

// Configuration mapping based on rank
const rankConfig = computed(() => {
  const configs = {
    1: { order: 'order-2', height: 'h-28', bottom: 'bottom-7', img: rank1Image, label: '1st' },
    2: { order: 'order-1', height: 'h-24', bottom: 'bottom-3', img: rank2Image, label: '2nd' },
    3: { order: 'order-3', height: 'h-20', bottom: 'bottom-0', img: rank3Image, label: '3rd' },
  };
  return configs[props.rank];
});
</script>

<template>
  <div :class="['flex flex-col items-center', rankConfig.order]">
    <!-- Card -->
    <div class="w-[220px]">
      <ResultCard 
        v-if="data"
        :key="data.student.id"  
        :student="data.student" 
        :is-flipped="true" 
        :enable-effects="false" 
      />
      <ResultCard 
        v-else 
        :key="'dummy-' + rarity" 
        :student="dummyStudent" 
        :is-flipped="false" 
      />
    </div>
    
    <!-- Podium Step -->
    <div :class="[rankConfig.height, 'relative w-full rounded-t-md mt-2 bg-slate-600/50 flex flex-col items-center justify-start']">
      <!-- Rank Icon -->
      <img :src="rankConfig.img" :alt="'rank' + rank" class="w-14 h-14 object-cover">
      <span class="font-bold text-md -mt-3 text-white" style="text-shadow: 1px 1px 3px #000;">
        {{ rankConfig.label }}
      </span>
    </div>
    
    
  </div>
</template>