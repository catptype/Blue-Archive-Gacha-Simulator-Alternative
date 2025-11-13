<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useToastStore } from '@/stores/toast';
import apiClient from '@/services/client';

// Import all necessary components
import SlidingBannerCarousel from '@/components/gacha/SlidingBannerCarousel.vue';
import DetailsModal from '@/components/gacha/DetailsModal.vue';
import GachaResults from '@/components/gacha/GachaResults.vue';
import planaMov from '@/assets/plana-gacha.mov';

interface Banner { banner_id: number; banner_name: string; image_url: string; }
interface Student { /* ... */ }

const banners = ref<Banner[]>([]);
const activeIndex = ref(0);
const gachaResults = ref<Student[]>([]);
const isDetailsModalVisible = ref(false);
const isResultsModalVisible = ref(false);
const toastStore = useToastStore();

const activeBanner = computed(() => banners.value[activeIndex.value] || null);

onMounted(async () => {
  const { data } = await apiClient.get('/banners/');
  banners.value = data;
});

const handlePull = async (amount: 1 | 10) => {
  if (!activeBanner.value) return;
  const bannerId = activeBanner.value.banner_id;
  const pullType = amount === 10 ? 'pull_ten' : 'pull_single';
  try {
    const { data } = await apiClient.post(`/gacha/${bannerId}/${pullType}`);
    gachaResults.value = data.results;
    isResultsModalVisible.value = true;
    
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
    <div class="absolute inset-0 z-0">
      <video autoplay muted loop class="hero-bg-video">
        <source :src="planaMov" type="video/mp4">
      </video>
      <div class="absolute inset-0 bg-black/50"></div>
    </div>
    
    <!-- Main UI Container -->
    <div class="relative w-full h-full flex flex-col justify-end items-center">
      <!-- Banner Carousel -->
      <div class="w-full max-w-[80%] h-36 -mb-12">
        <SlidingBannerCarousel
          v-if="banners.length > 0"
          :banners="banners"
          v-model:activeIndex="activeIndex"
        />
      </div>
      
      <!-- Central Core -->
      <div class="h-1/4 w-full flex justify-center">
        <div class="central-core h-full grid grid-cols-1 md:grid-cols-2 p-10 md:p-20 gap-4">
          <button @click="isDetailsModalVisible = true" class="pull-btn md:col-span-2 w-40 h-14 text-lg text-blue-300 rounded-lg justify-self-center">
            DETAILS
          </button>
          <button @click="handlePull(1)" class="pull-btn w-40 h-14 text-lg text-blue-300 rounded-lg md:justify-self-end justify-self-center">
            PULL x1
          </button>
          <button @click="handlePull(10)" class="pull-btn w-40 h-14 text-lg text-blue-300 rounded-lg md:justify-self-start justify-self-center">
            PULL x10
          </button>
        </div>
      </div>
      
    </div>

    <!-- Modals (These remain unchanged, but are controlled from the new UI) -->
    <DetailsModal
      v-if="isDetailsModalVisible && activeBanner"
      :banner-id="activeBanner.banner_id"
      @close="isDetailsModalVisible = false"
    />
    <GachaResults
      v-if="isResultsModalVisible"
      :results="gachaResults"
      @close="isResultsModalVisible = false"
    />
  </div>
</template>

<style scoped>
/* All scoped styles from your mockup */
.hero-bg-video {
  position: absolute; top: 50%; left: 50%;
  width: 100%; height: 100%; object-fit: cover;
  transform: translate(-50%, -50%); z-index: -1; opacity: 0.7;
}
.central-core {
  background: radial-gradient(circle, rgba(29, 78, 216, 0.4) 0%, rgba(10, 15, 30, 0.8) 60%);
  border-top: 2px solid rgba(59, 130, 246, 0.5);
  width: 150%;
  border-radius: 50% 50% 0 0 / 100% 100% 0 0;
  box-shadow: 0 0 40px rgba(59, 130, 246, 0.3);
}
.pull-btn {
  background-color: rgba(10, 20, 40, 0.8);
  border: 2px solid #3b82f6;
  box-shadow: 0 0 15px rgba(59, 130, 246, 0.5);
  transition: all 0.3s ease;
}
.pull-btn:hover {
  background-color: #3b82f6;
  color: white;
}
</style>