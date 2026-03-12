<script setup lang="ts">
  import LoadSpinner from '@/components/base/LoadSpinner.vue';
  import SchoolButton from '../components/SchoolButton.vue';

  interface School {
    id: number;
    name: string;
    image_url: string;
  }

  defineProps<{
    schools: School[];
    selectedId: number | null;
    isLoading: boolean;
  }>();

  const emit = defineEmits(['update:sidebarExpanded', 'selectSchool']);
</script>

<template>

  <div
    @mouseenter="emit('update:sidebarExpanded', true)"
    @mouseleave="emit('update:sidebarExpanded', false)"
    class="relative z-40 bg-black/60 backdrop-blur-sm border-r border-gray-800 p-3 flex flex-col gap-y-3 transition-all duration-300 ease-in-out overflow-y-auto"
  >
    <LoadSpinner v-if="isLoading" />

    <template v-else>
      <SchoolButton
        v-for="school in schools"
        :key="school.id"
        :school="school"
        :isActive="school.id === selectedId"
        @select="emit('selectSchool', school)"
      />
    </template>

  </div>
</template>

<style scoped>
/* Modern Scrollbar Styling */
div::-webkit-scrollbar { width: 8px; }
div::-webkit-scrollbar-track { background: transparent; }
div::-webkit-scrollbar-thumb {
  background-color: rgba(107, 114, 128, 0.4);
  border-radius: 10px;
  border: 2px solid transparent;
  background-clip: padding-box;
}
div::-webkit-scrollbar-thumb:hover { background-color: rgba(156, 163, 175, 0.6); }
div { scrollbar-width: thin; scrollbar-color: rgba(107, 114, 128, 0.4) transparent; }
</style>