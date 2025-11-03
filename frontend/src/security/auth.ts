import { defineStore } from 'pinia';
import { ref } from 'vue';
import axios from 'axios';
import router from '../router';

// The base URL for your API
const API_BASE_URL = 'http://127.0.0.1:8000';

export const useAuthStore = defineStore('auth', () => {
    const token = ref(localStorage.getItem('token') || null);
    const user = ref(JSON.parse(localStorage.getItem('user') || 'null'));

    // Set up Axios to automatically send the token with every request
    axios.interceptors.request.use(config => {
        if (token.value) {
            config.headers.Authorization = `Bearer ${token.value}`;
        }
        return config;
    });

    function setToken(newToken: string) {
        token.value = newToken;
        localStorage.setItem('token', newToken);
    }

    function setUser(newUser: object) {
        user.value = newUser;
        localStorage.setItem('user', JSON.stringify(newUser));
    }

    function clearAuth() {
        token.value = null;
        user.value = null;
        localStorage.removeItem('token');
        localStorage.removeItem('user');
    }

    async function login(formData: URLSearchParams) {
        // FastAPI's OAuth2PasswordRequestForm expects form data, not JSON
        const response = await axios.post(`${API_BASE_URL}/api/token`, formData);
        setToken(response.data.access_token);
        // After login, you would typically fetch the user's details
        // For now, we'll just store the username from the form.
        setUser({ username: formData.get('username') });
    }

    function logout() {
        clearAuth();
        router.push('/login'); // Redirect to login page
    }

    return { token, user, login, logout };
});