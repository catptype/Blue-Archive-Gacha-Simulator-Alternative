<script setup lang="ts">
    import { computed } from 'vue';
    import ResultCard from '../../../components/gacha/ResultCard.vue';
    // Import rank images (make sure they are in src/assets)
    import rank1Image from '../../../assets/rank1.png';
    import rank2Image from '../../../assets/rank2.png';
    import rank3Image from '../../../assets/rank3.png';

    // defineProps<{ topStudents: any[] }>();

    const props = defineProps<{ 
        topStudents: any[];
        rarity: number; // The active rarity (3, 2, or 1)
    }>();

    // --- THIS IS THE KEY LOGIC ---
    // Create a computed property that always returns an array of length 3.
    const podium = computed(() => {
    const padded = [...props.topStudents];
    while (padded.length < 3) {
        padded.push(null);
    }
    return padded;
    });

    // Create a dummy/placeholder student object that ResultCard can use.
    // It needs the same structure as a real student to avoid template errors.
    const placeholderStudent = {
        student_rarity: props.rarity, // Default to a 1-star card back
        is_pickup: false,
        is_new: false,
        student_id: -1,
        student_name: 'Unknown',
        portrait_url: '',
        school: { school_name: '', image_url: '' },
        version: { version_name: '' },
    };
</script>

<template>
  <div class="flex items-end justify-center gap-4 h-full text-center">
    
    <!-- 2nd Place -->
    <div class="order-1 flex flex-col items-center">
      <div class="w-[220px]">
        <!-- Conditionally render the ResultCard or a placeholder -->
        <ResultCard v-if="podium[1]" :student="podium[1].student" :is-flipped="true" />
        <ResultCard v-else :student="placeholderStudent" :is-flipped="false" />
      </div>
      <div class="w-full h-24 rounded-t-md mt-2 bg-slate-600/50 flex items-center justify-center">
        <!-- <p v-if="podium[1]" class="font-bold text-slate-300">x{{ podium[1].count }}</p> -->
      </div>
      <div class="absolute bottom-3 flex flex-col items-center">
        <img :src="rank2Image" class="w-14 h-14 object-cover">
        <span class="font-bold text-md -mt-4 text-white" style="text-shadow: 1px 1px 3px #000;">2nd</span>
      </div>
    </div>

    <!-- 1st Place -->
    <div class="order-2 flex flex-col items-center">
      <div class="w-[220px]">
        <ResultCard v-if="podium[0]" :student="podium[0].student" :is-flipped="true" />
        <ResultCard v-else :student="placeholderStudent" :is-flipped="false" />
      </div>
      <div class="w-full h-28 rounded-t-md mt-2 bg-slate-600/50 flex items-center justify-center">
        <!-- <p v-if="podium[0]" class="font-bold text-slate-300">x{{ podium[0].count }}</p> -->
      </div>
      <div class="absolute bottom-7 flex flex-col items-center">
        <img :src="rank1Image" class="w-14 h-14 object-cover">
        <span class="font-bold text-md -mt-4 text-white" style="text-shadow: 1px 1px 3px #000;">1st</span>
      </div>
    </div>

    <!-- 3rd Place -->
    <div class="order-3 flex flex-col items-center">
      <div class="w-[220px]">
        <ResultCard v-if="podium[2]" :student="podium[2].student" :is-flipped="true" />
        <ResultCard v-else :student="placeholderStudent" :is-flipped="false" />
      </div>
      <div class="w-full h-20 rounded-t-md mt-2 bg-slate-600/50 flex items-center justify-center">
        <!-- <p v-if="podium[2]" class="font-bold text-slate-300">x{{ podium[2].count }}</p> -->
      </div>
      <div class="absolute bottom-0 flex flex-col items-center">
        <img :src="rank3Image" class="w-14 h-14 object-cover">
        <span class="font-bold text-md -mt-4 text-white" style="text-shadow: 1px 1px 3px #000;">3rd</span>
      </div>
    </div>

  </div>
</template>
