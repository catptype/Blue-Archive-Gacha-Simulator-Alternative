// frontend/src/config.ts

// 1. Read the environment variable from Vite's `import.meta.env` object.
//    This object is automatically populated with variables from any `.env` files.
const apiUrlFromEnv = import.meta.env.VITE_API_BASE_URL;

// 2. Define your hardcoded default value, just like in os.getenv.
const defaultApiUrl = 'http://127.0.0.1:8000/api';

// 3. Export the final URL, using the environment variable if it exists,
//    otherwise falling back to the default.
export const API_BASE_URL = apiUrlFromEnv || defaultApiUrl;

// You can also export other configuration variables here in the future.
export const SOME_OTHER_CONFIG = 'some_value';