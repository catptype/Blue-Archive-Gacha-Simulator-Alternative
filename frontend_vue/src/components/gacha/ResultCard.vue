<script setup lang="ts">
    import { computed } from 'vue';
    import gachaR3Image from '@/assets/student_card/gacha_r3.png';
    import gachaR2Image from '@/assets/student_card/gacha_r2.png';
    import gachaR1Image from '@/assets/student_card/gacha_r1.png';
    import yellowStarImage from '@/assets/student_card/star_yellow.png'
    import newImage from '@/assets/student_card/imgfont_new.png'
    import pickupImage from '@/assets/student_card/imgfont_pickup.png'

    // Define a more detailed interface for the student prop
    interface Student {
        student_id: number;
        student_name: string;
        student_rarity: number;
        portrait_url: string;
        is_pickup: boolean; // Assumes API provides this
        is_new: boolean;    // Assumes API provides this
        school: {
            school_name: string;
            image_url: string;
        };
        version: {
            version_name: string;
        };
    }

    // const props = defineProps<{ student: Student }>();
    // const isFlipped = ref(false);
    const props = withDefaults(defineProps<{ 
      student: Student;
      isFlipped: boolean; 
      enableEffects?: boolean; // New optional prop
    }>(), {
      enableEffects: true, // Default to true
    });

    // --- Computed Properties for Dynamic Styling ---

    const cardBackImage = computed(() => {
        if (props.student.student_rarity === 3) return gachaR3Image;
        if (props.student.student_rarity === 2) return gachaR2Image;
        return gachaR1Image;
    });

    const rarityBorderClass = computed(() => ({
        'bg-gradient-to-br from-pink-400 via-purple-400 to-cyan-400': props.student.student_rarity === 3,
        'bg-yellow-400/80': props.student.student_rarity === 2,
        'bg-blue-400/80': props.student.student_rarity === 1,
    }));

    const schoolPillClass = computed(() => ({
        'bg-gradient-to-r from-pink-200 to-cyan-200 border-purple-400/80': props.student.student_rarity === 3,
        'bg-yellow-200 border-yellow-400/80': props.student.student_rarity === 2,
        'bg-blue-200 border-blue-400/80': props.student.student_rarity === 1,
    }));

    const rarityPillClass = computed(() => ({
        'bg-gradient-to-br from-pink-400 via-purple-400 to-cyan-400': props.student.student_rarity === 3,
        'bg-yellow-500 border-2 border-yellow-300/50': props.student.student_rarity === 2,
        'bg-blue-500 border-2 border-blue-300/50': props.student.student_rarity === 1,
    }));

    const rarityLineClass = computed(() => ({
        'bg-gradient-to-r from-pink-400 to-purple-400': props.student.student_rarity === 3,
        'bg-yellow-400': props.student.student_rarity === 2,
        'bg-blue-400': props.student.student_rarity === 1,
    }));

</script>

