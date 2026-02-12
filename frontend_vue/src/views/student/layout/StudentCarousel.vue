<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch } from 'vue';
import { type Student } from '@/types/web'
import LoadSpinner from '@/components/base/LoadSpinner.vue';
import CarouselCard from '../components/CarouselCard.vue';
import NavButton from '@/components/base/NavButton.vue';

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
    <LoadSpinner v-if="isLoading" />

    <!-- Carousel -->
    <div v-else-if="students.length > 0" class="character-group w-full h-full" ref="carouselGroup">
      <div
        class="slider-container absolute top-0 left-0 w-full h-full flex items-center"
        :style="sliderStyle"
        @transitionend="onTransitionEnd"
        ref="slider"
      >
        <CarouselCard
          v-for="(student, index) in displayStudents"
          :key="index"
          :student="student"
          :is-active="index === currentIndex"
          :use-transition="useTransition"
        />

      </div>

      <!-- Navigation -->
      <NavButton 
        direction="left" 
        @click="navigate(-1)" 
      />
      
      <NavButton 
        direction="right" 
        @click="navigate(1)" 
      />

    </div>
    
    <!-- No Students Message -->
    <div v-else class="w-full h-full flex items-center justify-center">
      <p class="text-xl text-slate-400">No students found for this school.</p>
    </div>
  </div>
</template>
