<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/security/auth';
import InputTextbox from './components/base/InputTextbox.vue';
import SubmitButton from './components/base/SubmitButton.vue';

// ============================================================
// State
// ============================================================

const username = ref('');
const password = ref('');
const error = ref('');
const isSubmitting = ref(false);

const router = useRouter();
const authStore = useAuthStore();

// ============================================================
// Actions
// ============================================================

const handleLogin = async () => {
  isSubmitting.value = true;
  error.value = '';

  try {
    const formData = new URLSearchParams({ 
      username: username.value, 
      password: password.value,
    });

    await authStore.login(formData);
    router.push('/');
  } catch (err) {
    error.value = 'Failed to login. Please check your credentials.';
    console.error(err);
  } finally {
    isSubmitting.value = false;
  }
};
</script>

<template>
  <div class="flex items-center justify-center min-h-screen pt-20">
    <div class="p-8 bg-slate-800/50 backdrop-blur-lg rounded-lg shadow-xl w-full max-w-md">
      <h1 class="text-3xl font-bold text-white text-center mb-6">Login</h1>
      <form @submit.prevent="handleLogin">
        <InputTextbox 
          v-model="username" 
          label="Username"
        />

        <InputTextbox 
          v-model="password" 
          label="Password" 
          type="password"
        />

        <SubmitButton 
          type="submit" 
          :disabled="isSubmitting"
          :label="isSubmitting ? 'Logging in...' : 'Login'"
        />
        <p v-if="error" class="text-red-400 text-center mt-4">{{ error }}</p>
      </form>
      
      <div class="text-center mt-6">
        <p class="text-slate-400">
          Don't have an account?
          <router-link to="/register" class="font-medium text-cyan-400 hover:underline">
            Register here
          </router-link>
        </p>
      </div>

    </div>
  </div>
</template>