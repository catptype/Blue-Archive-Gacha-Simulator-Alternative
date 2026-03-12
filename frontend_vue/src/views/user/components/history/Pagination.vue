<script setup lang="ts">
  import { ref, watch } from 'vue';
  import PolyButton from '@/components/base/PolyButton.vue';

  const props = defineProps<{ 
    currentPage: number; 
    totalPages: number; 
  }>();

  const emit = defineEmits(['change-page']);

  const pageInput = ref(props.currentPage);

  watch(() => props.currentPage, (newPage) => {
    pageInput.value = newPage;
  });

  const changePage = (page: number) => {
    if (page >= 1 && page <= props.totalPages) {
      emit('change-page', page);
    }
  };

  const jumpToPage = () => {
    const page = Math.max(1, Math.min(props.totalPages, pageInput.value));
    changePage(page);
  };
</script>

<template>
  <div
    v-if="totalPages > 1"
    class="flex flex-col sm:flex-row items-center justify-between gap-4 text-sm text-slate-300"
  >
    <!-- First & Previous -->
    <div class="flex items-center gap-2">
      <PolyButton @click="changePage(1)" color="cyan" label="&laquo; First" width="w-28" height="h-10" textsize="text-base"/>
      <PolyButton @click="changePage(currentPage - 1)" color="cyan" label="Previous" width="w-28" height="h-10" textsize="text-base"/>
    </div>

    <!-- Page Info & Go -->
    <form @submit.prevent="jumpToPage" class="flex items-center gap-2">
      <span>Page</span>
      <input type="number" v-model.number="pageInput" class="w-16 h-8 text-center bg-slate-900 border border-slate-600 rounded-md">
      <span>of {{ totalPages }}</span>
      <PolyButton color="cyan" label="Go" width="w-20" height="h-10" textsize="text-base"/>
    </form>

    <!-- Next & Last -->
    <div class="flex items-center gap-2">
      <PolyButton @click="changePage(currentPage + 1)" color="cyan" label="Next" width="w-28" height="h-10" textsize="text-base"/>
      <PolyButton @click="changePage(totalPages)" color="cyan" label="Last &raquo;" width="w-28" height="h-10" textsize="text-base"/>
    </div>
  </div>
</template>
