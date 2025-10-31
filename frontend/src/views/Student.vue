<script setup lang="ts">
import { ref, onMounted } from 'vue';
import SchoolFilter from '../components/student/SchoolFilter.vue';
import StudentCarousel from '../components/student/StudentCarousel.vue';

// --- Interfaces for our data shapes ---
interface School {
  school_id: string;
  school_name: string;
  image_url: string;
}
interface Student {
  student_id: string;
  student_name: string;
  image_url: string;
}

// --- Reactive State ---
const schools = ref<School[]>([]);
const students = ref<Student[]>([]);
const selectedSchoolId = ref<string | null>(null);
const isLoading = ref(true);

// --- MOCK API DATA (Replace with actual fetch calls) ---
const MOCK_SCHOOLS: School[] = [
  { school_id: 'abydos', school_name: 'Abydos', image_url: '/school_icons/abydos.png' },
  { school_id: 'gehenna', school_name: 'Gehenna', image_url: '/school_icons/gehenna.png' },
  { school_id: 'millennium', school_name: 'Millennium', image_url: '/school_icons/millennium.png' },
  { school_id: 'trinity', school_name: 'Trinity', image_url: '/school_icons/trinity.png' },
];
const MOCK_STUDENTS: Record<string, Student[]> = {
  abydos: [
    { student_id: 'shiroko', student_name: 'Shiroko', image_url: '/student_portraits/shiroko.png' },
    { student_id: 'hoshino', student_name: 'Hoshino', image_url: '/student_portraits/hoshino.png' },
  ],
  gehenna: [
    { student_id: 'hina', student_name: 'Hina', image_url: '/student_portraits/hina.png' },
    { student_id: 'ako', student_name: 'Ako', image_url: '/student_portraits/ako.png' },
  ],
  millennium: [
    { student_id: 'yuuka', student_name: 'Yuuka', image_url: '/student_portraits/yuuka.png' },
    { student_id: 'noa', student_name: 'Noa', image_url: '/student_portraits/noa.png' },
  ],
  trinity: [
    { student_id: 'mika', student_name: 'Mika', image_url: '/student_portraits/mika.png' },
    { student_id: 'nagisa', student_name: 'Nagisa', image_url: '/student_portraits/nagisa.png' },
  ]
};

// --- Logic ---

// This function will be called when a school is selected in the child component
async function fetchStudentsForSchool(schoolId: string) {
  if (selectedSchoolId.value === schoolId) return; // Don't refetch if already selected

  selectedSchoolId.value = schoolId;
  isLoading.value = true;
  students.value = []; // Clear current students

  console.log(`Fetching students for ${schoolId}...`);

  // --- REPLACE THIS with a real API call ---
  // const response = await fetch(`/api/students?school_id=${schoolId}`);
  // const data = await response.json();
  // students.value = data;
  await new Promise(resolve => setTimeout(resolve, 500)); // Simulate network delay
  students.value = MOCK_STUDENTS[schoolId] || [];
  // --- END of replacement section ---

  isLoading.value = false;
}

// onMounted is a Vue lifecycle hook that runs once when the component is first created.
onMounted(async () => {
  // --- REPLACE THIS with a real API call to fetch schools ---
  // const response = await fetch('/api/schools');
  // const data = await response.json();
  // schools.value = data;
  await new Promise(resolve => setTimeout(resolve, 200)); // Simulate network delay
  schools.value = MOCK_SCHOOLS;
  // --- END of replacement section ---
  
  // After fetching schools, automatically select the first one
  if (schools.value.length > 0) {
    fetchStudentsForSchool(schools.value[0].school_id);
  }
});

</script>



<template>
  <!-- Main grid container, positioned below the navbar -->
  <div class="absolute top-20 left-0 right-0" style="height: calc(100vh - 5rem); display: grid; grid-template-columns: auto 1fr;">
    
    <!-- Left Column: School Filter -->
    <SchoolFilter 
      :schools="schools" 
      :selected-school-id="selectedSchoolId"
      @select-school="fetchStudentsForSchool"
    />

    <!-- Right Column: Student Display -->
    <StudentCarousel 
      :students="students"
      :is-loading="isLoading"
    />

  </div>
</template>