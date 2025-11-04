<script setup lang="ts">
    import { ref, computed, onMounted } from 'vue';
    import axios from 'axios';
    import Background from '../components/Background.vue';
    import HeroPreview from '../components/gacha/HeroPreview.vue';
    import BannerCarousel from '../components/gacha/BannerCarousel.vue';
    import ActionPanel from '../components/gacha/ActionPanel.vue';
    import GachaResults from '../components/gacha/GachaResults.vue';

    interface Banner { banner_id: number; banner_name: string; image_url: string; }
    interface Student { student_id: number; student_rarity: number; /* ... other fields */ }

    const API_BASE_URL = 'http://127.0.0.1:8000/api';

    const banners = ref<Banner[]>([]);
    const activeIndex = ref(0);
    const isDetailsModalVisible = ref(false);
    const isResultsModalVisible = ref(false);
    const gachaResults = ref<Student[]>([]);

    const activeBanner = computed(() => banners.value[activeIndex.value] || null);

    onMounted(async () => {
        const response = await axios.get(`${API_BASE_URL}/banners/`);
        banners.value = response.data;
    });

    const handlePull = async (amount: 1 | 10) => {
        if (!activeBanner.value) return;
        const bannerId = activeBanner.value.banner_id;
        try {
            const response = await axios.post(`${API_BASE_URL}/gacha/${bannerId}/pull/${amount}`);
            gachaResults.value = response.data.results;
            isResultsModalVisible.value = true;
        } catch (error) {
            console.error("Gacha pull failed:", error);
        }
    };
</script>

<template>
  <div class="relative min-h-screen w-full bg-black antialiased text-white overflow-hidden">
    <Background />

    <div class="w-full max-w-screen mx-auto px-4 lg:px-6 pt-20">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6" style="height: calc(100vh - 7rem);">
        
        <HeroPreview :active-banner="activeBanner" />

        <div class="w-full h-full grid grid-rows-5 gap-6">
          <BannerCarousel
            :banners="banners"
            v-model:activeIndex="activeIndex"
          />
          <ActionPanel
            @show-details="isDetailsModalVisible = true"
            @pull="handlePull"
          />
        </div>
      </div>
    </div>
    
    <!-- Modals -->
    <GachaResults
      v-if="isResultsModalVisible"
      :results="gachaResults"
      @close="isResultsModalVisible = false"
    />
    <!-- DetailsModal would be added here similarly -->
  </div>
</template>