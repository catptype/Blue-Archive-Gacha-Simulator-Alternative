<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useToastStore } from '@/stores/toast';
import { type Student, type Banner } from '@/types/web'
import apiClient from '@/services/client';
import PolyButton from '@/components/base/PolyButton.vue';

// Import all necessary components
import BannerCarousel from './layout/BannerCarousel.vue';
import DetailsModal from './layout/DetailsModal.vue';
import ResultsModal from './layout/ResultsModal.vue';
import planaMov from '@/assets/plana-gacha.mov';


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
  const bannerId = activeBanner.value.id;
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
    <div class="absolute inset-0">
      <video autoplay muted loop class="w-full h-full object-cover opacity-80">
        <source :src="planaMov" type="video/mp4">
      </video>
      <div class="absolute inset-0 bg-black/50"></div>
    </div>
    
    <!-- Main UI Container -->
    <div class="relative w-full h-full flex flex-col justify-end items-center">
      
      <Transition name="fade" mode="out-in">
        <div 
          :key="activeBanner ? activeBanner.name : 'loading'"
          v-if="activeBanner"
          class="text-center mb-20 opacity-80"
        >
          <h2 class="text-3xl font-bold tracking-wider text-white" style="text-shadow: 2px 2px 8px rgba(0,0,0,0.7);">
            {{ activeBanner.name }}
          </h2>
        </div>
      </Transition>

      <!-- Banner Carousel -->
      <div class="w-full max-w-[80%] h-36 -mb-12">
        <BannerCarousel
          v-if="banners.length > 0"
          :banners="banners"
          v-model:activeIndex="activeIndex"
        />
      </div>

      <!-- Central Core -->
      <div class="h-auto w-full flex justify-center">
        <div class="w-full border border-slate-700 bg-slate-900/50 backdrop-blur-lg rounded-tl-full rounded-tr-full h-full grid grid-cols-1 md:grid-cols-2 p-10 md:p-20 gap-4">
          <button @click="isDetailsModalVisible = true" class="md:col-span-2 w-40 h-14 bg-cyan-600 hover:bg-cyan-500 text-lg text-white rounded-lg justify-self-center">
            DETAILS
          </button>
          <button @click="handlePull(1)" class="w-40 h-14 bg-cyan-600 hover:bg-cyan-500 text-lg text-white rounded-lg md:justify-self-end justify-self-center">
            PULL x1
          </button>
          <button @click="handlePull(10)" class="w-40 h-14 bg-cyan-600 hover:bg-cyan-500 text-lg text-white rounded-lg md:justify-self-start justify-self-center">
            PULL x10
          </button>
        </div>
      </div>


      <div class="relative z-30 w-full px-6 md:px-12 pb-8 pt-4 flex flex-col md:flex-row justify-between items-end bg-gradient-to-t from-black via-brand-dark/90 to-transparent">
        
        <div class="mb-4 md:mb-0">
            <div class="text-xs text-gray-500 tracking-[0.2em] mb-1">GUARANTEE COUNT</div>
            <div class="flex items-end gap-2">
                <span class="text-4xl font-bold text-white">45</span>
                <span class="text-xl text-gray-600 mb-1">/ 90</span>
            </div>
            <div class="w-48 h-1.5 bg-gray-800 mt-2 rounded-full overflow-hidden">
                <div class="h-full bg-brand-cyan shadow-[0_0_10px_#4DF0FF]" style="width: 50%"></div>
            </div>
        </div>

        <div class="flex items-center gap-4 md:gap-6">
            <PolyButton @click="handlePull(1)" color="cyan" label="Draw 1"/>
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
      @close="isResultsModalVisible = false"
    />
  </div>
</template>
