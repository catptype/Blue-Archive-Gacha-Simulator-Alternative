<script setup lang="ts">
  import { ref } from 'vue';
  import { useRouter } from 'vue-router';
  import axios from 'axios';
  import apiClient from '@/services/client';
  import InputTextbox from './components/InputTextbox.vue';
  import SubmitButton from './components/SubmitButton.vue';

  // ============================================================
  // State
  // ============================================================

  const username = ref('');
  const password = ref('');
  const confirmPassword = ref('');
  const error = ref('');
  const isRegistering = ref(false);

  const router = useRouter();

  // ============================================================
  // Actions
  // ============================================================

  const handleRegister = async () => {
    error.value = '';

    if (!username.value || !password.value || !confirmPassword.value) {
      error.value = 'Please fill out all fields.';
      return;
    }

    if (password.value !== confirmPassword.value) {
      error.value = 'Passwords do not match.';
      return;
    }

    isRegistering.value = true;

    try {
      await apiClient.post('/users/register/', {
        username: username.value,
        password: password.value,
      });

      router.push('/login');
    } catch (err: any) {
      error.value = axios.isAxiosError(err) && err.response
        ? err.response.data.detail ?? 'An unexpected error occurred.'
        : 'Registration failed. Please try again later.';

      console.error(err);
    } finally {
      isRegistering.value = false;
    }
  };
</script>

<template>
  <div class="flex items-center justify-center min-h-screen pt-20">
    <div class="p-8 bg-slate-800/50 backdrop-blur-lg rounded-lg shadow-xl w-full max-w-md">
      <h1 class="text-3xl font-bold text-white text-center mb-6">Create Account</h1>

      <form @submit.prevent="handleRegister">
        <InputTextbox 
          v-model="username"
          id="username"
          label="Username" 
        />
        <InputTextbox 
          v-model="password" 
          id="password"
          label="Password" 
          type="password" 
        />

        <InputTextbox 
          v-model="confirmPassword" 
          id="confirm-password"
          label="Confirm Password" 
          type="password" 
        />

        <SubmitButton 
          type="submit" 
          :disabled="isRegistering"
          :label="isRegistering ? 'Registering...' : 'Register'"
        />

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
