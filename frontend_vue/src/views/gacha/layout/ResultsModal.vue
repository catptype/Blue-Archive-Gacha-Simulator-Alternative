<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue';
import LoadSpinner from '@/components/base/LoadSpinner.vue';
import ResultCard from '../components/ResultCard.vue';
import NavButton from '@/components/base/NavButton.vue';
import PolyButton from '@/components/base/PolyButton.vue';
import { type Result } from '@/types/web'

const props = defineProps<{ 
  results: Result[]
  isPulling: boolean
}>();

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
const mobileCurrentIndex = ref(0);
const isDesktop = ref(window.innerWidth >= 1280);

const sliderTrackStyle = computed(() => ({ transform: `translateX(-${mobileCurrentIndex.value * 100}%)` }));

// -- Functions
const navigateMobile = (direction: 1 | -1) => {
  const newIndex = mobileCurrentIndex.value + direction;
  if (newIndex >= 0 && newIndex < props.results.length) {
    mobileCurrentIndex.value = newIndex;
  }
};

const revealCard = (index: number) => { flippedStates.value[index] = true; };

const revealAll = () => {
  // Sort for dramatic effect (logic is the same)
  const sortedIndices = props.results.map((_, index) => index)
  sortedIndices.forEach((cardIndex, revealIndex) => {
    // We now call revealCard to ensure the state is updated correctly
    setTimeout(() => { revealCard(cardIndex); }, revealIndex * 100);
  });
};

const handleResize = () => { isDesktop.value = window.innerWidth >= 1280; };

onMounted(() => { window.addEventListener('resize', handleResize); });
onUnmounted(() => { window.removeEventListener('resize', handleResize); });
</script>

<template>
  <Transition name="modal-fade" appear>
    <div class="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4">
      <div class="relative w-full max-w-7xl h-[90vh] bg-slate-800/80 border border-slate-600 rounded-lg shadow-2xl flex flex-col">
        
        <!-- Header -->
        <div class="shrink-0 p-4 border-b border-slate-600 flex justify-between items-center">
          <h2 class="text-2xl font-bold text-cyan-300">Gacha Results</h2>
        </div>

        <LoadSpinner v-if="props.isPulling" />

        <div v-else class="grow p-4 overflow-hidden" style="perspective: 1000px;">
          <!-- ====================== CONDITIONAL RENDERING START ====================== -->
          <!-- The `v-if` directive will ONLY render this block on large screens. -->
          <div v-if="isDesktop" class="w-full h-full flex items-center justify-center">
            <div class="grid gap-4 grid-cols-5" :class="{ 'grid-cols-1': results.length === 1 }">
              <ResultCard
                v-for="(result, index) in results"
                :key="result.id + '-' + index"
                :result="result"
                :is-flipped="flippedStates[index] ?? false"  
                @click="revealCard(index)"
                :class="{ 'xl:col-start-3': results.length === 1 }"
              />
            </div>
          </div>

          <!-- The `v-else` will ONLY render this block on smaller screens. -->
          <div v-else class="relative w-full h-full">
            <div class="slider-track absolute top-0 left-0 h-full w-full flex items-center transition-transform duration-500 ease-in-out" :style="sliderTrackStyle">
              <div v-for="(result, index) in results" :key="result.id + '-' + index" class="slider-slide relative w-full h-full shrink-0 flex items-center justify-center">
                <div class="w-64">
                  <ResultCard 
                    :result="result"
                    :is-flipped="flippedStates[index] ?? false" 
                    @click="revealCard(index)" 
                  />
                </div>
              </div>
            </div>
            
            <template v-if="results.length > 1">
              <NavButton @click="navigateMobile(-1)" v-show="mobileCurrentIndex > 0" direction="left" />
              <NavButton @click="navigateMobile(1)" v-show="mobileCurrentIndex < results.length - 1" direction="right" />
              <div class="absolute bottom-2 left-1/2 -translate-x-1/2 flex gap-2">
                <div v-for="(_, index) in results" :key="index" class="dot w-2 h-2 rounded-full transition-colors duration-300" :class="index === mobileCurrentIndex ? 'bg-white' : 'bg-white/30'"></div>
              </div>
            </template>
          </div>
        
        </div>

        <div class="shrink-0 p-4 flex justify-center items-center">
          <Transition v-if="!props.isPulling" name="fade" mode="out-in">
            <PolyButton 
              v-if="!allCardsRevealed"
              @click="revealAll"
              color="cyan"
              label="Reveal All"
            />
            <PolyButton 
              v-else-if="allCardsRevealed"
              @click="emit('close')"
              color="cyan"
              label="Close"
            />
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