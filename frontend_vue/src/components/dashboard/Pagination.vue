<script setup lang="ts">
    import { ref, watch } from 'vue';

    const props = defineProps<{ currentPage: number; totalPages: number; }>();
    const emit = defineEmits(['change-page']);

    const pageInput = ref(props.currentPage);

    watch(() => props.currentPage, (newPage) => {
        pageInput.value = newPage;
    });

    // --- THIS IS THE NEW PART ---
    // A function that returns the correct classes based on the disabled state.
    const buttonClass = (isDisabled: boolean) => {
        const baseClasses = 'px-3 py-1 rounded-md transition-colors';
        if (isDisabled) {
            return `${baseClasses} bg-slate-800 text-slate-500 pointer-events-none`;
        }
        return `${baseClasses} bg-slate-700 hover:bg-slate-600`;
    };
    // --- END OF NEW PART ---

    const changePage = (page: number) => {
        if (page >= 1 && page <= props.totalPages) {
            emit('change-page', page);
        }
    };

    const jumpToPage = () => {
        // Add a quick validation for the input
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
      <button @click="changePage(1)" :disabled="currentPage === 1" :class="buttonClass(currentPage === 1)">
        &laquo; First
      </button>
      <button @click="changePage(currentPage - 1)" :disabled="currentPage === 1" :class="buttonClass(currentPage === 1)">
        Previous
      </button>
    </div>

    <!-- Page Info & Go -->
    <form @submit.prevent="jumpToPage" class="flex items-center gap-2">
      <span>Page</span>
      <input type="number" v-model.number="pageInput" class="w-16 h-8 text-center bg-slate-900 border border-slate-600 rounded-md">
      <span>of {{ totalPages }}</span>
      <button type="submit" class="px-3 py-1 bg-cyan-600 hover:bg-cyan-500 rounded-md font-semibold transition-colors">Go</button>
    </form>

    <!-- Next & Last -->
    <div class="flex items-center gap-2">
      <button @click="changePage(currentPage + 1)" :disabled="currentPage === totalPages" :class="buttonClass(currentPage === totalPages)">
        Next
      </button>
      <button @click="changePage(totalPages)" :disabled="currentPage === totalPages" :class="buttonClass(currentPage === totalPages)">
        Last &raquo;
      </button>
    </div>
  </div>
</template>
