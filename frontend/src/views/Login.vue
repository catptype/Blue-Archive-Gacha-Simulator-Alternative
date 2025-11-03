<script setup lang="ts">
    import { ref } from 'vue';
    import { useRouter } from 'vue-router';
    import { useAuthStore } from '../security/auth';

    const username = ref('');
    const password = ref('');
    const error = ref('');
    const router = useRouter();
    const authStore = useAuthStore();

    const handleLogin = async () => {
    try {
        const formData = new URLSearchParams();
        formData.append('username', username.value);
        formData.append('password', password.value);
        await authStore.login(formData);
        router.push('/'); // Redirect to dashboard page on successful login
    } catch (err) {
        error.value = 'Failed to login. Please check your credentials.';
        console.error(err);
    }
    };
</script>

<template>
  <div class="flex items-center justify-center min-h-screen pt-20">
    <div class="p-8 bg-slate-800/50 backdrop-blur-lg rounded-lg shadow-xl w-full max-w-md">
      <h1 class="text-3xl font-bold text-white text-center mb-6">Login</h1>
      <form @submit.prevent="handleLogin">
        <div class="mb-4">
          <label class="block text-slate-300 mb-2">Username</label>
          <input v-model="username" type="text" class="w-full p-2 rounded bg-slate-700 text-white border border-slate-600 focus:outline-none focus:ring-2 focus:ring-cyan-500">
        </div>
        <div class="mb-6">
          <label class="block text-slate-300 mb-2">Password</label>
          <input v-model="password" type="password" class="w-full p-2 rounded bg-slate-700 text-white border border-slate-600 focus:outline-none focus:ring-2 focus:ring-cyan-500">
        </div>
        <button type="submit" class="w-full py-2 px-4 bg-cyan-600 hover:bg-cyan-500 rounded text-white font-bold transition-colors">
          Login
        </button>
        <p v-if="error" class="text-red-400 text-center mt-4">{{ error }}</p>
      </form>
    </div>
  </div>
</template>