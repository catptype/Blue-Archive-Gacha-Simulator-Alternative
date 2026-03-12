import axios, { type InternalAxiosRequestConfig, type AxiosResponse, type AxiosError } from 'axios';
import { useAuthStore } from '@/security/auth';
import { API_BASE_URL } from '@/config';

// A flag to track if we are already in the process of logging out
let isLoggingOut = false;

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: { 'Content-Type': 'application/json' }
});

// REQUEST INTERCEPTOR
apiClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const authStore = useAuthStore();
    
    if (authStore.token && config.headers) {
      // Use bracket notation or ensured headers to satisfy TS
      config.headers.Authorization = `Bearer ${authStore.token}`;
    }
    return config;
  },
  (error: AxiosError) => Promise.reject(error)
);

// RESPONSE INTERCEPTOR
apiClient.interceptors.response.use(
  (response: AxiosResponse) => response,
  async (error: AxiosError) => {
    
    // Check if the error is 401
    if (error.response?.status === 401) {
      const authStore = useAuthStore();

      // ONLY run this block if we aren't already logging out
      if (!isLoggingOut) {
        isLoggingOut = true; // Set the lock

        console.warn("Session expired. Logging out.");
        alert("Session expired. Logging out.")

        await authStore.logout(); 

        // After some time or after navigation, reset the lock 
        setTimeout(() => { isLoggingOut = false; }, 5000);
      }

      // Important: Stop the spam for the other 7 requests
      // We return a "silent" rejection or just stop the chain
      return Promise.reject(new Error("Session expired"));
    }

    return Promise.reject(error);
  }
);

export default apiClient;