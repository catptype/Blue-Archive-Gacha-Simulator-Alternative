<script setup lang="ts">
import { ref, onMounted } from 'vue';
import axios from 'axios';
import Background from '../components/Background.vue';
import SchoolList from '../components/student/SchoolFilter.vue';
import StudentCarousel from '../components/student/StudentCarousel.vue';

interface School { school_id: number; school_name: string; image_url: string; }
interface Student { student_id: number; student_name: string; portrait_url: string; }

// --- State managed by the parent ---
const schools = ref<School[]>([]);
const students = ref<Student[]>([]);
const selectedSchoolId = ref<number | null>(null);
const isLoadingSchools = ref(true);
const isLoadingStudents = ref(true);
const isSidebarExpanded = ref(false); // State for sidebar expansion

const API_BASE_URL = 'http://127.0.0.1:8000/api'; // Or your FastAPI URL

// --- Methods ---
async function fetchSchools() {
  isLoadingSchools.value = true;
  try {
    const response = await axios.get(`${API_BASE_URL}/schools/`);
    schools.value = response.data;
    // Automatically select the first school on load
    if (schools.value.length > 0) {
      handleSchoolSelect(schools.value[0]);
    }
  } catch (error) { console.error('Failed to fetch schools:', error); }
  finally { isLoadingSchools.value = false; }
}

async function handleSchoolSelect(school: School) {
  if (school.school_id === selectedSchoolId.value) return; // Don't reload if already selected

  selectedSchoolId.value = school.school_id;
  isLoadingStudents.value = true;
  try {
    const response = await axios.get(`${API_BASE_URL}/students/?school_id=${school.school_id}&version_id=1`);
    students.value = response.data;
  } catch (error) { console.error('Failed to fetch students:', error); }
  finally { isLoadingStudents.value = false; }
}

// Fetch initial data when the component is mounted
onMounted(fetchSchools);
</script>

<template>
  <!-- Main wrapper, pt-20 is for the fixed navbar -->
  <div class="relative min-h-screen w-full bg-black antialiased text-white overflow-hidden pt-20">
    <Background />
    
    <!-- 
      The main grid. Its class is dynamically bound to expand/collapse.
      The style provides the height calculation.
    -->
    <div
      id="main-grid"
      class="absolute top-20 left-0 right-0"
      :class="{ 'sidebar-expanded': isSidebarExpanded }"
      style="height: calc(100vh - 5rem);"
    >
      <!-- Left Column -->
      <SchoolList
        :schools="schools"
        :selected-id="selectedSchoolId"
        :is-loading="isLoadingSchools"
        @select-school="handleSchoolSelect"
        @update:sidebar-expanded="isSidebarExpanded = $event"
      />

      <!-- Right Column -->
      <Transition name="fade" mode="out-in">
        <StudentCarousel
          :key="selectedSchoolId"
          :students="students"
          :is-loading="isLoadingStudents"
          :is-sidebar-expanded="isSidebarExpanded"
        />
      </Transition>
    </div>
  </div>
</template>

<style>
/* Global styles from student-page.css needed for the grid and transitions */
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