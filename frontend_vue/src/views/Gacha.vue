<script setup lang="ts">
    import { ref, computed, onMounted } from 'vue';
    import { useToastStore } from '@/stores/toast';
    import Background from '@/components/Background.vue';
    import HeroPreview from '@/components/gacha/HeroPreview.vue';
    import BannerCarousel from '@/components/gacha/BannerCarousel.vue';
    import ActionPanel from '@/components/gacha/ActionPanel.vue';
    import GachaResults from '@/components/gacha/GachaResults.vue';
    import DetailsModal from '@/components/gacha/DetailsModal.vue';
    import apiClient from '@/services/client'; 

    interface Banner { banner_id: number; banner_name: string; image_url: string; }
    interface Student { student_id: number; student_rarity: number; }

    const banners = ref<Banner[]>([]);
    const activeIndex = ref(0);
    const isDetailsModalVisible = ref(false);
    const isResultsModalVisible = ref(false);
    const gachaResults = ref<Student[]>([]);

    const activeBanner = computed(() => banners.value[activeIndex.value] || null);

    onMounted(async () => {
        const response = await apiClient.get('/banners/'); 
        banners.value = response.data;
    });

    const toastStore = useToastStore();

    const handlePull = async (amount: 1 | 10) => {
    if (!activeBanner.value) return;
    
    const bannerId = activeBanner.value.banner_id;
    
    const pullType = amount === 10 ? 'pull_ten' : 'pull_single';

    try {
      const response = await apiClient.post(`/gacha/${bannerId}/${pullType}`); 
      gachaResults.value = response.data.results;
      isResultsModalVisible.value = true;

      const unlockedAchievements = response.data.unlocked_achievements;
      if (unlockedAchievements && unlockedAchievements.length > 0) {
        // Loop through the unlocked achievements and show a toast for each one.
        unlockedAchievements.forEach((ach: any, index: number) => {
          // Stagger the notifications so they appear one after another.
          setTimeout(() => {
            toastStore.addToast(ach);
          }, index * 500); // 500ms delay between each toast
        });
      }
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
    
    <DetailsModal
      v-if="isDetailsModalVisible && activeBanner"
      :banner-id="activeBanner.banner_id"
      @close="isDetailsModalVisible = false"
    />
  </div>
</template>