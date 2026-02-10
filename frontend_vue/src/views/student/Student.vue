<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { type Student, type School } from '@/types/web';
import Background from '@/components/Background.vue';
import SchoolSidebar from './layout/SchoolSidebar.vue';
import StudentCarousel from './layout/StudentCarousel.vue';
import apiClient from '@/services/client'; 

// --- State managed by the parent ---
const schools = ref<School[]>([]);
const students = ref<Student[]>([]);
const selectedSchoolId = ref<number | null>(null);
const isLoadingSchools = ref(true);
const isLoadingStudents = ref(true);
const isSidebarExpanded = ref(false);

// --- Methods ---
async function handleSchoolSelect(school: School) {
  if (school.id === selectedSchoolId.value) return; // Don't reload if already selected

  selectedSchoolId.value = school.id;
  isLoadingStudents.value = true;
  try {
    const response = await apiClient.get(`/students/?school_id=${school.id}&version_id=1`);
    students.value = response.data;
  } catch (error) { console.error('Failed to fetch students:', error); }
  finally { isLoadingStudents.value = false; }
}

// Fetch initial data when the component is mounted
onMounted(async () => {
  isLoadingSchools.value = true;
  try {
    const response = await apiClient.get('/schools/');
    schools.value = response.data;
    const firstSchool = schools.value[0];
    if (firstSchool) {
      handleSchoolSelect(firstSchool);
    }
  } catch (error) {
    console.error('Failed to fetch schools:', error);
  } finally {
    isLoadingSchools.value = false;
  }
});
</script>

<template>
  <!-- Main wrapper, pt-20 is for the fixed navbar -->
  <div class="relative min-h-screen w-full bg-black antialiased text-white overflow-hidden pt-20">
    <Background />
    
    <div
      id="main-grid"
      class="absolute top-20 left-0 right-0"
      :class="{ 'sidebar-expanded': isSidebarExpanded }"
      style="height: calc(100vh - 5rem);"
    >
      <!-- Left Column -->
      <SchoolSidebar
        :schools="schools"
        :selected-id="selectedSchoolId"
        :is-loading="isLoadingSchools"
        @select-school="handleSchoolSelect"
        @update:sidebar-expanded="isSidebarExpanded = $event"
      />

      <!-- Right Column -->
      <Transition name="fade" mode="out-in">
        <StudentCarousel
          :students="students"
          :is-loading="isLoadingStudents"
          :is-sidebar-expanded="isSidebarExpanded"
        />
      </Transition>
    </div>
  </div>
</template>

<style>
#main-grid {
  display: grid;
  grid-template-columns: 6rem 1fr;
  transition: grid-template-columns 300ms ease-in-out;
}
#main-grid.sidebar-expanded {
  grid-template-columns: 16rem 1fr;
}

/* Vue Transition styles for the fade effect */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>