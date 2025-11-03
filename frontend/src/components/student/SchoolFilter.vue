<script setup lang="ts">
interface School {
  school_id: number;
  school_name: string;
  image_url: string;
}

defineProps<{
  schools: School[];
  selectedId: number | null;
  isLoading: boolean;
}>();

const emit = defineEmits<{
  (e: 'selectSchool', school: School): void;
  (e: 'update:sidebarExpanded', isExpanded: boolean): void;
}>();
</script>

<template>
  <!-- 
    The component's root element handles the hover state for expansion.
    @mouseenter and @mouseleave are Vue's equivalent of onmouseenter/onmouseleave.
  -->
  <div
    @mouseenter="emit('update:sidebarExpanded', true)"
    @mouseleave="emit('update:sidebarExpanded', false)"
    class="relative z-40 bg-black/60 backdrop-blur-sm border-r border-gray-800 p-3 flex flex-col gap-y-3 transition-all duration-300 ease-in-out overflow-y-auto"
  >
    <div v-if="isLoading" class="text-slate-400 p-2">Loading...</div>
    <button
      v-for="school in schools"
      :key="school.school_id"
      @click="emit('selectSchool', school)"
      class="school-button w-full p-2 rounded-lg flex items-center transition-colors duration-300 ease-in-out bg-gray-600/80 hover:bg-sky-600/70"
      :class="{ 'active ring-2 ring-sky-400': school.school_id === selectedId }"
    >
      <img :src="school.image_url" :alt="`${school.school_name} Logo`" class="h-12 w-12 object-contain flex-shrink-0 transition-all duration-300">
      <span class="school-name ml-3 font-bold text-lg whitespace-nowrap overflow-hidden transition-all duration-300 ease-in-out opacity-0 max-w-0">
        {{ school.school_name }}
      </span>
    </button>
  </div>
</template>

<style scoped>
/* Scoped CSS from student-page.css, specific to this component */
.school-button img {
  filter: drop-shadow(0 0 8px rgba(56, 189, 248, 0.8));
}
.school-button:hover img {
  transform: scale(1.1);
}

/* 
  When the parent div is hovered, the .school-name inside it expands.
  This works because the hover state is on the parent of the span.
*/
div:hover .school-name {
  opacity: 1;
  max-width: 200px;
}

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