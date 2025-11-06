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

export default apiClient;