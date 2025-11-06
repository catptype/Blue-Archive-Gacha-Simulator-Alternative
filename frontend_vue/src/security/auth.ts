import { defineStore } from 'pinia';
import { ref } from 'vue';
import router from '../router';
import apiClient from '../services/client'; 

export const useAuthStore = defineStore('auth', () => {
    const token = ref(localStorage.getItem('token') || null);
    const user = ref(JSON.parse(localStorage.getItem('user') || 'null'));

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
        const response = await apiClient.post('/token', formData, {
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        });

        setToken(response.data.access_token);
        // After login, you would typically fetch the user's details
        // For now, we'll just store the username from the form.
        setUser({ username: formData.get('username') });
    }

    function logout() {
        clearAuth();
        router.push('/'); // Redirect to home page
    }

    return { token, user, login, logout };
});