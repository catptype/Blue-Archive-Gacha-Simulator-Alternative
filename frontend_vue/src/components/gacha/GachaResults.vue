<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue';
import ResultCard from './ResultCard.vue';

const props = defineProps<{ results: any[] }>();
const emit = defineEmits(['close']);

const flippedStates = ref<boolean[]>(props.results.map(() => false));

// --- NEW COMPUTED PROPERTY TO TRACK REVEAL STATE ---
// This will be true only when every value in the flippedStates array is true.
const allCardsRevealed = computed(() => {
  // For a single pull, it's "revealed" as soon as it's flipped.
  if (flippedStates.value.length === 0) return false;
  return flippedStates.value.every(state => state === true);
});

// --- The rest of the script is unchanged ---
const resultCards = ref<InstanceType<typeof ResultCard>[]>([]);
const mobileCurrentIndex = ref(0);
const isDesktop = ref(window.innerWidth >= 1280);
const handleResize = () => { isDesktop.value = window.innerWidth >= 1280; };
onMounted(() => { window.addEventListener('resize', handleResize); });
onUnmounted(() => { window.removeEventListener('resize', handleResize); });

const sliderTrackStyle = computed(() => ({ transform: `translateX(-${mobileCurrentIndex.value * 100}%)` }));
const navigateMobile = (direction: 1 | -1) => {
  const newIndex = mobileCurrentIndex.value + direction;
  if (newIndex >= 0 && newIndex < props.results.length) {
    mobileCurrentIndex.value = newIndex;
  }
};

const revealCard = (index: number) => {
  flippedStates.value[index] = true;
};

const revealAll = () => {
  // Sort for dramatic effect (logic is the same)
  const sortedIndices = props.results
    .map((_, index) => index)
    .sort((a, b) => props.results[b].student_rarity - props.results[a].student_rarity);
  
  sortedIndices.forEach((cardIndex, revealIndex) => {
    setTimeout(() => {
      // We now call revealCard to ensure the state is updated correctly
      revealCard(cardIndex);
    }, revealIndex * 100);
  });
};
</script>




<template>
  <Transition name="modal-fade" appear>
    <div class="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4">
      <div class="relative w-full max-w-7xl h-[90vh] bg-slate-800/80 border border-slate-600 rounded-lg shadow-2xl flex flex-col">
        
        <!-- Header -->
        <div class="flex-shrink-0 p-4 border-b border-slate-600 flex justify-between items-center">
          <h2 class="text-2xl font-bold text-cyan-300">Gacha Results</h2>
        </div>

        <div class="flex-grow p-4 overflow-hidden" style="perspective: 1000px;">
          <!-- ====================== CONDITIONAL RENDERING START ====================== -->
          <!-- The `v-if` directive will ONLY render this block on large screens. -->
          <div v-if="isDesktop" class="w-full h-full flex items-center justify-center">
            <div class="grid gap-4 grid-cols-5" :class="{ 'grid-cols-1': results.length === 1 }">
              <ResultCard
                v-for="(student, index) in results"
                :key="student.student_id + '-' + index"
                :student="student"
                :is-flipped="flippedStates[index]"  
                @click="revealCard(index)"
                :class="{ 'xl:col-start-3': results.length === 1 }"
              />
            </div>
          </div>

          <!-- The `v-else` will ONLY render this block on smaller screens. -->
          <div v-else class="relative w-full h-full">
            <div class="slider-track absolute top-0 left-0 h-full w-full flex items-center transition-transform duration-500 ease-in-out" :style="sliderTrackStyle">
              <div v-for="(student, index) in results" :key="student.student_id + '-' + index" class="slider-slide relative w-full h-full flex-shrink-0 flex items-center justify-center">
                <div class="w-64">
                  <ResultCard 
                    :student="student"
                    :is-flipped="flippedStates[index]" 
                    @click="revealCard(index)" 
                  />
                </div>
              </div>
            </div>
            
            <template v-if="results.length > 1">
              <button @click="navigateMobile(-1)" v-show="mobileCurrentIndex > 0" class="mobile-nav-arrow absolute left-2 top-1/2 -translate-y-1/2 bg-black/40 p-4 rounded-full z-40">
                <svg class="h-10 w-10 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path d="M15 19l-7-7 7-7" /></svg>
              </button>
              <button @click="navigateMobile(1)" v-show="mobileCurrentIndex < results.length - 1" class="mobile-nav-arrow absolute right-2 top-1/2 -translate-y-1/2 bg-black/40 p-4 rounded-full z-40">
                <svg class="h-10 w-10 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path d="M9 5l7 7-7 7" /></svg>
              </button>
              <div class="absolute bottom-2 left-1/2 -translate-x-1/2 flex gap-2">
                <div v-for="(_, index) in results" :key="index" class="dot w-2 h-2 rounded-full transition-colors duration-300" :class="index === mobileCurrentIndex ? 'bg-white' : 'bg-white/30'"></div>
              </div>
            </template>
          </div>
        
        </div>

        <div class="flex-shrink-0 p-4 border-t border-slate-700 flex justify-center items-center">
          <Transition name="fade" mode="out-in">
            <button
              v-if="!allCardsRevealed"
              @click="revealAll"
              class="px-6 py-3 bg-slate-600 hover:bg-slate-500 text-white font-semibold rounded-lg transition-colors text-lg"
            >
              Reveal All
            </button>
            <button
              v-else-if="allCardsRevealed"
              @click="emit('close')"
              class="px-6 py-3 bg-cyan-600 hover:bg-cyan-500 text-white font-semibold rounded-lg transition-colors text-lg"
            >
              Close
            </button>
          </Transition>
        </div>

      </div>
    </div>
  </Transition>
</template>

<style scoped>
/* Modal fade styles are unchanged */
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.3s ease;
}
.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}

/* Add a transition for the button swap */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>