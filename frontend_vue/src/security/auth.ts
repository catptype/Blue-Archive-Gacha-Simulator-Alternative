import { defineStore } from 'pinia';
import { ref } from 'vue';
import router from '@/router';
import apiClient from '@/services/client'; 

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

    // --- NEW: Function to fetch user data from the protected endpoint ---
    async function fetchUser() {
        if (!token.value) return; // Don't try if there's no token
        try {
            const response = await apiClient.get('/users/me');
            setUser(response.data); // Set the user with full data (id, role, etc.)
        } catch (error) {
            // This is where the magic happens!
            // If the token is expired, this call will fail with a 401.
            // The Axios response interceptor will catch it and call clearAuth().
            console.error("Failed to fetch user. Token might be invalid.", error);
        }
    }

    function logout() {
        clearAuth();
        router.push('/'); // Redirect to home page
    }

    return { token, user, login, logout, fetchUser };
});