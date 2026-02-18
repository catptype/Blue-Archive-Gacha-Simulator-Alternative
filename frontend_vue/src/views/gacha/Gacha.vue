<script setup lang="ts">
  import { ref, computed, onMounted } from 'vue';
  import { useToastStore } from '@/stores/toast';
  import { type Result, type Banner } from '@/types/web';
  import apiClient from '@/services/client';
  import PolyButton from '@/components/base/PolyButton.vue';
  import BannerCarousel from './layout/BannerCarousel.vue';
  import DetailsModal from './layout/DetailsModal.vue';
  import ResultsModal from './layout/ResultsModal.vue';

  // ============================================================
  // State
  // ============================================================

  const banners = ref<Banner[]>([]);
  const activeIndex = ref(0);
  const gachaResults = ref<Result[]>([]);
  const isPulling = ref(false);
  const isDetailsModalVisible = ref(false);
  const isResultsModalVisible = ref(false);

  const toastStore = useToastStore();

  // ============================================================
  // Derived
  // ============================================================

  const activeBanner = computed(() => banners.value[activeIndex.value] ?? null);

  // ============================================================
  // Actions
  // ============================================================

  const handlePull = async () => {
    if (!activeBanner.value || isPulling.value) return;

    const bannerId = activeBanner.value.id;

    isResultsModalVisible.value = true;
    isPulling.value = true;

    try {
      const { data } = await apiClient.post(`/gacha/${bannerId}/pull_ten`);

      gachaResults.value = data.results;

      // Stagger achievement toast notifications
      data.unlocked_achievements?.forEach((achievement: any, index: number) => {
        setTimeout(() => toastStore.addToast(achievement), index * 500);
      });
    } catch (error) {
      console.error('Gacha pull failed:', error);
    } finally {
      isPulling.value = false;
    }
  };

  // ============================================================
  // Lifecycle
  // ============================================================

  onMounted(async () => {
    const { data } = await apiClient.get('/banners/');
    banners.value = data;
  });
</script>

<template>
  <div class="relative w-full h-screen overflow-hidden text-gray-200">
    
    <!-- Banner Carousel -->
    <div class="relative w-full h-full flex flex-col justify-between items-center">
      
      <BannerCarousel
        v-if="banners.length > 0"
        :banners="banners"
        v-model:activeIndex="activeIndex"
      />

      <!-- Action Bar -->
      <div class="relative z-30 w-full px-12 pb-8 pt-4 gap-4 flex flex-wrap justify-end items-end bg-linear-to-t from-black via-brand-dark/90 to-transparent">
        <PolyButton @click="isDetailsModalVisible = true" color="gray" label="Details"/>
        <PolyButton @click="handlePull()" color="cyan" label="Draw 10"/>
      </div>
      
    </div>

    <!-- Modals -->
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