<template>
  <div class="student-card-flipper w-[220px] aspect-[3.5/5]" :class="{ 'cursor-pointer': enableEffects }" style="perspective: 1000px;">
    <!-- This inner div is the part that actually performs the 3D transition. -->
    <div class="relative w-full h-full transition-transform duration-700 ease-in-out" :class="{ 'is-flipped': isFlipped }" style="transform-style: preserve-3d;">
        
      <!-- CARD BACK -->
      <div class="absolute w-full h-full rounded-lg shadow-2xl overflow-hidden" style="backface-visibility: hidden;">
        <img :src="cardBackImage" class="w-full h-full object-cover">
      </div>

      <!-- CARD FRONT -->
      <div class="absolute w-full h-full" style="backface-visibility: hidden; transform: rotateY(180deg);">
        <!-- Main card structure with rarity-based border gradient -->
        <div class="relative w-full h-full rounded-lg shadow-2xl p-1" :class="rarityBorderClass">
          <div class="relative w-full h-full bg-white rounded-sm overflow-hidden flex flex-col">
            <!-- Portrait Section -->
            <div class="relative flex-[8] bg-slate-200">
              <div class="absolute inset-[12px] overflow-hidden" style="clip-path: polygon(12px 0, 100% 0, 100% calc(100% - 12px), calc(100% - 12px) 100%, 0 100%, 0 12px);">
                <img v-if="student.portrait_url" :src="student.portrait_url" :alt="student.student_name" class="w-full h-full object-cover">
                <div class="absolute inset-0 pointer-events-none" style="box-shadow: inset 0 0 10px 4px rgba(0, 0, 0, 0.5);"></div>
              </div>
              <div class="absolute top-0 left-3 h-8 px-3 rounded-b-md flex items-center gap-2 border-x-2 border-b-2" :class="schoolPillClass">
                <img :src="student.school.image_url" alt="" class="w-5 h-5 bg-white rounded-full p-0.5">
                <span class="text-xs font-bold text-slate-900">{{ student.school.school_name }}</span>
              </div>
            </div>
            <!-- Info Section -->
            <div class="flex-[2] flex flex-col justify-center px-3 py-2 bg-gray-100 border-t-2 border-gray-300">
              <div class="relative h-7 mb-2 flex items-center justify-center">
                <div class="absolute left-0 top-1/2 w-[25%] h-[2px]" :class="rarityLineClass"></div>
                <div class="relative h-full w-19 flex-shrink-0 flex items-center justify-center gap-0 rounded-full shadow-inner-sm" :class="rarityPillClass">
                  <img v-for="i in student.student_rarity" :key="i" :src="yellowStarImage" alt="star" class="w-4 h-4">
                </div>
                <div class="absolute right-0 top-1/2 w-[25%] h-[2px]" :class="rarityLineClass"></div>
              </div>
              <div class="text-center">
                <h2 class="text-lg font-bold text-gray-800 truncate" :title="student.student_name">{{ student.student_name }}</h2>
                <p v-if="student.version.version_name !== 'Original'" class="text-xs text-slate-500 -mt-1">({{ student.version.version_name }})</p>
              </div>
            </div>
          </div>
        </div>

        <!-- "PICKUP" Indicator -->
        <div v-if="student.is_pickup" class="absolute bottom-0 right-0 w-24 h-24 transform -rotate-12 translate-x-6 translate-y-16 pointer-events-none">
          <img :src="pickupImage" alt="Pickup">
        </div>
        
        <!-- "NEW" Indicator -->
        <div v-if="student.is_new" class="absolute top-0 left-0 w-20 h-20 transform -rotate-12 -translate-x-5 -translate-y-5 pointer-events-none">
          <img :src="newImage" alt="New">
        </div>

        <!-- 3-Star Special Effects -->
        <template v-if="student.student_rarity === 3 && enableEffects">
          <div class="card-shine-overlay absolute inset-0 rounded-lg"></div>
          <div class="afterglow absolute inset-[-4px] rounded-lg pointer-events-none"></div>
          <div class="sparkle-overlay absolute inset-0">
            <div v-for="i in 5" :key="i" class="sparkle"></div>
          </div>
        </template>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Paste the animation CSS from your Django template's <style> block here. */
/* This encapsulates all the visual logic within the component. */
.is-flipped {
  transform: rotateY(180deg);
}

.card-shine-overlay {
  position: absolute;
  inset: 0;
  overflow: hidden;
}
.card-shine-overlay::before {
  content: '';
  position: absolute;
  top: -150%;
  left: -150%;
  width: 60px;
  height: 400%;
  background: linear-gradient( to right, transparent 0%, rgba(255, 255, 255, 0.5) 50%, transparent 100% );
  transform: rotate(-45deg);
  opacity: 0;
}
.is-flipped .card-shine-overlay::before {
  animation: card-shine-anim 0.7s ease-in-out;
  animation-delay: 0.2s; 
}
@keyframes card-shine-anim {
  0% { left: -150%; opacity: 1; }
  100% { left: 150%; opacity: 1; }
}

.sparkle {
  position: absolute;
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transform: scale(0);
}
.sparkle::before {
  content: '✦'; 
  font-size: 32px;
  color: white;
  text-shadow: 0 0 5px #fff, 0 0 10px #f0f, 0 0 15px #0ff;
}
.is-flipped .sparkle:nth-child(1) { top: 10%; left: 20%; animation: sparkle-anim 0.7s ease-out 0.4s forwards; }
.is-flipped .sparkle:nth-child(2) { top: 80%; left: 30%; animation: sparkle-anim 0.7s ease-out 0.5s forwards; }
.is-flipped .sparkle:nth-child(3) { top: 30%; left: 80%; animation: sparkle-anim 0.7s ease-out 0.6s forwards; }
.is-flipped .sparkle:nth-child(4) { top: 50%; left: 50%; animation: sparkle-anim 0.7s ease-out 0.7s forwards; }
.is-flipped .sparkle:nth-child(5) { top: 90%; left: 70%; animation: sparkle-anim 0.7s ease-out 0.8s forwards; }
@keyframes sparkle-anim {
  0% { transform: scale(0) rotate(0deg); opacity: 0; }
  50% { transform: scale(1.5) rotate(90deg); opacity: 1; }
  100% { transform: scale(0) rotate(180deg); opacity: 0; }
}

.is-flipped .afterglow {
  animation: afterglow-anim 1s infinite linear;
}
@keyframes afterglow-anim {
  0%   { box-shadow: 0 0 25px 8px rgba(56, 189, 248, 0.7); }
  33%  { box-shadow: 0 0 25px 8px rgba(244, 114, 182, 0.7); }
  66%  { box-shadow: 0 0 25px 8px rgba(192, 132, 252, 0.7); }
  100% { box-shadow: 0 0 25px 8px rgba(56, 189, 248, 0.7); }
}
</style>