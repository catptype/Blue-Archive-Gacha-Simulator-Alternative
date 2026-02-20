<script setup lang="ts">
    import { computed } from 'vue';
    import { type Top3Student, type Student } from '@/types/web';
    import ResultCard from '@/views/gacha/components/ResultCard.vue';
    import rank1Image from '@/assets/rank1.png';
    import rank2Image from '@/assets/rank2.png';
    import rank3Image from '@/assets/rank3.png';

    const dummyStudent = computed<Student>(() => ({
        id: -1,
        name: 'Unknown',
        rarity: props.rarity, // Now this will update whenever props.rarity changes
        is_limited: false,
        version: { id: -1, name: '' },
        school: { id: -1, name: '', image_url: '' },
        portrait_url: '',
        artwork_url: '',
    }));

    const props = defineProps<{ 
        topStudents: Top3Student[];
        rarity: number; // The active rarity (3, 2, or 1)
    }>();

    // Create a computed property that always returns an array of length 3.
    const podium = computed<(Top3Student | null)[]>(() => {
      const padded: (Top3Student | null)[] = [...props.topStudents];
      while (padded.length < 3) {
          padded.push(null);
      }
      return padded;
    });
    
</script>

<template>
  <div class="flex items-end justify-center gap-4 h-full text-center">
    
    <!-- 2nd Place -->
    <div class="order-1 flex flex-col items-center">

      <!-- Card -->
      <div class="w-[220px]">
        <ResultCard v-if="podium[1]"
          :key="podium[1].student.id"  
          :student="podium[1].student" 
          :is-flipped="true" 
          :enable-effects="false" />
        <ResultCard v-else 
          :key="'dummy-' + props.rarity" 
          :student="dummyStudent" 
          :is-flipped="false" />
      </div>
      
      <!-- Podium -->
      <div class="w-full h-24 rounded-t-md mt-2 bg-slate-600/50 flex items-center justify-center"></div>
      
      <!-- Rank Icon -->
      <div class="absolute bottom-3 flex flex-col items-center">
        <img :src="rank2Image" alt="rank2" class="w-14 h-14 object-cover">
        <span class="font-bold text-md -mt-4 text-white" style="text-shadow: 1px 1px 3px #000;">2nd</span>
      </div>
    </div>

    <!-- 1st Place -->
    <div class="order-2 flex flex-col items-center">
      
      <!-- Card -->
      <div class="w-[220px]">
        <ResultCard v-if="podium[0]" 
          :key="podium[0].student.id"  
          :student="podium[0].student" 
          :is-flipped="true" 
          :enable-effects="false" />
        <ResultCard v-else 
          :key="'dummy-' + props.rarity" 
          :student="dummyStudent" 
          :is-flipped="false" />
      </div>
      
      <!-- Podium -->
      <div class="w-full h-28 rounded-t-md mt-2 bg-slate-600/50 flex items-center justify-center"></div>
      
      <!-- Rank Icon -->
      <div class="absolute bottom-7 flex flex-col items-center">
        <img :src="rank1Image" alt="rank1" class="w-14 h-14 object-cover">
        <span class="font-bold text-md -mt-4 text-white" style="text-shadow: 1px 1px 3px #000;">1st</span>
      </div>
    </div>

    <!-- 3rd Place -->
    <div class="order-3 flex flex-col items-center">
      
      <!-- Card -->
      <div class="w-[220px]">
        <ResultCard v-if="podium[2]"
          :key="podium[2].student.id" 
          :student="podium[2].student" 
          :is-flipped="true" :enable-effects="false" />
        <ResultCard v-else 
          :key="'dummy-' + props.rarity"   
          :student="dummyStudent" 
          :is-flipped="false" />
      </div>
      
      <!-- Podium -->
      <div class="w-full h-20 rounded-t-md mt-2 bg-slate-600/50 flex items-center justify-center"></div>
      
      <!-- Rank Icon -->
      <div class="absolute bottom-0 flex flex-col items-center">
        <img :src="rank3Image" alt="rank3" class="w-14 h-14 object-cover">
        <span class="font-bold text-md -mt-4 text-white" style="text-shadow: 1px 1px 3px #000;">3rd</span>
      </div>
    </div>

  </div>
</template>
