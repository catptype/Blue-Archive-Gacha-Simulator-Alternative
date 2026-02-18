<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch } from 'vue';
import LoadSpinner from '@/components/base/LoadSpinner.vue';
import ResultCard from '../components/ResultCard.vue';
import NavButton from '@/components/base/NavButton.vue';
import PolyButton from '@/components/base/PolyButton.vue';
import { type Result } from '@/types/web'
import planaMov from '@/assets/plana-gacha.mov';

const props = defineProps<{ 
  results: Result[]
  isPulling: boolean
}>();

const emit = defineEmits(['close']);

// --- LOGIC FOR VIDEO OVERLAY ---
const videoFinished = ref(false);

// We only show the results when BOTH the API is done AND the video is finished
const showResults = computed(() => {
  return !props.isPulling && videoFinished.value;
});

const handleVideoEnd = () => {
  videoFinished.value = true;
};

// Reset state if the component stays mounted but isPulling changes
watch(() => props.isPulling, (newVal) => {
  if (newVal) {
    videoFinished.value = false;
  }
});


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
  <Transition name="fade" appear>
    <div class="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4">
      <div class="relative w-full max-w-7xl h-[90vh] bg-slate-800/80 border border-slate-600 rounded-lg shadow-2xl flex flex-col overflow-hidden">
        
        <!-- 1. VIDEO OVERLAY LAYER -->
        <Transition name="fade">
          <div v-if="!showResults" class="absolute inset-0 z-20 bg-black flex items-center justify-center">
             <video 
              ref="videoRef"
              autoplay 
              muted 
              playsinline
              class="w-full h-full object-cover"
              @ended="handleVideoEnd"
            >
              <source :src="planaMov" type="video/mp4">
            </video>
            
            <!-- Optional: Show a mini loader if API is still working but video ended -->
            <div v-if="videoFinished && props.isPulling" class="absolute bottom-10">
              <LoadSpinner />
            </div>
          </div>
        </Transition>

        <!-- 2. RESULTS LAYER -->
        <div v-if="showResults" class="flex flex-col h-full w-full">

          <!-- Header -->
          <div class="shrink-0 p-4 border-b border-slate-600 flex justify-between items-center">
            <h2 class="text-2xl font-bold text-cyan-300">Gacha Results</h2>
          </div>

          <div class="grow p-4 overflow-hidden" style="perspective: 1000px;">
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
            <Transition name="fade" mode="out-in">
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
    </div>
  </Transition>
</template>