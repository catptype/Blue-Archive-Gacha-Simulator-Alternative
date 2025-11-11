<script setup lang="ts">
    import { ref, onMounted, computed } from 'vue';
    import apiClient from '@/services/client';
    import StudentPoolSection from './StudentPoolSection.vue';

    const props = defineProps<{ bannerId: number }>();
    const emit = defineEmits(['close']);

    const bannerData = ref<any>(null);
    const isLoading = ref(true);
    const error = ref('');
    const viewMode = ref<'grid' | 'list'>('grid');

    onMounted(async () => {
        try {
            const response = await apiClient.get(`/banners/${props.bannerId}/details/`);
            bannerData.value = response.data;
        } catch (err) {
            error.value = "Failed to load banner details.";
            console.error(err);
        } finally {
            isLoading.value = false;
        }
    });

    // --- Computed properties to calculate individual rates ---
    const pickupRatePerStudent = computed(() => {
        if (!bannerData.value || bannerData.value.pickup_r3_students.length === 0) return 0;
        return Number(bannerData.value.preset.preset_pickup_rate) / bannerData.value.pickup_r3_students.length;
    });
    const nonPickupR3RatePerStudent = computed(() => {
        if (!bannerData.value || bannerData.value.nonpickup_r3_students.length === 0) return 0;
            const nonPickupRate = Number(bannerData.value.preset.preset_r3_rate) - Number(bannerData.value.preset.preset_pickup_rate);
        return nonPickupRate / bannerData.value.nonpickup_r3_students.length;
    });
    const r2RatePerStudent = computed(() => {
        if (!bannerData.value || bannerData.value.r2_students.length === 0) return 0;
        return Number(bannerData.value.preset.preset_r2_rate) / bannerData.value.r2_students.length;
    });
    const r1RatePerStudent = computed(() => {
        if (!bannerData.value || bannerData.value.r1_students.length === 0) return 0;
        return Number(bannerData.value.preset.preset_r1_rate) / bannerData.value.r1_students.length;
    });
</script>

<template>
  <Transition name="modal-fade">
    <div class="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4" @click.self="emit('close')">
      <div class="relative w-full max-w-4xl h-[80vh] bg-slate-800 border border-slate-600 rounded-lg shadow-2xl flex flex-col">
        <button @click="emit('close')" class="absolute top-2 right-2 text-slate-400 hover:text-white z-10 text-4xl leading-none">&times;</button>

        <!-- Loading State -->
        <div v-if="isLoading" class="w-full h-full flex items-center justify-center">
          <svg class="animate-spin h-8 w-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path></svg>
        </div>

        <!-- Error State -->
        <div v-else-if="error" class="w-full h-full flex items-center justify-center">
          <p class="text-red-400">{{ error }}</p>
        </div>
        
        <!-- Content -->
        <template v-else-if="bannerData">
          <!-- Header -->
          <div class="flex-shrink-0 p-4 border-b border-slate-600">
            <h2 class="text-2xl font-bold text-cyan-300">Banner Details: {{ bannerData.banner_name }}</h2>
          </div>

          <!-- View Switcher -->
          <div class="flex-shrink-0 p-4 flex justify-between items-center border-b border-slate-700">
            <div class="flex items-center border border-slate-600 rounded-lg">
              <button @click="viewMode = 'grid'" :class="viewMode === 'grid' ? 'bg-slate-700 text-white' : 'bg-transparent text-slate-400'" class="p-2" title="Grid View">
                <svg class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor"><path d="M5 3a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2V5a2 2 0 00-2-2H5zM5 11a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2v-2a2 2 0 00-2-2H5zM11 5a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V5zM11 13a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" /></svg>
              </button>
              <button @click="viewMode = 'list'" :class="viewMode === 'list' ? 'bg-slate-700 text-white' : 'bg-transparent text-slate-400'" class="p-2" title="List View">
                <svg class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor"><path d="M3 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" /></svg>
              </button>
            </div>
            <p class="text-center text-xs text-slate-400 italic">Hover over a student's portrait to see their individual rate.</p>
          </div>

          <!-- Scrollable Content -->
          <div class="flex-grow p-4 overflow-y-auto">
            <StudentPoolSection v-if="bannerData.pickup_r3_students.length > 0" title="Pickup Students" :totalRate="Number(bannerData.preset.preset_pickup_rate)" :students="bannerData.pickup_r3_students" :viewMode="viewMode" :individualRate="pickupRatePerStudent" :is-pickup="true" />
            <StudentPoolSection v-if="bannerData.nonpickup_r3_students.length > 0" title="Available ★★★ Pool" :totalRate="Number(bannerData.preset.preset_r3_rate) - Number(bannerData.preset.preset_pickup_rate)" :students="bannerData.nonpickup_r3_students" :viewMode="viewMode" :individualRate="nonPickupR3RatePerStudent" :is-pickup="false" />
            <StudentPoolSection v-if="bannerData.r2_students.length > 0" title="Available ★★ Pool" :totalRate="Number(bannerData.preset.preset_r2_rate)" :students="bannerData.r2_students" :viewMode="viewMode" :individualRate="r2RatePerStudent" :is-pickup="false" />
            <StudentPoolSection v-if="bannerData.r1_students.length > 0" title="Available ★ Pool" :totalRate="Number(bannerData.preset.preset_r1_rate)" :students="bannerData.r1_students" :viewMode="viewMode" :individualRate="r1RatePerStudent" :is-pickup="false" />
          </div>
        </template>
      </div>
    </div>
  </Transition>
</template>