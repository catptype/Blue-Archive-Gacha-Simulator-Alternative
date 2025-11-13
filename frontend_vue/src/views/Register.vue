<script setup lang="ts">
    import { ref } from 'vue';
    import { useRouter } from 'vue-router';
    import apiClient from '../services/client';
    import axios from 'axios';

    const username = ref('');
    const password = ref('');
    const confirmPassword = ref('');
    const error = ref('');
    const isLoading = ref(false);
    const router = useRouter();

    const handleRegister = async () => {
        // Clear previous errors on a new submission
        error.value = '';
        
        // --- START: ADDED VALIDATION LOGIC ---
        if (!username.value || !password.value || !confirmPassword.value) {
            error.value = 'Please fill out all fields.';
            return; // Stop the function
        }

        if (password.value !== confirmPassword.value) {
            error.value = 'Passwords do not match.';
            return; // Stop the function
        }
        // --- END: ADDED VALIDATION LOGIC ---

        isLoading.value = true;

        try {
            // The API request remains the same, sending only the final password
            await apiClient.post('/register/', {
              username: username.value,
              password: password.value,
            });

            // On success, redirect the user to the login page to sign in.
            router.push('/login');

        } catch (err: any) {
            // if (apiClient.isAxiosError(err) && err.response) {
            if (axios.isAxiosError(err) && err.response) {
                error.value = err.response.data.detail || 'An unexpected error occurred.';
            } else {
                error.value = 'Registration failed. Please try again later.';
            }
            console.error(err);
        } finally {
            isLoading.value = false;
        }
    };
</script>

<template>
  <div class="flex items-center justify-center min-h-screen pt-20">
    <div class="p-8 bg-slate-800/50 backdrop-blur-lg rounded-lg shadow-xl w-full max-w-md">
      <h1 class="text-3xl font-bold text-white text-center mb-6">Create Account</h1>

      <form @submit.prevent="handleRegister">
        <div class="mb-4">
          <label for="username" class="block text-slate-300 mb-2">Username</label>
          <input
            v-model="username"
            id="username"
            type="text"
            required
            class="w-full p-2 rounded bg-slate-700 text-white border border-slate-600 focus:outline-none focus:ring-2 focus:ring-cyan-500"
          >
        </div>
        <div class="mb-4"> <!-- Reduced bottom margin -->
          <label for="password" class="block text-slate-300 mb-2">Password</label>
          <input
            v-model="password"
            id="password"
            type="password"
            required
            maxlength="20"
            class="w-full p-2 rounded bg-slate-700 text-white border border-slate-600 focus:outline-none focus:ring-2 focus:ring-cyan-500"
          >
        </div>
        <!-- START: ADDED CONFIRM PASSWORD BLOCK -->
        <div class="mb-6">
          <label for="confirm-password" class="block text-slate-300 mb-2">Confirm Password</label>
          <input
            v-model="confirmPassword"
            id="confirm-password"
            type="password"
            required
            maxlength="20"
            class="w-full p-2 rounded bg-slate-700 text-white border border-slate-600 focus:outline-none focus:ring-2 focus:ring-cyan-500"
          >
        </div>
        <!-- END: ADDED CONFIRM PASSWORD BLOCK -->
        <button
          type="submit"
          class="w-full py-2 px-4 bg-cyan-600 hover:bg-cyan-500 rounded text-white font-bold transition-colors"
          :disabled="isLoading"
        >
          {{ isLoading ? 'Registering...' : 'Register' }}
        </button>
        <p v-if="error" class="text-red-400 text-center mt-4">{{ error }}</p>
      </form>

      <div class="text-center mt-6">
        <p class="text-slate-400">
          Already have an account?
          <router-link to="/login" class="font-medium text-cyan-400 hover:underline">
            Login here
          </router-link>
        </p>
      </div>
    </div>
  </div>
</template>
