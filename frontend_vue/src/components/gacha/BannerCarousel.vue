<script setup lang="ts">
    import { ref, onMounted, onUnmounted } from 'vue';
    interface Banner { banner_id: number; image_url: string; }

    const props = defineProps<{ banners: Banner[]; activeIndex: number; }>();
    const emit = defineEmits(['update:activeIndex']);

    const isDesktop = ref(window.innerWidth >= 1024);
    const onResize = () => { isDesktop.value = window.innerWidth >= 1024; };
    onMounted(() => window.addEventListener('resize', onResize));
    onUnmounted(() => window.removeEventListener('resize', onResize));

    const navigate = (direction: 1 | -1) => {
        const total = props.banners.length;
        const newIndex = (props.activeIndex + direction + total) % total;
        emit('update:activeIndex', newIndex);
    };

    function getCardStyle(index: number) {
        const totalCards = props.banners.length;
        const offset = index - props.activeIndex;
        const loopedOffset = (offset + totalCards + Math.floor(totalCards / 2)) % totalCards - Math.floor(totalCards / 2);
        const gap = isDesktop.value ? 65 : 30;
        const scale = loopedOffset === 0 ? 1.0 : (isDesktop.value ? 0.7 : 0.6);
        return {
            transform: `translateY(-50%) translateX(calc(-50% + ${loopedOffset * gap}%)) scale(${scale})`,
            opacity: Math.abs(loopedOffset) > 1 ? 0 : 1,
            zIndex: totalCards - Math.abs(loopedOffset),
        };
    }
</script>

<template>
  <div class="relative row-span-2 w-full h-full overflow-hidden">
    <div
      v-for="(banner, index) in banners"
      :key="banner.banner_id"
      class="banner-card absolute top-1/2 left-1/2 h-full w-full transition-all duration-500 ease-in-out rounded-lg overflow-hidden cursor-pointer"
      :style="getCardStyle(index)"
      @click="emit('update:activeIndex', index)"
    >
      <div class="card-image-wrapper w-full h-full" :class="{ 'grayscale': index !== activeIndex }">
        <img :src="banner.image_url" class="w-full h-full object-contain">
      </div>
    </div>
    
    <!-- Navigation Arrows -->
    <button @click="navigate(-1)" class="nav-arrow nav-left absolute left-6 bottom-6 bg-black/40 p-3 rounded-full hover:bg-sky-500/50 transition-colors z-40">
      <svg class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path d="M15 19l-7-7 7-7" /></svg>
    </button>
    <button @click="navigate(1)" class="nav-arrow nav-right absolute right-6 bottom-6 bg-black/40 p-3 rounded-full hover:bg-sky-500/50 transition-colors z-40">
      <svg class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path d="M9 5l7 7-7 7" /></svg>
    </button>
  </div>
</template>