import axios from 'axios';
import { useAuthStore } from '../security/auth';
import { API_BASE_URL } from '../config';

// Create a new Axios instance with a pre-configured base URL
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  }
});

// Use an interceptor to automatically attach the auth token to every request
apiClient.interceptors.request.use(config => {
  // We need to get a fresh instance of the store here,
  // as this file is evaluated before the main app is set up.
  const authStore = useAuthStore();
  
  if (authStore.token) {
    config.headers.Authorization = `Bearer ${authStore.token}`;
  }
  return config;
}, error => {
  return Promise.reject(error);
});

// --- ADD THIS NEW INTERCEPTOR ---
apiClient.interceptors.response.use(
  // If the response is successful, just return it
  (response) => response,
  // If there's an error...
  (error) => {
    // Check if it's a 401 Unauthorized error
    if (error.response && error.response.status === 401) {
      console.log("Token expired or invalid. Logging out.");
      alert("Token expired or invalid. Logging out.");
      const authStore = useAuthStore();
      authStore.logout(); // Call the logout action from your store
    }
    // Return the error so the component that made the call can also handle it
    return Promise.reject(error);
  }
);

export default apiClient;