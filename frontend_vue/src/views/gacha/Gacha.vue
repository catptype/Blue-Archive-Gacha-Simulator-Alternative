<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useToastStore } from '@/stores/toast';
import { type Result, type Banner } from '@/types/web'
import apiClient from '@/services/client';
import PolyButton from '@/components/base/PolyButton.vue';

// Import all necessary components
import BannerCarousel from './layout/BannerCarousel.vue';
import DetailsModal from './layout/DetailsModal.vue';
import ResultsModal from './layout/ResultsModal.vue';
import planaMov from '@/assets/plana-gacha.mov';


const banners = ref<Banner[]>([]);
const activeIndex = ref(0);
const gachaResults = ref<Result[]>([]);
const isDetailsModalVisible = ref(false);
const isResultsModalVisible = ref(false);
const isPulling = ref(false);
const toastStore = useToastStore();

const activeBanner = computed(() => banners.value[activeIndex.value] || null);

onMounted(async () => {
  const { data } = await apiClient.get('/banners/');
  banners.value = data;
});

const handlePull = async (amount: 1 | 10) => {
  // Handling multiple click
  if (!activeBanner.value || isPulling.value) return;
  
  const bannerId = activeBanner.value.id;
  const pullType = amount === 10 ? 'pull_ten' : 'pull_single';
  
  try {
    isResultsModalVisible.value = true;
    isPulling.value = true
    const { data } = await apiClient.post(`/gacha/${bannerId}/${pullType}`);
    gachaResults.value = data.results;
    isPulling.value = false
    
    // Toast notification logic is unchanged
    if (data.unlocked_achievements?.length > 0) {
      data.unlocked_achievements.forEach((ach: any, index: number) => {
        setTimeout(() => toastStore.addToast(ach), index * 500);
      });
    }
  } catch (error) { console.error("Gacha pull failed:", error); }
};
</script>

<template>
  <div class="relative w-full h-screen overflow-hidden text-gray-200">
    <!-- Background -->
    <!-- <div class="absolute inset-0">
      <video autoplay muted loop class="w-full h-full object-cover opacity-80">
        <source :src="planaMov" type="video/mp4">
      </video>
      <div class="absolute inset-0 bg-black/50"></div>
    </div> -->
    
    <!-- Main UI Container -->
    <div class="relative w-full h-full flex flex-col justify-between items-center">
      
      <!-- Banner Carousel -->
      <BannerCarousel
        v-if="banners.length > 0"
        :banners="banners"
        v-model:activeIndex="activeIndex"
      />

      <div class="relative z-30 w-full px-6 md:px-12 pb-8 pt-4 flex flex-col md:flex-row justify-end items-end bg-linear-to-t from-black via-brand-dark/90 to-transparent">
        <div class="flex items-center gap-4 md:gap-6">
            <PolyButton @click="isDetailsModalVisible = true" color="gray" label="Details"/>
            <!-- <PolyButton @click="handlePull(1)" color="cyan" label="Draw 1"/> -->
            <PolyButton @click="handlePull(10)" color="cyan" label="Draw 10"/>
        </div>
    </div>
      
    </div>

    <!-- Modals (These remain unchanged, but are controlled from the new UI) -->
    <DetailsModal
      v-if="isDetailsModalVisible && activeBanner"
      :banner-id="activeBanner.id"
      @close="isDetailsModalVisible = false"
    />
    <ResultsModal
      v-if="isResultsModalVisible"
      :results="gachaResults"
      :is-pulling="isPulling"
      @close="isResultsModalVisible = false"
    />
  </div>
</template>
