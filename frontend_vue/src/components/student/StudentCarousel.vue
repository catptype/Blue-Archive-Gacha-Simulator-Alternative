<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch } from 'vue';

interface Student {
  student_id: number;
  student_name: string;
  portrait_url: string;
}

const props = defineProps<{
  students: Student[];
  isLoading: boolean;
  isSidebarExpanded: boolean;
}>();

const CLONE_COUNT = 3;
const carouselGroup = ref<HTMLElement | null>(null);
const slider = ref<HTMLElement | null>(null); // Add ref for the slider
const currentIndex = ref(CLONE_COUNT);
const isTransitioning = ref(false);
const useTransition = ref(false);

// This will hold the ID of our animation frame loop
let animationFrameId: number | null = null;

const displayStudents = computed(() => {
  if (props.students.length === 0) return [];
  const startClones = props.students.slice(-CLONE_COUNT);
  const endClones = props.students.slice(0, CLONE_COUNT);
  return [...startClones, ...props.students, ...endClones];
});

const sliderStyle = computed(() => {
  if (!carouselGroup.value) return {};
  const containerWidth = carouselGroup.value.offsetWidth;
  const cardWidth = 300;
  const margin = 32;
  const totalCardWidth = cardWidth + margin;
  const offsetToCenter = (containerWidth / 2) - (totalCardWidth / 2);
  const newX = offsetToCenter - (currentIndex.value * totalCardWidth);
  return {
    transform: `translateX(${newX}px)`,
    transition: useTransition.value ? 'transform 600ms ease-in-out' : 'none',
  };
});

const navigate = (direction: 1 | -1) => {
  if (isTransitioning.value) return;
  isTransitioning.value = true;
  useTransition.value = true;
  currentIndex.value += direction;
};

const onTransitionEnd = () => {
  isTransitioning.value = false;
  const totalRealCards = props.students.length;
  if (currentIndex.value >= totalRealCards + CLONE_COUNT) {
    useTransition.value = false; // Disable transition for the jump
    currentIndex.value = CLONE_COUNT;
  }
  if (currentIndex.value < CLONE_COUNT) {
    useTransition.value = false; // Disable transition for the jump
    currentIndex.value = totalRealCards + CLONE_COUNT - 1;
  }
};



const getCardStyle = (index: number) => {
  const isActive = index === currentIndex.value;
  return {
    transform: `scale(${isActive ? 1.15 : 0.9})`,
    opacity: isActive ? '1' : '0.5',
    filter: isActive ? 'none' : 'grayscale(1)',
  };
};

const getCardNameStyle = (index: number) => {
  const isActive = index === currentIndex.value;
  return {
    'opacity-100 translate-x-0': isActive,
    'opacity-0 -translate-x-8': !isActive,
  };
};

// --- ========================================================= ---
// --- NEW & IMPROVED: Sidebar Synchronization Logic             ---
// --- ========================================================= ---

/**
 * Manually calculates and sets the carousel's position.
 * This is our high-performance function for the animation loop.
 */
function recenterInstantly() {
  if (!carouselGroup.value || !slider.value) return;
  
  slider.value.style.transition = 'none';
  const containerWidth = carouselGroup.value.offsetWidth;
  const cardWidth = 300;
  const margin = 32;
  const totalCardWidth = cardWidth + margin;
  const offsetToCenter = (containerWidth / 2) - (totalCardWidth / 2);
  const newX = offsetToCenter - (currentIndex.value * totalCardWidth);

  // Directly manipulate the style for instant updates, bypassing the computed property.
  slider.value.style.transform = `translateX(${newX}px)`;
}

/**
 * Starts a 300ms animation loop that calls recenterInstantly on every frame.
 */
function startRecenterAnimationLoop() {
  if (animationFrameId) cancelAnimationFrame(animationFrameId);
  if (!slider.value) return;

  const animationDuration = 300; // Must match the CSS transition duration of the sidebar
  let startTime: number | null = null;

  // Disable the slider's own CSS transition during our manual animation
  slider.value.style.transition = 'none';

  const loop = (currentTime: number) => {
    if (!startTime) startTime = currentTime;
    const elapsedTime = currentTime - startTime;

    recenterInstantly(); // Update on every frame

    if (elapsedTime < animationDuration) {
      animationFrameId = requestAnimationFrame(loop);
    } else {
      // Animation finished, restore the CSS transition for navigation clicks
      if (slider.value) {
        slider.value.style.transition = 'transform 600ms ease-in-out';
      }
    }
  };

  animationFrameId = requestAnimationFrame(loop);
}

// THE TRIGGER: Watch for sidebar changes and start the animation loop.
watch(() => props.isSidebarExpanded, () => {
  startRecenterAnimationLoop();
});

// Add/remove window resize listener
onMounted(() => window.addEventListener('resize', recenterInstantly));
onUnmounted(() => window.removeEventListener('resize', recenterInstantly));

</script>

<template>
  <div class="h-full relative overflow-hidden">
    <!-- Loading Spinner -->
    <div v-if="isLoading" class="w-full h-full flex items-center justify-center">
      <svg class="animate-spin h-10 w-10 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
    </div>

    <!-- Carousel -->
    <div v-else-if="students.length > 0" class="character-group w-full h-full" ref="carouselGroup">
      <div
        class="slider-container absolute top-0 left-0 w-full h-full flex items-center"
        :style="sliderStyle"
        @transitionend="onTransitionEnd"
        ref="slider"
      >
        <div
          v-for="(student, index) in displayStudents"
          :key="index"
          class="character-card flex-shrink-0 w-[300px] h-[85%] mx-4"
          :class="{ 'transition-all duration-500 ease-in-out': useTransition }"
          :style="getCardStyle(index)"
        >
          <div class="relative w-full h-full group">
            <img :src="student.portrait_url" :alt="student.student_name" class="w-full h-full object-cover rounded-lg">
            <div
              class="character-name absolute bottom-[20px] left-[70px]"
              :class="[getCardNameStyle(index), { 'transition-all duration-500 ease-in-out': useTransition }]"
            >
              <h2 
                class="text-5xl font-black text-white uppercase tracking-widest origin-bottom-left transform -rotate-90"
                style="text-shadow: 2px 2px 10px rgba(0, 0, 0, 0.7);">
                {{ student.student_name }}
              </h2>
            </div>
          </div>
        </div>
      </div>

      <!-- Navigation -->
      <button @click="navigate(-1)" class="nav-arrow nav-left absolute left-6 top-1/2 -translate-y-1/2 bg-black/40 p-3 rounded-full hover:bg-sky-500/50 transition-colors z-40">
        <svg class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" /></svg>
      </button>
      <button @click="navigate(1)" class="nav-arrow nav-right absolute right-6 top-1/2 -translate-y-1/2 bg-black/40 p-3 rounded-full hover:bg-sky-500/50 transition-colors z-40">
        <svg class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" /></svg>
      </button>
    </div>
    
    <!-- No Students Message -->
    <div v-else class="w-full h-full flex items-center justify-center">
      <p class="text-xl text-slate-400">No students found for this school.</p>
    </div>
  </div>
</template>
