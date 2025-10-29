<script setup lang="ts">
import { ref } from 'vue';
import logo from '../assets/logo.png';

// This replaces Alpine's x-data. `ref` creates reactive variables.
const openMenu = ref(false);
const openDropdown = ref(false);

// This is a MOCK user object. Later, you will fetch this data from your API.
// To test the logged-out view, set isAuthenticated to false.
const user = ref({
  isAuthenticated: true,
  username: 'Sensei',
});

function logout() {
  console.log('Logging out...');
  // Here you would make an API call to your FastAPI backend to log the user out
  user.value.isAuthenticated = false; // Update the state
  openDropdown.value = false;
  openMenu.value = false;
}
</script>

<template>
  <!-- 
    The root nav element. 
    - Vue's @click is the equivalent of Alpine's @click.
    - We will manage state inside the <script> section.
  -->
  <nav class="fixed top-0 left-0 right-0 z-50 bg-slate-900/60 backdrop-blur-lg border-b border-slate-700/50">
    <div class="w-full max-w-6xl mx-auto px-4">
      <div class="flex items-center justify-between h-20">
        
        <!-- Navbar Brand: <router-link> is Vue Router's version of <a> for internal links -->
        <router-link to="/" class="flex-shrink-0">
          <img :src="logo" alt="logo" class="h-12 w-auto">
        </router-link>

        <!-- Primary Navigation (Desktop) -->
        <div class="hidden lg:flex lg:items-center lg:space-x-8">
          <router-link to="/student" class="text-slate-300 hover:text-cyan-400 transition-colors duration-200">Student</router-link>
          <router-link to="/gacha" class="text-slate-300 hover:text-cyan-400 transition-colors duration-200">Gacha</router-link>
          
          <!-- User auth links (Desktop): v-if/v-else replaces Django's {% if %} -->
          <div v-if="user.isAuthenticated" class="relative">
            <!-- Dropdown Toggle Button -->
            <button @click="openDropdown = !openDropdown" class="flex items-center space-x-2 text-slate-300 hover:text-cyan-400 transition-colors duration-200">
              <span>{{ user.username }}</span>
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
            </button>
            
            <!-- Dropdown Menu: v-show toggles visibility, just like Alpine's x-show -->
            <div v-show="openDropdown" @click.away="openDropdown = false" class="absolute right-0 mt-2 w-48 py-2 bg-slate-800 border border-slate-700 rounded-lg shadow-xl">
              <router-link to="/dashboard" class="block px-4 py-2 text-sm text-slate-300 hover:bg-slate-700 hover:text-cyan-400">Dashboard</router-link>
              <button @click="logout" type="button" class="w-full text-left px-4 py-2 text-sm text-slate-300 hover:bg-slate-700 hover:text-cyan-400">Logout</button>
            </div>
          </div>
          <div v-else class="flex items-center space-x-4">
            <router-link to="/register" class="text-slate-300 hover:text-cyan-400 transition-colors duration-200">Register</router-link>
            <router-link to="/login" class="px-4 py-2 text-white bg-cyan-600 hover:bg-cyan-500 rounded-md transition-colors duration-200">Login</router-link>
          </div>
        </div>

        <!-- Mobile Menu Button -->
        <div class="lg:hidden">
          <button @click="openMenu = !openMenu" class="text-slate-300 hover:text-cyan-400">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16m-7 6h7"></path></svg>
          </button>
        </div>

      </div>
    </div>

    <!-- Mobile Menu (collapsible) -->
    <div v-show="openMenu" class="lg:hidden bg-slate-900/80 border-t border-slate-700">
      <div class="px-4 pt-2 pb-4 space-y-2">
        <router-link to="/student" class="block px-3 py-2 text-slate-300 hover:bg-slate-700 rounded-md">Student</router-link>
        <router-link to="/gacha" class="block px-3 py-2 text-slate-300 hover:bg-slate-700 rounded-md">Gacha</router-link>
        <hr class="border-slate-700">

        <!-- Mobile auth links -->
        <div v-if="user.isAuthenticated">
          <div class="px-3 py-2 text-slate-400 font-semibold">{{ user.username }}</div>
          <router-link to="/dashboard" class="block px-3 py-2 text-slate-300 hover:bg-slate-700 rounded-md">Dashboard</router-link>
          <button @click="logout" type="button" class="w-full text-left block px-3 py-2 text-slate-300 hover:bg-slate-700 rounded-md">Logout</button>
        </div>
        <div v-else>
          <router-link to="/register" class="block px-3 py-2 text-slate-300 hover:bg-slate-700 rounded-md">Register</router-link>
          <router-link to="/login" class="block px-3 py-2 text-slate-300 hover:bg-slate-700 rounded-md">Login</router-link>
        </div>
      </div>
    </div>
  </nav>
</template>

