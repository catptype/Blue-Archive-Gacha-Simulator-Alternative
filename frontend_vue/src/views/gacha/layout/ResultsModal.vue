<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch } from 'vue';
import planaMov from '@/assets/plana-gacha.mov';
import LoadSpinner from '@/components/base/LoadSpinner.vue';
import ResultCard from '../components/ResultCard.vue';
import NavButton from '@/components/base/NavButton.vue';
import PolyButton from '@/components/base/PolyButton.vue';
import { type Result } from '@/types/web';

// ============================================================
// Props & Emits
// ============================================================

const props = defineProps<{
  results: Result[];
  isPulling: boolean;
}>();

const emit = defineEmits<{
  close: [];
}>();

// ============================================================
// Video Overlay State
//
// The results layer is hidden until BOTH conditions are met:
//   1. The API has finished pulling (isPulling === false)
//   2. The intro video has finished playing
// ============================================================

const videoFinished = ref(false);

const showResults = computed(() => !props.isPulling && videoFinished.value);

const handleVideoEnd = () => {
  videoFinished.value = true;
};

// Reset video state whenever a new pull starts
watch(
  () => props.isPulling,
  (isPulling) => { if (isPulling) videoFinished.value = false; }
);

// ============================================================
// Card Flip State
// ============================================================

const flippedStates = ref<boolean[]>(props.results.map(() => false));

const allCardsRevealed = computed(
  () => flippedStates.value.length > 0 && flippedStates.value.every(Boolean)
);

const revealCard = (index: number) => {
  flippedStates.value[index] = true;
};

const revealAll = () => {
  // Stagger reveals for a dramatic effect
  props.results.forEach((_, index) => {
    setTimeout(() => revealCard(index), index * 100);
  });
};

// ============================================================
// Mobile Slider
// ============================================================

const DESKTOP_BREAKPOINT = 1280; // px (matches Tailwind's `xl`)

const mobileCurrentIndex = ref(0);
const isDesktop = ref(window.innerWidth >= DESKTOP_BREAKPOINT);

const sliderTrackStyle = computed(() => ({
  transform: `translateX(-${mobileCurrentIndex.value * 100}%)`,
}));

const navigateMobile = (direction: 1 | -1) => {
  const next = mobileCurrentIndex.value + direction;
  const isInBounds = next >= 0 && next < props.results.length;
  if (isInBounds) mobileCurrentIndex.value = next;
};

const handleResize = () => {
  isDesktop.value = window.innerWidth >= DESKTOP_BREAKPOINT;
};

onMounted(() => window.addEventListener('resize', handleResize));
onUnmounted(() => window.removeEventListener('resize', handleResize));
</script>

<template>
  <Transition name="fade" appear>
    <div class="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4">
      <div class="relative w-full max-w-7xl h-[90vh] bg-slate-800/80 border border-slate-600 rounded-lg shadow-2xl flex flex-col overflow-hidden">
        
        <!-- ===================== VIDEO OVERLAY =====================
             Shown while results aren't ready yet. Fades out once
             both the API call and video playback are complete.
        ============================================================ -->
        <Transition name="fade">
          <div v-if="!showResults" class="absolute inset-0 z-20 bg-black flex items-center justify-center">
             <video 
              autoplay 
              muted 
              playsinline
              class="w-full h-full object-cover"
              @ended="handleVideoEnd"
            >
              <source :src="planaMov" type="video/mp4">
            </video>
            
            <!-- Spinner for when video ends before API responds -->
            <div v-if="videoFinished && props.isPulling" class="absolute bottom-10">
              <LoadSpinner />
            </div>
          </div>
        </Transition>

        <!-- ===================== RESULTS LAYER =====================
             Rendered only after video + API are both done.
        ============================================================ -->
        <div v-if="showResults" class="flex flex-col h-full w-full">

          <!-- Header -->
          <div class="shrink-0 p-4 border-b border-slate-600 flex justify-between items-center">
            <h2 class="text-2xl font-bold text-cyan-300">Gacha Results</h2>
          </div>

          <!-- Card Display Area -->
          <div class="grow p-4 overflow-hidden perspective-[1000px]">
            
            <!-- Desktop: Static grid -->
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

            <!-- Mobile: Swipeable slider -->
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
              
              <!-- Slider controls (only shown for multiple results) -->
              <template v-if="results.length > 1">
                <NavButton @click="navigateMobile(-1)" v-show="mobileCurrentIndex > 0" direction="left" />
                <NavButton @click="navigateMobile(1)" v-show="mobileCurrentIndex < results.length - 1" direction="right" />
                
                <!-- Pagination dots -->
                <div class="absolute bottom-2 left-1/2 -translate-x-1/2 flex gap-2">
                  <div v-for="(_, index) in results" :key="index" class="dot w-2 h-2 rounded-full transition-colors duration-300" :class="index === mobileCurrentIndex ? 'bg-white' : 'bg-white/30'"></div>
                </div>
              </template>
            </div>
          
          </div>

          <!-- Reveal Actions -->
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