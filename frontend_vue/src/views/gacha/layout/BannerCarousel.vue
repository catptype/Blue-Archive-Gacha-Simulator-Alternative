<script setup lang="ts">
import { type CSSProperties } from 'vue'
import { type Banner } from '@/types/web'
import NavButton from '@/components/base/NavButton.vue';

const props = defineProps<{
  banners: Banner[];
  activeIndex: number;
}>();

const emit = defineEmits(['update:activeIndex']);

// --- REVISED LOGIC (3D Perspective Logic from Mock) ---
const getCardStyle = (index: number): CSSProperties => {
  const total = props.banners.length;
  if (total === 0) return {};
  
  let diff = index - props.activeIndex;

  // Handle looping for seamless wrapping
  if (diff > total / 2) { diff -= total; }
  if (diff < -total / 2) { diff += total; }

  const isActive = diff === 0;
  
  // Calculate 3D transforms
  let xOffset = diff * 65; 
  if (Math.abs(diff) > 2) xOffset = diff * 40; 
  
  const zOffset = isActive ? 0 : -400 - (Math.abs(diff) * 100); 
  const rotateY = isActive ? 0 : (diff > 0 ? -25 : 25); 
  
  return {
    transform: `translateX(${xOffset}%) translateZ(${zOffset}px) rotateY(${rotateY}deg) scale(${isActive ? 1 : 0.85})`,
    zIndex: isActive ? 50 : (50 - Math.abs(diff)),
    opacity: Math.abs(diff) >= 2 ? 0 : (isActive ? 1 : 0.4),
    filter: `blur(${isActive ? 0 : 4}px) brightness(${isActive ? 1 : 0.6})`,
    pointerEvents: (isActive || Math.abs(diff) < 2) ? 'auto' : 'none',
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
  
  <!-- Wrapper with perspective -->
  <div class="relative w-full h-full perspective-distant transform-3d flex items-center justify-center overflow-hidden">
    
    <!-- Navigation Buttons (Kept exactly the same as requested) -->
    <NavButton 
      direction="left" 
      @click="goPrev" 
      class="z-100"
    />
    <NavButton 
      direction="right" 
      @click="goNext"
      class="z-100"
    />

    <!-- 2. Text Info (Ported from Mockup) -->
    <div class="absolute left-6 md:left-24 top-1/4 z-60 pointer-events-none">
      <transition name="fade" mode="out-in">
        <div :key="activeIndex" class="w-full">
          <div class="flex items-center gap-2 mb-2">
            <div class="h-px w-8 bg-[#4DF0FF]"></div>
            <span class="text-[#4DF0FF] font-bold tracking-widest text-xs uppercase">Banner</span>
          </div>
          <h1 class="text-5xl font-black italic uppercase leading-none mb-4 text-white drop-shadow-lg">
            {{ banners[activeIndex]?.name }}
          </h1>
        </div>
      </transition>
    </div>

    <!-- REVISED CARDS -->
    <div 
      v-for="(banner, index) in banners"
      :key="banner.id"
      class="landscape-card absolute w-[700px] h-[350px] max-w-[80vw] max-h-[40vw] transition-all duration-500 cursor-pointer"
      :class="{ 'active-card': activeIndex === index }"
      :style="getCardStyle(index)"
      @click="emit('update:activeIndex', index)"
    >
      <!-- Main Banner Image -->
      <img 
        :src="banner.image_url" 
        :alt="banner.name"
        class="w-full h-full object-contain transition-transform duration-700"
        :class="activeIndex === index ? 'scale-100' : 'scale-110 grayscale-30'"
      >

      <!-- Shine Animation Layer -->
      <div class="shine-bar"></div>

    </div>
  </div>
</template>

<style scoped>

.landscape-card {
  -webkit-mask-image: linear-gradient(to bottom, 
    transparent 1%, 
    black 20%, 
    black 100%
  );
  mask-image: linear-gradient(to bottom, 
    transparent 1%, 
    black 20%, 
    black 100%
  );
}

.shine-bar {
  position: absolute;
  top: 0; 
  left: -100%;
  width: 50%; 
  height: 100%;
  background: linear-gradient(
    to right, 
    transparent, 
    rgba(255, 255, 255, 0.2), 
    transparent
  );
  transform: skewX(-25deg);
  pointer-events: none;
}

.active-card .shine-bar {
  animation: shine 3s infinite;
}

@keyframes shine {
  0% { left: -100%; }
  20% { left: 200%; }
  100% { left: 200%; }
}
</style>