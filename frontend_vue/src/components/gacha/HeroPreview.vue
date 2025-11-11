<script setup lang="ts">
    import { ref, watch } from 'vue';
    import planaMov from '@/assets/plana-gacha.mov';
    
    interface Banner { banner_name: string; }
    
    const props = defineProps<{ activeBanner: Banner | null }>();
    const textVisible = ref(false);

    watch(() => props.activeBanner, () => {
        textVisible.value = false;
        setTimeout(() => { textVisible.value = true; }, 100);
    }, { immediate: true });
</script>

<template>
  <div class="relative w-full h-full bg-slate-900 border border-slate-700 rounded-lg shadow-2xl overflow-hidden">
    <video autoplay muted loop class="absolute inset-0 w-full h-full object-cover z-0">
      <source :src="planaMov" type="video/mp4">
    </video>
    <div class="absolute inset-0 bg-gradient-to-t from-black/60 via-black/20 to-transparent z-10"></div>
    <div
      v-if="activeBanner"
      class="absolute bottom-0 left-0 p-6 z-20 text-5xl font-black text-white uppercase tracking-widest transition-all duration-500"
      :class="textVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'"
      style="text-shadow: 2px 2px 10px rgba(0,0,0,0.7);"
    >
      {{ activeBanner.banner_name }}
    </div>
  </div>
</template>