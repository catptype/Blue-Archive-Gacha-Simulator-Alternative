<script setup lang="ts">
// Define the shape of the data this component expects
interface School {
  school_id: string;
  school_name: string;
  image_url: string;
}

// Define the props passed from the parent component
defineProps<{
  schools: School[];
  selectedSchoolId: string | null;
}>();

// Define the events this component can emit to the parent
const emit = defineEmits(['select-school']);

function selectSchool(schoolId: string) {
  emit('select-school', schoolId);
}
</script>

<template>
  <!-- 
    The #left-column styling is handled here.
    - We use the 'group' utility from Tailwind to manage the hover effect.
    - When this div is hovered over (`group-hover:`), the school names inside will become visible.
  -->
  <div class="group relative z-40 bg-black/60 backdrop-blur-sm border-r border-gray-800 p-3 flex flex-col gap-y-3 transition-all duration-300 ease-in-out overflow-y-auto w-20 hover:w-56">
    <button
      v-for="school in schools"
      :key="school.school_id"
      @click="selectSchool(school.school_id)"
      class="w-full p-2 rounded-lg flex items-center transition-colors duration-300 ease-in-out bg-gray-600/80 hover:bg-sky-600/70"
      :class="{ 'ring-2 ring-sky-400': school.school_id === selectedSchoolId }"
    >
      <!-- We will assume images are served from the API or a CDN -->
      <img :src="school.image_url" :alt="`${school.school_name} Logo`" class="h-12 w-12 object-contain flex-shrink-0 transition-all duration-300">
      
      <!-- 
        School name styling.
        - By default, it's invisible and takes up no space (opacity-0 max-w-0).
        - On group-hover, it fades in and expands.
      -->
      <span class="school-name ml-3 font-bold text-lg whitespace-nowrap overflow-hidden transition-all duration-300 ease-in-out opacity-0 max-w-0 group-hover:opacity-100 group-hover:max-w-full">
        {{ school.school_name }}
      </span>
    </button>
  </div>
</template>
