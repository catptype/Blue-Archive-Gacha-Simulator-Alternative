<script setup lang="ts">
import { type Banner } from '@/types/web'
import NavButton from '@/components/base/NavButton.vue';

const props = defineProps<{
  banners: Banner[];
  activeIndex: number;
}>();

const emit = defineEmits(['update:activeIndex']);

// --- CORE LOGIC (Direct translation of your AlpineJS function) ---
const getPosition = (index: number) => {
  const total = props.banners.length;
  if (total === 0) return {};
  
  let diff = index - props.activeIndex;

  // Handle looping for seamless wrapping
  if (diff > total / 2) { diff -= total; }
  if (diff < -total / 2) { diff += total; }

  // Define default values
  let scale = 0.8;
  let zIndex = 1;
  let filter = 'brightness(0.3)';
  let opacity = 1;
  let pointerEvents: 'auto' | 'none' = 'auto'; // Default to clickable

  if (diff === 0) { // Center banner
    scale = 1.1;
    zIndex = 10;
    filter = 'brightness(1)';
  } else if (Math.abs(diff) > 1) { // Banners far away
    opacity = 0;
    pointerEvents = 'none';
  }
  
  const translateX = (diff * 100) - 50;

  return {
    transform: `translateX(${translateX}%) translateY(${diff === 0 ? '-70px' : '0'}) scale(${scale})`,
    zIndex: zIndex,
    filter: filter,
    opacity: opacity,
    pointerEvents: pointerEvents,
  };
};

const goNext = () => {
  const total = props.banners.length;
  if (total > 0) emit('update:activeIndex', (props.activeIndex + 1) % total);
};

const goPrev = () => {
  const total = props.banners.length;
  if (total > 0) emit('update:activeIndex', (props.activeIndex - 1 + total) % total);
};
</script>

<template>
  <div class="relative w-full max-w-[80%] h-36 mx-auto">
    <!-- Navigation Buttons -->
    <NavButton 
      direction="left" 
      @click="goPrev" 
    />
    <NavButton 
      direction="right" 
      @click="goNext" 
    />

    <!-- Banner Images -->
    <img
      v-for="(banner, index) in banners"
      :key="banner.id"
      :src="banner.image_url"
      :alt="banner.name"
      :style="getPosition(index)"
      @click="emit('update:activeIndex', index)"
      class="banner-image object-cover cursor-pointer"
    />
  </div>
</template>



<style scoped>
/* Scoped styles from your mockup */
.banner-image {
  position: absolute;
  top: 0;
  left: 50%;
  width: 40%;
  max-width: 400px;
  min-width: 300px;
  transition: all 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94);

  -webkit-mask-image: linear-gradient(to bottom, 
    transparent 1%, 
    black 10%, 
    black 100%
  );
  mask-image: linear-gradient(to bottom, 
    transparent 1%, 
    black 10%, 
    black 100%
  );
}
</style>